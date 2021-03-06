import sqlite3

"""Класс для подключения к БД (для разнообразия)"""
class DBconnect:
    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()


"""Фунункция создания подключения и возврата результата по переданному запросу"""
def executing_db_query(query):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


# поиск по названию
# def movie_by_title(title):
#     db_connect = DBconnect('netflix.db')
#     query = f"""
#             SELECT title, country, release_year, listed_in, description
#             FROM netflix
#             WHERE title
#             LIKE '%{title}%'
#             ORDER BY release_year DESC
#             LIMIT 1
#             """
#     db_connect.cursor.execute(query)
#     result = db_connect.cursor.fetchall()
#     return {
#         "title": result[0],
#         "country": result[1],
#         "release_year": result[2],
#         "listed_in": result[3],
#         "description": result[4].replace('\n', '')
#     }

# поиск по названию
def movie_by_title(title):
    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title
            LIKE '%{title}%'
            ORDER BY release_year DESC
            LIMIT 1
            """
    result = executing_db_query(query)
    if not result:
        return "Фильм с такиим названием не найден"
    return {
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "listed_in": result[0][3],
        "description": result[0][4].replace('\n', '')
    }


# поиск по диапазону лет выпуска
def movies_by_years(year1, year2):
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year1} AND {year2}
            LIMIT 100
            """
    result = executing_db_query(query)
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0], "release_year": movie[1]})
    return result_list

# поиск по рейтингу
def movies_by_rating(category):
    rating_param = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R','NC-17'"
    }
    if category not in rating_param:
        return "Переданной группы не существует"
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({rating_param[category]})
            """
    result = executing_db_query(query)
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0], "rating": movie[1], "description": movie[2].replace('\n', '')})
    return result_list

# поиск по жанру (10 самых свежих фильмов)
def movies_by_genre(genre):
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
            """
    result = executing_db_query(query)
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0], "description": movie[1].replace('\n', '')})
    if not result_list:
        return "Такого жанра не найдено"
    return result_list

# для 2 актеров возвращает список тех, кто играет с ними в паре больше 2 раз
def partners_more_than_two_films(actor1, actor2):
    query = f"""
            SELECT netflix.cast
            FROM netflix
            WHERE netflix.cast LIKE '%{actor1}%' AND netflix.cast LIKE '%{actor2}%'
            """
    result = executing_db_query(query)
    actors_list = []
    for movie in result:
        actors = movie[0].split(', ')
        for actor in actors:
            actors_list.append(actor)
    result_list = []
    for actor in actors_list:
        if actor != actor1 and actor != actor2 and actors_list.count(actor) > 2:
            result_list.append(actor)
    return set(result_list)

# возвращает список названий по типу картины, году выпуска и жанру
def movies_by_type_year_genre(typ, year, genre):
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE type LIKE '{typ}'
            AND release_year LIKE '{year}'
            AND listed_in LIKE '%{genre}%'
            """
    result = executing_db_query(query)
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0], "description": movie[1].replace('\n', '')})
    return result_list
