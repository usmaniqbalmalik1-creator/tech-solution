import sqlite3
conn=sqlite3.connect("analytics.db")
conn.executescript("""
CREATE TABLE IF NOT EXISTS sales(
id INTEGER PRIMARY KEY, customer TEXT, product TEXT,
category TEXT, quantity INTEGER, revenue REAL, month TEXT);
DELETE FROM sales;
""")
rows=[("Ali","Laptop","Electronics",2,1800,"2026-01"),("Sara","Phone","Electronics",4,2400,"2026-01"),("Hamza","Desk","Furniture",3,900,"2026-02"),("Ayesha","Phone","Electronics",2,1200,"2026-02"),("Bilal","Chair","Furniture",8,800,"2026-03"),("Hina","Laptop","Electronics",1,900,"2026-03")]
conn.executemany("INSERT INTO sales(customer,product,category,quantity,revenue,month) VALUES(?,?,?,?,?,?)",rows)
conn.commit(); conn.close(); print("Created analytics.db")