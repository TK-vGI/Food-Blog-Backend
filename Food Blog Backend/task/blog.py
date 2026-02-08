import sqlite3

DB_NAME = "food_blog.db"

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Create table p
cur.execute("CREATE TABLE IF NOT EXISTS meals("
            "meal_id INT PRIMARY KEY,"
            "meal_name TEXT UNIQUE NOT NULL);")

cur.execute("CREATE TABLE IF NOT EXISTS ingredients("
            "ingredient_id INT PRIMARY KEY,"
            "ingredient_name TEXT UNIQUE NOT NULL);")

cur.execute("CREATE TABLE IF NOT EXISTS measures("
            "measure_id INT PRIMARY KEY,"
            "measure_name TEXT UNIQUE);")


for table, values in data.items():
    column = table[:-1] + "_name"   # meals → meal_name
    cur.executemany(
        f"INSERT INTO {table} ({column}) VALUES (?);",
        [(v,) for v in values]
    )

# # meals
# cur.executemany(
#     "INSERT INTO meals (meal_name) VALUES (?);",
#     [(meal,) for meal in data["meals"]]
# )
#
# # ingredients
# cur.executemany(
#     "INSERT INTO ingredients (ingredient_name) VALUES (?);",
#     [(ingredient,) for ingredient in data["ingredients"]]
# )
#
# # measures
# cur.executemany(
#     "INSERT INTO measures (measure_name) VALUES (?);",
#     [(measure,) for measure in data["measures"]]
# )



conn.commit()
conn.close()
