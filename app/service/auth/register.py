from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.helper.helper import get_pg_connection, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserRegister(BaseModel):
    name: str # Just dummy
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    try: 
        conn = get_pg_connection()
        cur = conn.cursor()
        # Check username already exist?
        cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Username already registered")
        # Hash password
        hashed_pw = hash_password(user.password)
        # Insert new admin
        cur.execute(
            "INSERT INTO users (username, password, create_at) VALUES (%s, %s, NOW()) RETURNING id",
            (user.username, hashed_pw)
        )
        user_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()
        return {
            "message": "Register as admin Successful!", 
            "user_id": user_id
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Unexpected error
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )