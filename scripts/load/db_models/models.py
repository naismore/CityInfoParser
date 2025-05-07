from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class FederalDistrict(Base):
    __tablename__ = 'federal_district'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    regions: Mapped[list["Region"]] = relationship("Region", back_populates="federal_district")
    cities: Mapped[list["City"]] = relationship("City", back_populates="federal_district")

    def __repr__(self):
        return f"FederalDistrict(id={self.id}, name={self.name!r})"


class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    id_federal_district: Mapped[int] = mapped_column(ForeignKey("federal_district.id"))

    federal_district: Mapped["FederalDistrict"] = relationship("FederalDistrict", back_populates="regions")
    cities: Mapped[list["City"]] = relationship("City", back_populates="region")

    def __repr__(self):
        return f"Region(id={self.id}, name={self.name!r})"


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    population: Mapped[int] = mapped_column(Integer)
    foundation_date: Mapped[datetime] = mapped_column(DateTime)
    id_region: Mapped[int] = mapped_column(ForeignKey("region.id"))
    id_federal_district: Mapped[int] = mapped_column(ForeignKey("federal_district.id"))

    region: Mapped["Region"] = relationship("Region", back_populates="cities")
    federal_district: Mapped["FederalDistrict"] = relationship("FederalDistrict", back_populates="cities")

    def __repr__(self):
        return f"City(id={self.id}, name={self.name!r})"