from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, Session
from db import create_all_tables, get_session
from models import (
    Cliente, ClienteCreate, ClienteUpdate,
    Factura, FacturaCreate, FacturaUpdate
)

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente: ClienteCreate, session: Session = Depends(get_session)):
    db_cliente = Cliente.model_validate(cliente)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", response_model=list[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    return session.exec(select(Cliente)).all()

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente_data: ClienteUpdate, session: Session = Depends(get_session)):
    cliente_db = session.get(Cliente, cliente_id)
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    data_dict = cliente_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(cliente_db, key, value)
        
    session.add(cliente_db)
    session.commit()
    session.refresh(cliente_db)
    return cliente_db

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"ok": True, "mensaje": f"Cliente {cliente_id} eliminado"}


@app.post("/facturas/", response_model=Factura)
def crear_factura(factura: FacturaCreate, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, factura.cliente_id)
    if not cliente:
        raise HTTPException(status_code=400, detail="El cliente especificado no existe")
        
    db_factura = Factura.model_validate(factura)
    session.add(db_factura)
    session.commit()
    session.refresh(db_factura)
    return db_factura

@app.get("/facturas/", response_model=list[Factura])
def listar_facturas(session: Session = Depends(get_session)):
    return session.exec(select(Factura)).all()

@app.get("/facturas/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@app.put("/facturas/{factura_id}", response_model=Factura)
def actualizar_factura(factura_id: int, factura_data: FacturaUpdate, session: Session = Depends(get_session)):
    factura_db = session.get(Factura, factura_id)
    if not factura_db:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    data_dict = factura_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(factura_db, key, value)
        
    session.add(factura_db)
    session.commit()
    session.refresh(factura_db)
    return factura_db

@app.delete("/facturas/{factura_id}")
def eliminar_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    session.delete(factura)
    session.commit()
    return {"ok": True, "mensaje": f"Factura {factura_id} eliminada"}
