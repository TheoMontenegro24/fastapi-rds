from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ClienteBase(SQLModel):
    nombre: str
    email: str
    telefono: Optional[str] = None

class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    facturas: List["Factura"] = Relationship(back_populates="cliente")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class FacturaBase(SQLModel):
    monto: float
    concepto: str
    cliente_id: int = Field(foreign_key="cliente.id")

class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: Optional[Cliente] = Relationship(back_populates="facturas")

class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(SQLModel):
    monto: Optional[float] = None
    concepto: Optional[str] = None
    cliente_id: Optional[int] = None