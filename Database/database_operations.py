import random
import sqlite3
import secrets
import hashlib
import time

DATABASE = R"B:\Computer Science and Engineering\PycharmIDE\MovieReviewV5\Database\database.db"


def generate_random_string(length=128):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(secrets.choice(characters) for _ in range(length))


def is_unique_salt(conn, salt):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE salt=?", (salt,))
    count = c.fetchone()[0]
    return count == 0


def generate_unique_salt(conn):
    while True:
        salt = generate_random_string()
        if is_unique_salt(conn, salt):
            return salt


def get_final_salt():
    conn = sqlite3.connect(DATABASE)
    unique_salt = generate_unique_salt(conn)
    conn.close()
    return unique_salt


def get_salted_password(salt, password):
    return salt + password + salt


def encode_sha256(salted_password):
    return hashlib.sha256(salted_password.encode("utf-8")).hexdigest()


def get_hashed_password(password):
    salt = get_final_salt()
    salted_password = get_salted_password(salt, password)
    hashed_password = encode_sha256(salted_password)
    return salt, hashed_password


def get_salt_from_username(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT salt FROM users WHERE username=?", (username,))
    salt = c.fetchone()[0]
    conn.close()
    return salt


def get_salted_password_from_username(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT salted_password FROM users WHERE username=?", (username,))
    salted_password = c.fetchone()[0]
    conn.close()
    return salted_password


def check_password(username, password):
    salt = get_salt_from_username(username)
    salted_password = get_salted_password_from_username(username)
    make_salted_password = get_salted_password(salt, password)
    hashed_password = encode_sha256(make_salted_password)

    if hashed_password == salted_password:
        return True
    else:
        return False


def insert_user(username, password, email):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        salt, hashed_password = get_hashed_password(password)

        c.execute("""
                INSERT INTO users (username, salt, salted_password, email)
                VALUES (?, ?, ?, ?)
            """, (username, salt, hashed_password, email))
        conn.commit()
        conn.close()

    except sqlite3.IntegrityError:
        return False


def is_username_exists(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    count = c.fetchone()[0]
    return count > 0


####################################################################################################


def print_hashed_password():
    print(get_hashed_password("password"))


def get_hashed_password_sample(pwd):
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()


def generate_movie_id():
    current_timestamp = int(time.time() * 1000)  # Convert to milliseconds
    random_number = random.randint(1000, 9999)  # Adjust the range as needed

    movie_id = int(f"{current_timestamp}{random_number}")

    return movie_id


def add_movie_details_to_database(title, json_data, summary_data, brief_data):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Check if the title already exists in the comments table
    c.execute("SELECT * FROM movies WHERE title=?", (title,))
    existing_title = c.fetchone()

    if existing_title is None:
        movie_id = generate_movie_id()
        # If the title doesn't exist, add the movie details to the comments table
        c.execute(
            "INSERT INTO movies (movie_id, movie_name, title, imdb, wiki_summary, wiki_detailed) VALUES (?, ?, ?, ?, ?, ?)",
            (movie_id, title, title, f"{json_data}", f"{summary_data}", f"{brief_data}"))

        conn.commit()
        conn.close()

        return "Movie details added successfully!"
    else:
        # If the title already exists, leave it
        conn.close()
        return "Movie details already exist."


######################################################################################################


def get_user_id(username):
    print("--Username: ", username)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        # Fetch the result
        result = c.fetchone()
        print("Result: ", result)

        if result:
            user_id = result[0]
            return user_id
        else:
            # Username not found
            return None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the cursor and connection
        c.close()
        conn.close()


def get_comments(user_id):
    list_of_comments = []
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        # Execute a SELECT query to fetch the desired columns based on the provided user_id
        c.execute("SELECT movie_id, created_at, content FROM comments WHERE user_id = ?", (user_id,))

        # Fetch all the results
        results = c.fetchall()

        # Display the results
        for result in results:
            movie_id, created_at, content = result
            list_of_comments.append([movie_id, created_at, content])
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the cursor and connection
        c.close()
        conn.close()

        return list_of_comments


def delete_comment_by_id_and_created_at(user_id, created_at):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        c.execute("DELETE FROM comments WHERE user_id = ? AND created_at = ?", (user_id, created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        c.close()
        conn.close()


def get_movies_and_movie_ids():
    list_of_movies = []
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    try:
        # Execute a SELECT query to fetch the desired columns
        c.execute("SELECT movie_id, title FROM movies")

        # Fetch all the results
        results = c.fetchall()

        for result in results:
            movie_id, title = result
            list_of_movies.append([movie_id, title])

        return list_of_movies

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the cursor and connection
        c.close()
        conn.close()
