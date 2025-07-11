from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.helper.helper import get_pg_connection
from app.utils.utils import only_admin

class BarangUpdate(BaseModel):
    kode_barang: str = Field(None, min_length=4)
    nama_barang: str = None
    stock: int = None
    deskripsi: str = None

router = APIRouter(prefix="/barang", tags=["Barang"])

@router.patch("/{id}", summary="Update data barang")
def update_barang(
    id: int,
    barang: BarangUpdate,
    username: str = Depends(only_admin)  # Only admin
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
          # Is barang already exist?
        cur.execute("SELECT id FROM barang WHERE id = %s", (id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
        
        # Prepare updated fields
        fields = []
        values = []
        if barang.kode_barang is not None:
            fields.append("kode_barang = %s")
            values.append(barang.kode_barang)
        if barang.nama_barang is not None:
            fields.append("nama_barang = %s")
            values.append(barang.nama_barang)
        if barang.stock is not None:
            fields.append("stock = %s")
            values.append(barang.stock)
        if barang.deskripsi is not None:
            fields.append("deskripsi = %s")
            values.append(barang.deskripsi)

        if not fields:
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Tidak ada data untuk diupdate")

        # Update query
        query = f"UPDATE barang SET {', '.join(fields)} WHERE id = %s"
        values.append(id)
        cur.execute(query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
        return {
            "status": "Success",
            "message": "Barang updated successfully!"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500)