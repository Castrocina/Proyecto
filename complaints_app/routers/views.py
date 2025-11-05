from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import auth as auth_service, crud, ml, models, schemas
from ..config import settings
from ..database import get_db

router = APIRouter()
template_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(template_dir))


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def login_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        context = {"request": request, "error": "Correo o contraseña incorrectos"}
        return templates.TemplateResponse("login.html", context, status_code=status.HTTP_401_UNAUTHORIZED)

    token = auth_service.create_access_token(data={"sub": user.id})
    redirect = RedirectResponse(url="/complaint", status_code=status.HTTP_303_SEE_OTHER)
    redirect.set_cookie("access_token", token, httponly=True)
    return redirect


@router.get("/complaint", response_class=HTMLResponse)
def complaint_form(
    request: Request,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    products = crud.get_products(db)
    complaints = (
        db.query(models.Complaint)
        .filter(models.Complaint.owner_id == current_user.id)
        .order_by(models.Complaint.created_at.desc())
        .all()
    )
    context = {
        "request": request,
        "products": products,
        "complaints": complaints,
        "message": request.query_params.get("message"),
    }
    return templates.TemplateResponse("complaint_form.html", context)


@router.post("/complaint", response_class=HTMLResponse)
def submit_complaint(
    request: Request,
    product_id: int = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    service_areas = crud.get_service_areas(db)
    candidate_labels = [area.name for area in service_areas] or settings.candidate_areas
    predicted_label, score = ml.predict_responsible_area(
        product_name=product.name,
        description=description,
        candidate_labels=candidate_labels,
    )
    area = crud.find_service_area_by_name(db, predicted_label)

    complaint_payload = schemas.ComplaintCreate(product_id=product_id, description=description)
    crud.create_complaint(
        db,
        owner=current_user,
        complaint_data=complaint_payload,
        predicted_label=predicted_label,
        score=score,
        service_area=area,
    )
    redirect = RedirectResponse(url="/complaint?message=Reclamación%20registrada", status_code=status.HTTP_303_SEE_OTHER)
    return redirect


@router.post("/logout", response_class=HTMLResponse)
def logout_view(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
