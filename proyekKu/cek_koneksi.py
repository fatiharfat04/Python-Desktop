from database import koneksi
with koneksi() as db:
    with db.cursor() as cur:
        cur.execute("SELECT DATABASE(), VERSION()")
        print(cur.fetchone())