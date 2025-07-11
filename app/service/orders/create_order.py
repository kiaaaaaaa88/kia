from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.helper.helper import get_pg_connection
from app.utils.utils import only_user

class OrderCreate(BaseModel):
    barang_id: int = Field(..., description="ID barang")
    jumlah: int = Field(..., gt=0, description="Total barang (minimal 1)")

router = APIRouter(prefix="/order", tags=["Order (User)"])

@router.post("", summary="Order barang")
def create_order(
    order: OrderCreate,
    user=Depends(only_user) # Only user
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        # Is barang available and not empty stock?
        cur.execute("SELECT id, stock FROM barang WHERE id = %s", (order.barang_id,))
        barang = cur.fetchone()
        if not barang:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Barang not found")
        if barang["stock"] < order.jumlah:
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="The item is out of stock")
        # Input order
        cur.execute(
            "INSERT INTO orders (user_id, barang_id, jumlah) VALUES (%s, %s, %s) RETURNING id",
            (user["user_id"], order.barang_id, order.jumlah)
        )
        order_id = cur.fetchone()["id"]
        # Update stock barang
        cur.execute(
            "UPDATE barang SET stock = stock - %s WHERE id = %s",
            (order.jumlah, order.barang_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "Success",
            "message": "Order created!", 
            "order_id": order_id
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)