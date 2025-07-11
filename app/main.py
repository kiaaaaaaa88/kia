from fastapi import FastAPI
from app.service.auth import login, register
from app.service.auth_user import register_user
from app.service.barang import get_barang, create, update, delete
from app.service.orders import get_orders, create_order, update_order

app = FastAPI(
    title="Logistics App",
    description="Backend untuk aplikasi logistik barang (pencatatan, pelacakan, dan pengelolaan data pengiriman).",
    version="1.0.0"
)

# default
@app.get("/")
async def health_check():
    return {"status": "ok"}

# auth admin
app.include_router(login.router)
app.include_router(register.router)

# auth user
app.include_router(register_user.router)

# barang
app.include_router(get_barang.router)
app.include_router(create.router)
app.include_router(update.router)
app.include_router(delete.router)

# order
app.include_router(get_orders.router)
app.include_router(create_order.router)
app.include_router(update_order.router)




