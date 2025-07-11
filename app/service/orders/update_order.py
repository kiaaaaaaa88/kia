from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.helper.helper import get_pg_connection
from app.utils.utils import only_user

class OrderUpdateStatus(BaseModel):
    status: str = Field(..., description="Status order (ex: dikirim, sampai)")

router = APIRouter(prefix="/order", tags=["Order (User)"])

@router.patch("/{order_id}", summary="Update status order (pending, sampai)")
def update_order_status(
    order_id: int,
    update: OrderUpdateStatus,
    user=Depends(only_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        # Get order, check owner and status
        cur.execute(
            "SELECT user_id, status FROM orders WHERE id = %s", (order_id,)
        )
        order = cur.fetchone()
        if not order:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Order not found")
        if order["user_id"] != user["user_id"]:
            cur.close()
            conn.close()
            raise HTTPException(status_code=403, detail="You cannot edit orders belonging to other users")
        if order["status"] != "pending":
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Orders can only be updated if still pending!")

        # Update status
        cur.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (update.status, order_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "Success", 
            "message": f"Status order update to '{update.status}'"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)