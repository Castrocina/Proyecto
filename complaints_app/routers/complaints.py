from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth as auth_service, crud, ml, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/complaints", tags=["complaints"])


@router.post("/", response_model=schemas.ComplaintRead, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint: schemas.ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user),
):
    product = db.query(models.Product).filter(models.Product.id == complaint.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    service_areas = crud.get_service_areas(db)
    candidate_labels = [area.name for area in service_areas] or [
        "Atención General"
    ]
    predicted_label, score = ml.predict_responsible_area(
        product_name=product.name,
        description=complaint.description,
        candidate_labels=candidate_labels,
    )
    service_area = crud.find_service_area_by_name(db, predicted_label)
    new_complaint = crud.create_complaint(
        db,
        owner=current_user,
        complaint_data=complaint,
        predicted_label=predicted_label,
        score=score,
        service_area=service_area,
    )
    return new_complaint


@router.get("/", response_model=list[schemas.ComplaintRead])
def list_complaints(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user),
):
    return (
        db.query(models.Complaint)
        .filter(models.Complaint.owner_id == current_user.id)
        .order_by(models.Complaint.created_at.desc())
        .all()
    )
