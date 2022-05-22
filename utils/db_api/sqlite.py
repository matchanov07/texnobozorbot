from email.mime import image
import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_praduct_table(self):
        sql = """
        CREATE TABLE Product(
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image TEXT NOT NULL,
            date DATETIME NOT NULL,
            cat_id INTEGER NOT NULL
        );
        """
        self.execute(sql, commit=True)
    
    def create_category_table(self):
        sql = """
        CREATE TABLE Category(
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_catr_table(self):
        sql = """
        CREATE TABLE Catr(
            id INTEGER PRIMARY KEY,
            tg_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            amuount INTEGER NOT NULL
        );
        """
        self.execute(sql, commit=True)        

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def add_category_title(self, title: str):
        sql = """
        INSERT INTO Category(title) VALUES(?);
        """
        self.execute(sql, parameters=(title, ), commit=True)

    def add_products(self, title, description, price, image, date, cat_id):
        
        sql = """
        INSERT INTO Product(title, description, price, image, date, cat_id) VALUES(?,?,?,?,?,?);
        """
        self.execute(sql, parameters=(title, description, price, image, date, cat_id), commit=True)

    def add_product_cart(self, tg_id: int, title: str, price: int, amuount: int):
        sql = "SELECT * FROM Catr WHERE tg_id=? AND title=?"
        data = self.execute(sql, parameters=(tg_id,title), fetchone=True)
        print(data)
        if data:
            sql = "Update Catr SET amuount=? where id=?"
            self.execute(sql, parameters=((int(data[4])+ int(amuount), int(data[0]))), commit=True)
        else:
            sql = """
            INSERT INTO Catr(tg_id, title, price, amuount) VALUES(?, ?, ?, ?);
            """
            self.execute(sql, parameters=(tg_id, title, price, amuount), commit=True)
            


    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_cats(self):
        sql = """
        SELECT * FROM Category
        """
        return self.execute(sql, fetchall=True)
    
    def select_all_prods(self):
        sql = """
        SELECT * FROM Product
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
      
    def get_current_products(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Catr WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)
    
    def delete_current_products(self, **kwargs):
        sql = "DELETE FROM Catr WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, commit=True)


    def product_by_cat_id(self, **kwargs):
        sql = "SELECT id FROM Category WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        cat_id = self.execute(sql, parameters=parameters, fetchone=True)
        return cat_id[0]

    def get_praduct_cat_id(self, **kwargs):
        sql = "SELECT title FROM Product WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)


    def get_product_title_id(self, **kwargs):
        sql = "SELECT * FROM Product WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_cart(self):
        self.execute("DELETE FROM Catr WHERE TRUE", commit=True)   

    def delete_products(self, tg_id):
        sql = "DELETE FROM Catr WHERE tg_id=?"
        self.execute(sql, (tg_id, ), commit=True)

def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
