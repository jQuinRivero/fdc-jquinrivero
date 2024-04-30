import sqlite3  
from typing import Optional  
  
class DatabaseHandler:  
    def __init__(self, db_path: str):  
        self.db_path = db_path  
        self.conn = sqlite3.connect(self.db_path)  
        self.create_tables()  
  
    def create_tables(self):  
        try:  
            cursor = self.conn.cursor()  
            cursor.execute(  
                """    
                CREATE TABLE IF NOT EXISTS Stores (    
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT UNIQUE    
                )    
            """  
            )  
            cursor.execute(  
                """    
                CREATE TABLE IF NOT EXISTS Categories (    
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT UNIQUE    
                )    
            """  
            )  
            cursor.execute(  
                """    
                CREATE TABLE IF NOT EXISTS FigCategories (    
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT UNIQUE    
                )    
            """  
            )  
            cursor.execute(  
                """    
                CREATE TABLE IF NOT EXISTS Products (    
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    store_id INTEGER,    
                    category_id INTEGER,    
                    fig_category_id INTEGER,    
                    name TEXT,    
                    ingredients TEXT,    
                    allergens TEXT,    
                    picture_url TEXT,    
                    UNIQUE(store_id, name),    
                    FOREIGN KEY(store_id) REFERENCES Stores(id),    
                    FOREIGN KEY(category_id) REFERENCES Categories(id),    
                    FOREIGN KEY(fig_category_id) REFERENCES FigCategories(id)    
                )    
            """  
            )  
            self.conn.commit()  
        except Exception as e:  
            print(f"Error creating tables: {e}")  
  
    def upsert_store(self, store_name: str) -> int:  
        try:  
            cursor = self.conn.cursor()  
            cursor.execute(  
                """    
                INSERT INTO Stores (name)    
                VALUES (?)    
                ON CONFLICT(name) DO UPDATE SET    
                name = excluded.name    
            """,  
                (store_name,),  
            )  
            self.conn.commit()  
            return cursor.lastrowid  
        except Exception as e:  
            print(f"Error upserting store: {e}")  
            return -1  
  
    def upsert_category(self, category_name: str) -> int:  
        try:  
            cursor = self.conn.cursor()  
            cursor.execute(  
                """    
                INSERT INTO Categories (name)    
                VALUES (?)    
                ON CONFLICT(name) DO UPDATE SET    
                name = excluded.name    
            """,  
                (category_name,),  
            )  
            self.conn.commit()  
            return cursor.lastrowid  
        except Exception as e:  
            print(f"Error upserting category: {e}")  
            return -1  
  
    def upsert_fig_category(self, fig_category_name: Optional[str]) -> Optional[int]:  
        if fig_category_name is None:  
            return None  
        try:  
            cursor = self.conn.cursor()  
            cursor.execute(  
                """    
                INSERT INTO FigCategories (name)    
                VALUES (?)    
                ON CONFLICT(name) DO UPDATE SET    
                name = excluded.name    
            """,  
                (fig_category_name,),  
            )  
            self.conn.commit()  
            return cursor.lastrowid  
        except Exception as e:  
            print(f"Error upserting fig category: {e}")  
            return -1  
  
    def upsert_product(  
        self,  
        store_id: int,  
        category_id: int,  
        fig_category_id: Optional[int],  
        product_name: str,  
        ingredients: str,  
        allergens: str,  
        picture_url: str,  
    ) -> int:  
        try:  
            cursor = self.conn.cursor()  
            cursor.execute(  
                """    
                INSERT INTO Products (store_id, category_id, fig_category_id, name, ingredients, allergens, picture_url)    
                VALUES (?, ?, ?, ?, ?, ?, ?)    
                ON CONFLICT(store_id, name) DO UPDATE SET    
                category_id = excluded.category_id,    
                fig_category_id = excluded.fig_category_id,    
                ingredients = excluded.ingredients,    
                allergens = excluded.allergens,    
                picture_url = excluded.picture_url    
            """,  
                (  
                    store_id,  
                    category_id,  
                    fig_category_id,  
                    product_name,  
                    ingredients,  
                    allergens,  
                    picture_url,  
                ),  
            )  
            self.conn.commit()  
            return cursor.lastrowid  
        except Exception as e:  
            print(f"Error upserting product: {e}")  
            return -1  
        
    def get_store_id(self, store_name: str) -> Optional[int]:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT id FROM Stores WHERE name = ?", (store_name,))  
        result = cursor.fetchone()  
        return result[0] if result else None  
  
    def get_category_id(self, category_name: str) -> Optional[int]:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT id FROM Categories WHERE name = ?", (category_name,))  
        result = cursor.fetchone()  
        return result[0] if result else None  
  
    def get_fig_category_id(self, fig_category_name: str) -> Optional[int]:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT id FROM FigCategories WHERE name = ?", (fig_category_name,))  
        result = cursor.fetchone()  
        return result[0] if result else None  
  
    def count_stores(self) -> int:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT COUNT(*) FROM Stores")  
        return cursor.fetchone()[0]  
  
    def count_categories(self) -> int:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT COUNT(*) FROM Categories")  
        return cursor.fetchone()[0]  
  
    def count_fig_categories(self) -> int:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT COUNT(*) FROM FigCategories")  
        return cursor.fetchone()[0]  
  
    def count_products(self) -> int:  
        cursor = self.conn.cursor()  
        cursor.execute("SELECT COUNT(*) FROM Products")  
        return cursor.fetchone()[0]  
  
    def __del__(self):  
        self.conn.close()  
