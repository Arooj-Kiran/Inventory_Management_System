import sqlite3
import os

def create_db():
    db_path = os.path.abspath("ims.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    


    

    # Create employee table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employee(EmpID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name text,
        Email text,
        Gender text,
        ContactNo text,
        DOB text,
        DOJ text,
        Password text,
        UserType text,
        Address text,
        Salary text
    )
    """)
    con.commit()

    #  Create supplier table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS supplier(
        invoice INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        desc TEXT
    )
    """)
    con.commit()
  
    #  Create category table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS category(
    cid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)

""")
    con.commit()
    
 #  Create product table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS product(
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        Category TEXT,
        Supplier TEXT,
        name TEXT,
        price TEXT,
        qty TEXT,
        status TEXT
    )
    """)

    

    con.commit()
    con.close()
    print("Database and tables created successfully!")


create_db()

#===============