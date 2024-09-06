from NewSimpleSQL.SimpleSQLite import Database, ID, generate_id
import sqlite3
from sqlite3 import Blob
import marshal

db: Database = Database(sqlite3_connection=sqlite3.connect("database/Dimp_Data.db"))

def NewDatabase(db_url: str):
    db: Database = Database(sqlite3_connection=db_url)

def create_tables():
    
    db.complicated_create_tables(
        [
            {
                "name" : "Users",
                "columns" : {
                    "id" : ID(auto_increment=False),
                    "description" : [str, "Hello! I'm a new user"],
                    "create_date" : (str,),
                    "verified_problems_published" : [int, 0],
                    "unverified_problems_published" : [int, 0],
                    "verified_problems_resolved" : [int, 0],
                    "unverified_problems_resolved" : [int, 0],
                    "points" : [int, 0],
                    "easy_problems_resolved" : [int, 0],
                    "medium_problems_resolved" : [int, 0],
                    "hard_problems_resolved" : [int, 0],
                    "extreme_problems_resolved" : [int, 0]
                }
            },
            {
                "name" : "Problems",
                "columns" : {
                    "id" : ID(),
                    "author_id" : (int,),
                    "name" : (str,),
                    "description" : (str,),
                    "type" : (str,),
                    "publish_date" : (str,),
                    "edited_date" : [str, None],
                    "difficulty" : [str, None],
                    "solution" : [str, None],
                    "verified" : [int, False]
                },
                "fk" : {
                    "author_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "Solutions",
                "columns" : {
                    "id" : (int,),
                    "problem_id" : (int,),
                    "author_id" : (int,),
                    "description" : (str,),
                    "publish_date" : (str,)
                },
                "composite" : ["id", "problem_id"],
                "fk" : {
                    "problem_id" : ("Problems", "id", True),
                    "author_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "Users_difficulty",
                "columns" : {
                    "user_id" : (int,),
                    "problem_id" : (int,),
                    "vote" : (int,) # Votan que dificultad es el problema
                },
                "composite" : ["user_id", "problem_id"],
                "fk" : {
                    "user_id" : ("Users", "id", True),
                    "problem_id" : ("Problems", "id", True)
                }
            },
            {
                "name" : "Users_votes",
                "columns" : {
                    "user_id" : (int,),
                    "solution_id" : (int,),
                    "vote" : (int,) # Votan si la solucion es valida o no
                },
                "composite" : ["user_id", "solution_id"],
                "fk" : {
                    "user_id" : ("Users", "id", True),
                    "solution_id" : ("Solutions", "id", True)
                }
            },
            {
                "name" : "cn_accounts",
                "columns" : {
                    "user_id" : ID(auto_increment=False),
                    "achievements" : Blob,
                    "created_date" : (str,),
                    "money" : [int, 0],
                    "games_played" : [int, 0],
                    "games_won" : [int, 0],
                    "max_difficulty_played" : str,
                    "max_round_played" : [int, 0]
                },
                "fk" : {
                    "user_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "games_saves",
                "columns" : {
                    "id" : ID(),
                    "user_id" : (int,),
                    "game_name" : [str, "cn"],
                    "game_info" : (Blob,)
                },
                "fk" : {
                    "user_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "tf_accounts",
                "columns" : {
                    "user_id" : ID(auto_increment=False),
                    "games_played" : [int, 0],
                    "games_won" : [int, 0],
                    "correct_twenty_four" : [int, 0]
                },
                "fk" : {
                    "user_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "administrators",
                "columns" : {
                    "user_id" : ID(auto_increment=False),
                    "agregate_date" : (str,),
                    "super_admin" : [int, 0]
                },
                "fk" : {
                    "user_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "banned_users",
                "columns" : {
                    "user_id" : ID(auto_increment=False),
                    "ban_date" : (str,),
                    "unban_date" : [str, None]
                },
                "fk" : {
                    "user_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "clubs",
                "columns" : {
                    "id" : ID(),
                    "name" : (str,),
                    "description" : [str, "A new club"],
                    "create_date" : (str,),
                    "creator_id" : (int,),
                    "joined_users" : [int, 0],
                    "users" : (Blob,),
                    "image" : Blob
                },
                "fk" : {
                    "creator_id" : ("Users", "id", True)
                }
            },
            {
                "name" : "tasks",
                "columns" : {
                    "id" : ID(),
                    "club_id" : (int,),
                    "author_id" : (int,),
                    "name" : (str,),
                    "description" : (str,),
                    "created_date" : (str,),
                    "end_date" : [str, None]
                }
            }
        ]
    )
    
def SearchBy(table: str, columns: str, value: str|int, id_name_column_name: tuple[str] = ("id", "name")):
    """
    Use this command for search a value with the id or name
    """
    
    if value.isnumeric():
        value = int(value)
        return db.simple_select_data(table, columns, f'WHERE {id_name_column_name[0]} = {value}', True)
    
    return db.simple_select_data(table, columns, f'WHERE {id_name_column_name[1]} = "{value}"', True)
    
def add_super_admin():
    from datetime import datetime
    db.simple_insert_data("administrators", (
        427319348831453186,
        datetime.now().date(),
        True
    ))