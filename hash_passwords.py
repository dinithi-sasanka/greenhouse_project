from utils.db import get_connection
from werkzeug.security import generate_password_hash

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT id, password FROM users")
users = cur.fetchall()

for user_id, plain_pwd in users:
    
    if plain_pwd.startswith("pbkdf2:sha256:"):
        continue
    hashed = generate_password_hash(plain_pwd)
    cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))
    print(f"Password re-hashed for user ID {user_id}")

conn.commit()
cur.close()
conn.close()
print("All passwords re-hashed using Werkzeug!")
