from fastapi import FastAPI
from app.routes.clientes import router as clientes_router
from app.routes.productos import router as productos_router
from app.routes.ventas import router as ventas_router

app = FastAPI(
    title="SmartBusiness AI",
    version="1.0.0"
)

app.include_router(clientes_router)
app.include_router(productos_router)
app.include_router(ventas_router)

@app.get("/")
def root():
    return {
        "message": "SmartBusiness AI API funcionando correctamente"
    }