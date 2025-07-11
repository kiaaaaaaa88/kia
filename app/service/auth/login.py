from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.helper.helper import get_pg_connection, verify_password
from app.utils.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    db_user = cur.fetchone()
    cur.close()
    conn.close()

    # Check user available & verification password
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password invalid")

    # Generate JWT token
    token = create_access_token(
        data={
            "sub": user.username,
            "role": db_user["role"],
            "user_id": db_user["id"]
        }
    )

    return {
        "status": "Success",
        "access_token": token
    }