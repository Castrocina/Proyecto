from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    complaints: Mapped[List["Complaint"]] = relationship(
        "Complaint", back_populates="owner", cascade="all, delete-orphan"
    )


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)

    complaints: Mapped[List["Complaint"]] = relationship("Complaint", back_populates="product")


class ServiceArea(Base, TimestampMixin):
    __tablename__ = "service_areas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=False)

    complaints: Mapped[List["Complaint"]] = relationship(
        "Complaint", back_populates="area", cascade="all, delete-orphan"
    )


class ComplaintType(Base, TimestampMixin):
    __tablename__ = "complaint_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)

    complaints: Mapped[List["Complaint"]] = relationship(
        "Complaint", back_populates="complaint_type"
    )


class Complaint(Base, TimestampMixin):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    complaint_type_id: Mapped[int | None] = mapped_column(
        ForeignKey("complaint_types.id"), nullable=True
    )
    area_id: Mapped[int | None] = mapped_column(ForeignKey("service_areas.id"))
    predicted_label: Mapped[str | None] = mapped_column(String(250))
    score: Mapped[float | None] = mapped_column(Float)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    product: Mapped[Product] = relationship("Product", back_populates="complaints")
    complaint_type: Mapped[ComplaintType | None] = relationship(
        "ComplaintType", back_populates="complaints"
    )
    area: Mapped[ServiceArea | None] = relationship(
        "ServiceArea", back_populates="complaints"
    )
    owner: Mapped[User | None] = relationship("User", back_populates="complaints")
