import sqlite3


class DBconnect:
    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()


def get_by_title(title):
    db_connect = DBconnect('netflix.db')
    db_connect.cursor.execute(f"""
                              SELECT title, country, release_year, listed_in, description
                              FROM netflix
                              WHERE title
                              LIKE '%{title}%'
                              ORDER BY release_year DESC
                              LIMIT 1
                              """)
    result = db_connect.cursor.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "listed_in": result[3],
        "description": result[4].replace('\n', '')
    }

# print(get_by_title("100"))
