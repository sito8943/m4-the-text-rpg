"""Character save stored in a SQLite database (game.db)."""

import json
import sqlite3

DB_FILE = "game.db"
TABLES = (
    """CREATE TABLE IF NOT EXISTS character (
        name TEXT NOT NULL, level INTEGER, hp INTEGER, mp INTEGER, xp INTEGER, gold INTEGER,
        cclass TEXT, weapon_name TEXT, weapon_damage INTEGER)""",
    """CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY, name TEXT, description TEXT, item_type TEXT, effect TEXT)""",
    """CREATE TABLE IF NOT EXISTS defeated_enemies (name TEXT PRIMARY KEY)""",
)

class DatabaseManager:
    """Saves and loads the character in a SQLite database."""

    def __init__(self, db_file=DB_FILE):
        """Stores the database file name. Tables are created on first use."""
        self.db_file = db_file

    def _connect(self):
        """Opens the database and creates the tables if they don't exist."""
        conn = sqlite3.connect(self.db_file)
        for table in TABLES:
            conn.execute(table)
        return conn

    def save_character(self, data):
        """Replaces the saved character with the dict made by Character.to_dict."""
        conn = self._connect()
        try:
            # cleaning previous data
            for table in ("character", "inventory", "defeated_enemies"):
                conn.execute(f"DELETE FROM {table}")
            conn.execute("INSERT INTO character VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (data["name"], data["level"], data["hp"], data["mp"], data["xp"], data["gold"],
                        json.dumps(data["cclass"]), data["weapon"]["name"], data["weapon"]["damage"]))
            for item in data["inventory"]["items"]:
                conn.execute(
                    "INSERT INTO inventory (name, description, item_type, effect) VALUES (?, ?, ?, ?)",
                    (item["name"], item["description"], item["item_type"], json.dumps(item["effect"])))
            for name in data["defeated_enemies"]:
                conn.execute("INSERT INTO defeated_enemies VALUES (?)", (name,))
            conn.commit()
        finally:
            conn.close()

    def load_character(self):
        """Returns the saved character as a dict for Character.from_dict, or None if there is no save."""
        conn = self._connect()
        try:
            row = conn.execute("SELECT * FROM character").fetchone()
            if row is None:
                return None
            items = conn.execute("SELECT name, description, item_type, effect FROM inventory ORDER BY id").fetchall()
            enemies = conn.execute("SELECT name FROM defeated_enemies").fetchall()
        finally:
            conn.close()
        name, level, hp, mp, xp, gold, cclass, weapon_name, weapon_damage = row
        return {
            "name": name, "level": level, "hp": hp, "mp": mp, "xp": xp, "gold": gold,
            "cclass": json.loads(cclass),
            "weapon": {"name": weapon_name, "damage": weapon_damage},
            "inventory": {"items": [
                {"name": n, "description": d, "item_type": t, "effect": json.loads(e)}
                for n, d, t, e in items]},
            "defeated_enemies": [enemy[0] for enemy in enemies],
        }
