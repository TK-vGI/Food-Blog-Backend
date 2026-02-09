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


def create_stage2(conn):
    conn.execute("""
                CREATE TABLE IF NOT EXISTS recipes
                (
                    recipe_id          INTEGER PRIMARY KEY,
                    recipe_name        TEXT NOT NULL,
                    recipe_description TEXT
                );
                """)
    conn.commit()


def create_stage3(conn):
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS serve
                 (
                     serve_id  INTEGER PRIMARY KEY,
                     recipe_id INTEGER NOT NULL,
                     meal_id   INTEGER NOT NULL,
                     FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
                     FOREIGN KEY (meal_id) REFERENCES meals (meal_id)
                 );
                 """)
    conn.commit()


def add_recipe(conn, name, description, serving):
    cur = conn.cursor()

    # Insert recipe
    cur.execute("""
        INSERT INTO recipes (recipe_name, recipe_description)
        VALUES (?, ?);
    """, (name, description))

    recipe_id = cur.lastrowid  # get the new recipe's ID

    # Insert into serve table
    meal_ids = serving.split()  # e.g. "1 3 4" → ["1", "3", "4"]

    for meal_id in meal_ids:
        cur.execute("""
            INSERT INTO serve (recipe_id, meal_id)
            VALUES (?, ?);
        """, (recipe_id, int(meal_id)))

    conn.commit()


def prompt_for_recipe():
    recipe_name = input("Recipe name: ").strip()
    if recipe_name == "":
        return None  # signal to stop

    recipe_description = input("Recipe description: ").strip()
    recipe_serving = input(
        "1) breakfast  2) brunch  3) lunch  4) supper \n"
        "When the dish can be served: "
    ).strip()

    return recipe_name, recipe_description, recipe_serving


def main():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        create_stage1(conn, data)
        create_stage2(conn)
        create_stage3(conn)

        print("Pass the empty recipe name to exit.")

        while True:
            result = prompt_for_recipe()
            if result is None:
                break

            name, description, serving = result
            add_recipe(conn, name, description, serving)

    conn.close()



if __name__ == "__main__":
    main()