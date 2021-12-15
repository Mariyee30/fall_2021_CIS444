import psycopg2


def get_db():
    return psycopg2.connect(host="localhost", dbname="minecraft" , user="m_user", password="m_password")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 
