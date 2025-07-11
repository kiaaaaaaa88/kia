from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from app.helper.helper import get_pg_connection
from app.utils.utils import only_admin

router = APIRouter(prefix="/barang", tags=["Barang"])

class BarangCreate(BaseModel):
    kode_barang: str = Field(..., min_length=4, description="Kode barang Min. 4 characters")
    nama_barang: str
    stock: int
    deskripsi: str = None

@router.post("", status_code=201, summary="Tambahkan barang")
def create_barang(
    barang: BarangCreate,
    username: str = Depends(only_admin) # Only admin
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        # Is kode_barang already exist?
        cur.execute("SELECT id FROM barang WHERE kode_barang = %s", (barang.kode_barang,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Kode barang sudah terdaftar")
        # Insert new barang
        cur.execute(
            "INSERT INTO barang (kode_barang, nama_barang, stock, deskripsi) VALUES (%s, %s, %s, %s) RETURNING id",
            (barang.kode_barang, barang.nama_barang, barang.stock, barang.deskripsi)
        )
        barang_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "Success",
            "message": "Barang added successfully!", 
            "barang_id": barang_id
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)