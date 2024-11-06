from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class FiToTypeMappingHistory(Base):
    __tablename__ = "fi_to_type_mapping_history"
    fi_id: Mapped[str] = mapped_column(primary_key=True)


class FinancialInstitutionsHistory(Base):
    __tablename__ = "financial_institutions_history"
    lei: Mapped[str] = mapped_column(primary_key=True)
