from dataclasses import dataclass


@dataclass
class DBData:
    db_info = {"host": 'localhost',
               "port": 3306,
               "user": 'root',
               "password": 'root',
               "db": 'tg_farm',
               "autocommit": True
               }
