from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    locations = relationship("Location", back_populates="category", cascade="save-update, merge")
    category_reviews = relationship("LocationCategoryReview", back_populates="review_category",
                                    cascade="delete, delete-orphan")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="locations")
    location_reviews = relationship("LocationCategoryReview", back_populates="review_location",
                                    cascade="delete, delete-orphan")

    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', 'name', name='_no_duplicated_locations'),
    )


class LocationCategoryReview(Base):
    __tablename__ = "location_category_review"
    id = Column(Integer, primary_key=True)
    last_reviewed_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True, default=datetime.now(tz=pytz.utc))

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    review_category = relationship("Category", back_populates="category_reviews", passive_deletes=True)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    review_location = relationship("Location", back_populates="location_reviews", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('category_id', 'location_id', name='_category_location_uc'),
    )
