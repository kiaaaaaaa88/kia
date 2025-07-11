from fastapi import APIRouter, Depends, HTTPException, status
from app.helper.helper import get_pg_connection
from app.utils.utils import only_admin

router = APIRouter(prefix="/barang", tags=["Barang"])

@router.delete("/{id}", summary="Hapus barang")
def delete_barang(id: int, username: str = Depends(only_admin)): # Only admin
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        # Ensure barang is exist!
        cur.execute("SELECT id FROM barang WHERE id = %s", (id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Barang not found!")
        # Delete barang
        cur.execute("DELETE FROM barang WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "Success",
            "message": "Barang deleted successfully!"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)