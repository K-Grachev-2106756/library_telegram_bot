from flask import send_file, Flask
import pandas as pd
import sqlalchemy as sql
import psycopg2
from os import getcwd
import getpass



USERNAME = getpass.getuser()
PORT = 5433

engine = sql.create_engine(f"postgresql+psycopg2://{USERNAME}:@localhost:{PORT}/")
connection = engine.connect()

metadata = sql.MetaData()
books = sql.Table('books', metadata)
borrows = sql.Table('borrows', metadata)

sql.inspect(engine).reflect_table(books, None)
sql.inspect(engine).reflect_table(borrows, None)

def book_stat(book_id:int):
    wd = getcwd()
    df = pd.read_sql(f'select borrow_id, book_id, date_start, date_end from borrows where book_id = {book_id}', con=connection)
    path = f'{wd}/files/{book_id}.csv'
    df.to_csv(path, index = False)

    return path

app = Flask(__name__)

@app.route("/download/<book_id>")
def download(book_id:int):
    return send_file(book_stat(book_id))




app.run("0.0.0.0", port=8080)






































#@app.route("/stores/<store_id>", methods = ['GET'])
#def store_information(store_id:int):
#    return f"<p>{store_info(store_id)}</p>"

#@app.route("/stores/add", methods = ['POST'])
#def add_store():
#    return add(flask.request)


