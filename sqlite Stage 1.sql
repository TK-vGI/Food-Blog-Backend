CREATE TABLE IF NOT EXISTS  meals (
    meal_id INTEGER PRIMARY KEY,
    meal_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS  "ingredients" (
    ingredient_id INTEGER PRIMARY KEY,
    ingredient_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS measures (
    measure_id INTEGER PRIMARY KEY,
    measure_name TEXT UNIQUE
);

INSERT INTO meals (meal_id,meal_name) VALUES
            (1, 'breakfast'),
            (2,'brunch'),
            (3,'lunch'),
            (4,'supper');

INSERT INTO ingredients (ingredient_name) VALUES
            ('milk'),
            ('cacao'),
            ('strawberry'),
            ('blueberry'),
            ('blackberry'),
            ('sugar');

INSERT INTO measures (measure_name) VALUES
            ('ml'),
            ('g'),
            ('l'),
            ('cup'),
            ('tbsp'),
            ('tsp'),
            ('dsp'),
            ('');
