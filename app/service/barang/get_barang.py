from fastapi import APIRouter, Depends, HTTPException, Query
from app.helper.helper import get_pg_connection
from app.utils.utils import get_current_user

router = APIRouter(prefix="/barang", tags=["Barang"])

@router.get("", summary="Mendapatkan data semua barang (auth admin & user)")
def get_all_barang(
    q: str = Query(None, description="Keyword searching"),
    username: str = Depends(get_current_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        if q:
            # Searching LIKE (case-insensitive)
            search_pattern = f"%{q}%"
            cur.execute(
                """
                SELECT id, kode_barang, nama_barang, stock, deskripsi
                FROM barang
                WHERE LOWER(kode_barang) LIKE LOWER(%s)
                   OR LOWER(nama_barang) LIKE LOWER(%s)
                """,
                (search_pattern, search_pattern)
            )
        else:
            cur.execute("SELECT id, kode_barang, nama_barang, stock, deskripsi FROM barang")
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