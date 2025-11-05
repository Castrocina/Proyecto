from typing import Iterable, Optional

from sqlalchemy.orm import Session

from . import auth, models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_products(db: Session) -> list[models.Product]:
    return db.query(models.Product).order_by(models.Product.name).all()


def get_service_areas(db: Session) -> list[models.ServiceArea]:
    return db.query(models.ServiceArea).order_by(models.ServiceArea.name).all()


def find_service_area_by_name(db: Session, name: str) -> Optional[models.ServiceArea]:
    return db.query(models.ServiceArea).filter(models.ServiceArea.name == name).first()


def create_complaint(
    db: Session,
    *,
    owner: models.User,
    complaint_data: schemas.ComplaintCreate,
    predicted_label: str,
    score: float,
    service_area: Optional[models.ServiceArea],
) -> models.Complaint:
    complaint = models.Complaint(
        description=complaint_data.description,
        product_id=complaint_data.product_id,
        complaint_type_id=complaint_data.complaint_type_id,
        area=service_area,
        predicted_label=predicted_label,
        score=score,
        owner=owner,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


def create_product(db: Session, name: str) -> models.Product:
    product = models.Product(name=name)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_service_area(db: Session, name: str, email: str, channel: str) -> models.ServiceArea:
    area = models.ServiceArea(name=name, email=email, channel=channel)
    db.add(area)
    db.commit()
    db.refresh(area)
    return area


def create_complaint_type(db: Session, name: str) -> models.ComplaintType:
    complaint_type = models.ComplaintType(name=name)
    db.add(complaint_type)
    db.commit()
    db.refresh(complaint_type)
    return complaint_type
