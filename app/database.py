import psycopg2
from psycopg2.extras import RealDictCursor


try:
    conn = psycopg2.connect(host='localhost', database='fastapi_postgres', user='myuser', password='password', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DB connected")
except: 
    print("unseccesful")

