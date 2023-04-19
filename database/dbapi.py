from .models import *
from sqlalchemy import MetaData, select, desc, insert, update, func, text, and_, or_
from datetime import datetime
import getpass



#USERNAME = getpass.getuser()
#PORT = 5433

class DatabaseConnector:
    
    def __init__(self, USERNAME, PORT):
            self.engine = create_engine(f"postgresql+psycopg2://{USERNAME}:@localhost:{PORT}")
        
    def add(self, title, author, published):
        connection = self.engine.connect()
        insertion = insert(Book).values(
            title=title, 
            author=author, 
            published=published, 
            date_added = datetime.today()
        )
        res = connection.execute(insertion)
        if res:
            connection.commit()
            return int(res.inserted_primary_key[0])
        return False

    def delete(self, id):
        connection = self.engine.connect()
        find = select(Book).join(Borrow, Borrow.book_id == Book.book_id, isouter = True).where(and_(Book.book_id == id, or_(Borrow.date_start is None, Borrow.date_end.is_(None))))
        find = connection.execute(find).all()
        if find:
            upd = update(Book).values(date_deleted = datetime.today()).where(Book.book_id == id)
            res = connection.execute(upd)
            print(res)
            if res:
                connection.commit()
                return True
            return False
        return False

    def list_books(self):
        connection = self.engine.connect()
        all = select(Book)
        res = connection.execute(all).all()
        if res:
            return res
        return False

    def get_book(self, title, author, year):
        connection = self.engine.connect()
        book = select(Book).where(and_(func.lower(Book.title) == func.lower(title), and_(func.lower(Book.author) == func.lower(author), Book.published == year)))
        res = connection.execute(book).all()
        return res

    def borrow(self, book_id, user_id):
        connection = self.engine.connect()
    
        check_bor = select(Borrow).where(Borrow.book_id == book_id).order_by(desc(Borrow.date_start)).limit(1)
        bor_check_list = connection.execute(check_bor).fetchall()

        query = f'select * from borrows where user_id = {user_id} and date_end is null'
        check_user = text(query)
        user_check_list = connection.execute(check_user).fetchall()

        if((len(bor_check_list) == 0 or bor_check_list[0][3]!=None) and (len(user_check_list) == 0)):
            insertion = insert(Borrow).values(
                book_id = book_id, 
                date_start = datetime.today(),
                user_id = user_id
            )
            connection.execute(insertion)
            connection.commit()
            return True
        return False

    def get_borrow(self, user_id):
        connection = self.engine.connect()
    
        check = select(Borrow).where(Borrow.user_id == user_id).order_by(desc(Borrow.date_start)).limit(1)
        check_list = connection.execute(check).fetchall()

        if(len(check_list) == 0):
            return None
        return check_list
    
    def retrieve(self, user_id):
        connection = self.engine.connect()
        borrow = self.get_borrow(user_id)
        
        if borrow == None or borrow[0][3] != None:
            return False

        upd = update(Borrow).values(date_end = datetime.today()).where(Borrow.user_id == user_id)
        res = connection.execute(upd)
        connection.commit()
        
        book = connection.execute(select(Borrow).where(Borrow.user_id == user_id).order_by(Borrow.date_end, desc(Borrow.borrow_id)).limit(1)).fetchall()
        book_id = book[0][1]
        str = connection.execute(select(Book).where(Book.book_id == book_id)).fetchall()
        return f'{str[0][1]} {str[0][2]} {str[0][3]}' 

#print(DatabaseConnector().add('green', 'A.Green', 1234))
#print(DatabaseConnector.borrow(2, 1001))

#print(DatabaseConnector().get_borrow(1001))


#print(DatabaseConnector().retrieve(1001))