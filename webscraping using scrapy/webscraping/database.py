import sqlite3
con = sqlite3.connect("amazon.db")
cur = con.cursor()
cur.execute("""
            create table amazon (
                image_path text,
                product_name text,
                product_price text,
                ratings text   
            )
            """)

con.commit()
con.close()