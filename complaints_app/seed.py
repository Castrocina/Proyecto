"""Populate the database with initial catalog data."""

from sqlalchemy.orm import Session

from . import crud, models
from .database import Base, SessionLocal, engine

PRODUCTS = [
    "Cuenta de nómina",
    "Tarjeta de crédito",
    "Cuenta de ahorro",
    "Fideicomiso",
    "Crédito hipotecario",
    "Banca en línea",
    "Banca móvil",
]

SERVICE_AREAS = [
    ("Seguridad Digital", "seguridad@example.com", "Tecnología"),
    ("Créditos Hipotecarios", "hipotecas@example.com", "Hipotecas"),
    ("Cartera Digitales", "cartera@example.com", "Tarjetas"),
    ("Mesa de Control de Inversiones", "inversiones@example.com", "Inversiones"),
    ("Facturación", "facturacion@example.com", "Facturación"),
    ("Operaciones Money e Pagos", "pagos@example.com", "Pagos"),
    ("Operaciones y Tesorería", "tesoreria@example.com", "Tesorería"),
    ("Operaciones y Efectivo", "efectivo@example.com", "Efectivo"),
    ("Medios de Pago y Tarjetas", "tarjetas@example.com", "Tarjetas"),
    ("Compensación", "compensacion@example.com", "Compensación"),
]

COMPLAINT_TYPES = [
    "Cobro no reconocido",
    "Servicio intermitente",
    "Falla de seguridad",
    "Error en estado de cuenta",
]


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        for product in PRODUCTS:
            if not db.query(models.Product).filter_by(name=product).first():
                crud.create_product(db, product)
        for name, email, channel in SERVICE_AREAS:
            if not db.query(models.ServiceArea).filter_by(name=name).first():
                crud.create_service_area(db, name, email, channel)
        for complaint_type in COMPLAINT_TYPES:
            if not db.query(models.ComplaintType).filter_by(name=complaint_type).first():
                crud.create_complaint_type(db, complaint_type)
    finally:
        db.close()


if __name__ == "__main__":
    run()
