import psycopg2
import pandas as pd

class Database:
    conn = None
    cur = None

    def __init__(self):
        self.conn = psycopg2.connect(
            user='postgres',
            password='124',
            database='postgres',
            host='localhost',
            port='5432'
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_df(self, table_name):
        query = f'SELECT * FROM "{table_name}";'
        self.cur.execute(query)
        records = self.cur.fetchall()
        colnames = [desc[0] for desc in self.cur.description]
        data = [dict(zip(colnames, record)) for record in records]
        return pd.DataFrame(data)
    
    def execute(self, query):
        self.cur.execute(query)

def main():
    db = Database()
    print(db.get_df("case"))
    db.close()

# Run the main function
if __name__ == "__main__":
    main()