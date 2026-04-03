import psycopg2
from connectt import connect

conn = connect()
cur = conn.cursor()

cur.execute("SELECT * FROM search_contacts(%s);", ("ali",))
print(cur.fetchall())


cur.execute("CALL upsert_contact(%s, %s);", ("Ali", "123456789"))

conn.commit()
cur.close()
conn.close()