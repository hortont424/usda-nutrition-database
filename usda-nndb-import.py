import codecs
import os
import sqlite3

NNDB_PATH = "/Users/thorton/Downloads/sr28asc/"

database = sqlite3.connect("sr28.db")

def read_nndb_file(filename):
    with codecs.open(os.path.join(NNDB_PATH, filename), encoding='iso-8859-1') as source:
        for row in source.readlines():
            fields = [r.strip("~") for r in row.rstrip().split("^")]
            yield fields

def unknown_value_list(length):
    return ", ".join(["?"] * length)

def import_nndb_file(filename, tablename, fields, constraints=[]):
    data = read_nndb_file(filename)
    constraints = ", ".join(constraints)
    if constraints:
        constraints = ", " + constraints
    database.execute("CREATE TABLE " + tablename + "(" + ", ".join(fields) + constraints + ")")
    database.executemany("INSERT INTO " + tablename + " VALUES (" + unknown_value_list(len(fields)) + ")", data)

import_nndb_file("NUTR_DEF.txt", "nutrient",
    ["id INTEGER NOT NULL PRIMARY KEY",
     "unit TEXT",
     "infoods_tag TEXT",
     "name TEXT",
     "sigfigs TEXT",
     "sr_order TEXT"])

import_nndb_file("FOOD_DES.txt", "food",
    ["id INTEGER NOT NULL PRIMARY KEY",
     "food_group TEXT",
     "name TEXT",
     "short_name TEXT",
     "other_names TEXT",
     "manufacturer TEXT",
     "survey TEXT",
     "refuse_description TEXT",
     "refuse_percentage TEXT",
     "scientific_name TEXT",
     "nitrogen_factor TEXT",
     "protein_factor TEXT",
     "fat_factor TEXT",
     "carbohyrate_factor TEXT"])

import_nndb_file("NUT_DATA.txt", "nutritional_data",
    ["food_id INTEGER NOT NULL",
     "nutrient_id INTEGER NOT NULL",
     "amount_per_edible_hectogram REAL",
     "num_data_points INTEGER",
     "std_error REAL",
     "source_id TEXT",
     "derivation_id TEXT",
     "ref_ndb_no TEXT",
     "is_fortified TEXT",
     "num_studies INTEGER",
     "min REAL",
     "max REAL",
     "degrees_of_freedom INTEGER",
     "lower_error_bound REAL",
     "upper_error_bound REAL",
     "statistical_comments TEXT",
     "date_modified TEXT",
     "confidence_id TEXT"],
    ["PRIMARY KEY (food_id, nutrient_id)",
     "FOREIGN KEY (food_id) REFERENCES food(id)",
     "FOREIGN KEY (nutrient_id) REFERENCES nutrient(id)"])

import_nndb_file("WEIGHT.txt", "weight",
    ["food_id INTEGER NOT NULL",
     "id INTEGER NOT NULL",
     "amount REAL",
     "description TEXT",
     "weight_grams REAL",
     "num_data_points INTEGER",
     "std_error REAL"],
    ["PRIMARY KEY (food_id, id)",
     "FOREIGN KEY (food_id) REFERENCES food(id)"])

database.commit()
database.close()
