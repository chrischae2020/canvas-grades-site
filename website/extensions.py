from pymongo import MongoClient

cluster = MongoClient("EXAMPLE_DB")
db = cluster['mydb']