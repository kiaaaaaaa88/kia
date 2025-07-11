from app.helper.helper import get_pg_conection

def test_pg_conection():
    try:
        conn = get_pg_conection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        print("conection to postgreSQL succesful!")
        return True
    except Exception as e:
        print(f"conection to postgreSQL failed: {e}")
        return False
    
if __name__ == "__main__":
    test_pg_conection()

