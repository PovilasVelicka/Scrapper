from interfaces import repository as repo
import sqlite3
from typing import Optional


class SqlRepository(repo.IDataAccessRepository):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()


    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                price TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_details (
                product_id TEXT,
                key TEXT,
                value TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
        """)
        self.conn.commit()


    def get_first_or_default(self, id_keys: dict[str, str | int]) -> Optional[dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (id_keys["id"],))
        row = cursor.fetchone()
        if row:
            product = {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
            cursor.execute("SELECT key, value FROM product_details WHERE product_id = ?", (row[0],))
            details = [{key: value} for key, value in cursor.fetchall()]
            product["details"] = details
            return product
        return None


    def update(self, new_item: dict, id_keys: dict[str, str | int]) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, description = ?, price = ?
            WHERE id = ?
        """, (new_item["name"], new_item["description"], new_item["price"], id_keys["id"]))

        # Clear and re-insert details
        cursor.execute("DELETE FROM product_details WHERE product_id = ?", (id_keys["id"],))
        for detail in new_item.get("details", []):
            for key, value in detail.items():
                cursor.execute("""
                    INSERT INTO product_details (product_id, key, value)
                    VALUES (?, ?, ?)
                """, (id_keys["id"], key, value))

        self.conn.commit()
        return new_item


    def insert(self, item: dict) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO products (id, name, description, price)
            VALUES (?, ?, ?, ?)
        """, (item["id"], item["name"], item["description"], item["price"]))

        for detail in item.get("details", []):
            for key, value in detail.items():
                cursor.execute("""
                    INSERT INTO product_details (product_id, key, value)
                    VALUES (?, ?, ?)
                """, (item["id"], key, value))

        self.conn.commit()
        return item