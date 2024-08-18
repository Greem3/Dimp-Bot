from NewSimpleSQL import Database, generate_id
import sqlite3

db: Database = Database(sqlite3.connect("Dimp_Data.db"))

def create_tables():
    
    db.complicated_create_tables(
        [
            {
                "name" : "Users",
                "columns" : {
                    "name" : str,
                    "id" : int,
                    "verified_problems_published" : int,
                    "unverified_problems_published" : int,
                    "verified_problems_resolved" : int,
                    "unverified_problems_resolved" : int,
                    "points" : int,
                    "easy_problems_resolved" : int,
                    "medium_problems_resolved" : int,
                    "hard_problems_resolved" : int,
                    "extreme_problems_resolved" : int,
                }
            },
            {
                "name" : "Problems",
                "columns" : {
                    "name" : str,
                    "id" : int,
                    "description" : str,
                    "solution" : str,
                    "publish_date" : str,
                    "total_solutions" : int,
                    "difficulty" : str
                }
            }
        ]
    )