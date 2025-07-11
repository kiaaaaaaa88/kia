from fastapi import APIRouter, Depends, HTTPException
from app.helper.helper import get_pg_connection
from app.utils.utils import only_admin

router = APIRouter(prefix="/order", tags=["Order (admin)"])

@router.get("/user/{user_id}", summary="Mendapatkan data order dari user")
def get_orders_by_user(
    user_id: int,
    admin=Depends(only_admin) # Only admin
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.id, o.user_id, o.barang_id, b.kode_barang, b.nama_barang,
                   o.jumlah, o.tanggal_order, o.status
            FROM orders o
            JOIN barang b ON o.barang_id = b.id
            WHERE o.user_id = %s
            ORDER BY o.tanggal_order DESC
        """, (user_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return {
            "status": "Success",
            "data": results
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)