import sqlite3

DB_NAME = "food_blog.db"
# DB_NAME = "C:/Users/tomas/PycharmProjects/Food Blog Backend/Food.db"

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

def create_stage1(conn, data):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meals(
            meal_id INTEGER PRIMARY KEY,
            meal_name TEXT UNIQUE NOT NULL
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingredients(
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT UNIQUE NOT NULL
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS measures(
            measure_id INTEGER PRIMARY KEY,
            measure_name TEXT UNIQUE
        );
    """)

    # Check if meals table already has data
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM meals;")
    if cur.fetchone()[0] == 0:
        # Only insert if empty
        for table, values in data.items():
            column = table[:-1] + "_name"
            conn.executemany(
                f"INSERT INTO {table} ({column}) VALUES (?);",
                [(v,) for v in values]
            )
        conn.commit()


def add_recipe(conn, name, description):
    conn.execute("""
        INSERT INTO recipes (recipe_name, recipe_description)
        VALUES (?, ?);
    """, (name, description))
    conn.commit()


def main():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        # Create database food_blog.db, tables
        create_stage1(conn, data)

        # Create table recipe
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS recipes
                    (
                        recipe_id          INTEGER PRIMARY KEY,
                        recipe_name        TEXT NOT NULL,
                        recipe_description TEXT
                    );
                    """)
        conn.commit()

        # Populate table
        while True:
            recipe_name = input("Recipe name: ").strip()
            if recipe_name == "":
                break

            recipe_description = input("Recipe description: ").strip()
            add_recipe(conn, recipe_name,recipe_description)

    conn.close()


if __name__ == "__main__":
    main()