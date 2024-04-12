import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        salt TEXT NOT NULL,
        salted_password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create movies table
    c.execute("""CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY,
        movie_name TEXT UNIQUE NOT NULL,
        title TEXT UNIQUE NOT NULL,
        imdb TEXT NOT NULL,
        wiki_summary TEXT DEFAULT '',
        wiki_detailed TEXT DEFAULT ''
    )""")

    # Create comments table
    c.execute("""CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        content TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )""")

    conn.commit()
    conn.close()


def delete_all_from_a_table(table_name):
    conn = sqlite3.connect(r"B:\Computer Science and Engineering\PycharmIDE\MovieReviewV5\Database\database.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM {table_name}",)
    conn.commit()
    conn.close()

delete_all_from_a_table('movies')


# alter table movies to add likes and dislikes column

# def add():
#     conn = sqlite3.connect(r"B:\Computer Science and Engineering\PycharmIDE\MovieReviewV5\Database\database.db")
#     c = conn.cursor()
#     c.execute("ALTER TABLE movies DROP likes ")
#     c.execute("ALTER TABLE movies DROP dislikes ")
#     conn.commit()
#     conn.close()
#
# add()

# create a new table likes where the primary key is a combination of username and movie_id
# def create_likes():
#     conn = sqlite3.connect(r"B:\Computer Science and Engineering\PycharmIDE\MovieReviewV5\Database\database.db")
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS likes (
#                     username TEXT,
#                     movie_id INTEGER,
#                     FOREIGN KEY (username) REFERENCES users(username),
#                     FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
#                     PRIMARY KEY (username, movie_id)
#                 )''')
#
#     c.execute('''CREATE TABLE IF NOT EXISTS dislikes (
#                     username TEXT,
#                     movie_id INTEGER,
#                     FOREIGN KEY (username) REFERENCES users(username),
#                     FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
#                     PRIMARY KEY (username, movie_id)
#                 )''')
#
#     conn.commit()
#     conn.close()
#
#
# create_likes()

