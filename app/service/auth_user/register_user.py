from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.helper.helper import get_pg_connection, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserRegisterUser(BaseModel):
    name: str  # Dummy
    username: str
    password: str

@router.post("/register-user")
def register_user(user: UserRegisterUser):
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
        # Insert new user, lock role as 'user'
        cur.execute(
            "INSERT INTO users (username, password, role, create_at) VALUES (%s, %s, %s, NOW()) RETURNING id",
            (user.username, hashed_pw, "user")
        )
        user_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()
        return {
            "message": "Register as user successful!", 
            "user_id": user_id
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")