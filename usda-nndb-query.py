import codecs
import os
import sqlite3

NNDB_PATH = "/Users/thorton/Downloads/sr28asc/"

database = sqlite3.connect("sr28.db")

for row in database.execute("SELECT food.name, nutrient.name, nutrient.unit, nutritional_data.amount_per_edible_hectogram FROM nutritional_data INNER JOIN nutrient ON nutritional_data.nutrient_id=nutrient.id INNER JOIN food on nutritional_data.food_id=food.id WHERE food.name='Restaurant, family style, fried mozzarella sticks'"):
    food, nutrient, unit, amount_per_edible_hectogram = row
    print food, nutrient, amount_per_edible_hectogram, unit

print "\n\n\n\n\n\n"

for row in database.execute("SELECT food.name, nutrient.name, nutrient.unit, nutritional_data.amount_per_edible_hectogram FROM nutritional_data INNER JOIN nutrient ON nutritional_data.nutrient_id=nutrient.id INNER JOIN food on nutritional_data.food_id=food.id WHERE nutrient.name='Caffeine' ORDER BY nutritional_data.amount_per_edible_hectogram"):
    food, nutrient, unit, amount_per_edible_hectogram = row
    print food, amount_per_edible_hectogram, unit
