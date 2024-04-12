from functools import partial

from flask import Flask, render_template, request, jsonify

from Database.database_operations import is_username_exists, add_movie_details_to_database, get_user_id, get_comments, \
    delete_comment_by_id_and_created_at, get_movies_and_movie_ids
import sqlite3

from algorithm.nltk.strings import modify_review
from requests.exceptions import ConnectionError

app = Flask(__name__)

DATABASE = r"B:\Computer Science and Engineering\PycharmIDE\MovieReviewV5\Database\database.db"


@app.route('/', methods=['GET', 'POST'])
def start():
    app.jinja_env.cache = {}
    return render_template('Default_Page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('Login_Page.html')


@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    from Database.database_operations import insert_user
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print(username, email, password)

    check_insertion = insert_user(username, password, email)

    if check_insertion is False:
        return "Email already exists\nPlease try again"
    return "User created successfully"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('Signup_Page.html')


@app.route('/home-page', methods=['GET', 'POST'])
def login_get_details():
    username = request.form.get('username')

    print(username)

    username_exists = is_username_exists(username)
    print(username_exists)

    if username_exists is False:
        return render_template('No_User_Exists_Page.html')

    from Database.database_operations import check_password
    password = request.form.get('password')
    print("Password: ", password)

    password_check = check_password(username, password)
    print("password_check", password_check)

    if password_check is False:
        return render_template('Wrong_Password_Page.html')

    print(username)
    return render_template('Movie_Page.html', username=username)


# Define a route for handling POST requests to '/process_input'
@app.route('/process_input', methods=['POST'])
def process_input():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Extract 'input' key from the JSON data, default to an empty string if not present
    input_value = data.get('input', '')

    if input_value == '':
        return jsonify({"Data": "Please enter a movie name :)", "Summary": "", "Brief": "", "Image": "", "Title": ""})

    print("Use TMDB here")
    print("Input: ", input_value)
    print("Here")

    from algorithm.tmdb.scrap_data import scrap_data

    dict_ = scrap_data(input_value)

    print("dict_: ", dict_)

    print("Title: ", dict_['title'])

    string = (f"{dict_['title']}\n"
              f"{dict_['certification']}\n"
              f"{dict_['description']}\n"
              f"{dict_['genre']}\n\n"
              f"Rating: {dict_['rating']}/100\n"
              f"{dict_['profile']}\n")

    print(type(dict_['cast']), type(dict_['alt']))

    cast_ = []
    for i in range(len(dict_['cast'])):
        cast_.append([dict_['cast'][i], dict_['alt'][i]])

    print(cast_)

    print(string)

    add_movie_details_to_database(dict_['title'], "", "", "")

    return jsonify(
        {"Data": string, "Summary": "", "Brief": "", "Image": dict_['image'], "Title": dict_['title'], "cast": cast_})


@app.route("/submit-review", methods=["GET", "POST"])
def submit_review():
    data = request.get_json()
    title = data['title']
    review = data['review']
    username = data['username']

    if len(review) == 0:
        print("Review is empty!")
        return jsonify({"message": "Review is empty!"})

    review = modify_review(review)
    print(title, review)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    existing_title = c.fetchone()

    if existing_title is not None:
        conn2 = sqlite3.connect(DATABASE)
        c2 = conn2.cursor()

        conn3 = sqlite3.connect(DATABASE)
        c3 = conn3.cursor()
        c3.execute("SELECT id FROM users WHERE username=?", (username,))
        get_user_id = c3.fetchone()[0]

        c2.execute("INSERT INTO comments (user_id, movie_id, content) VALUES (?, ?, ?)",
                   (get_user_id, existing_title[0], review))

        c2.close()
        conn2.commit()
        conn2.close()

        c3.close()
        conn3.commit()
        conn3.close()
        pass

    else:
        return jsonify({"message": "Movie not found!"})

    return jsonify({"message": "Review submitted successfully!"})


@app.route('/load-data', methods=["GET", "POST"])
def load_data():
    data = request.get_json()
    title = data.get('title')

    if len(title) == 0:
        return jsonify({"comments": ["Empty title!"]})

    print("Title in load data: ", title, data.get('username'))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Select all comments for the given title
    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    movie_id = c.fetchone()[0]

    c.execute("SELECT content FROM comments WHERE movie_id=?", (movie_id,))
    comments = c.fetchall()

    conn.close()

    # Convert the result to a list of strings
    comments_list = [comment[0] for comment in comments]
    print("Comment list: ", comments_list)

    if len(comments_list) == 0:
        return jsonify({"comments": ["No comments yet!"]})

    # Send comments data to AJAX in an appropriate format (JSON in this case)
    return jsonify({"comments": comments_list})


@app.route('/redirect-page', methods=["GET", "POST"])
def go_to_user_profile():
    username = request.args.get("username", "")

    print("redirecting-page username: ", username)

    return render_template("User_Profile.html", username=username)


def combine_lists(comment, movie_dict):
    movie_id, created_at, content = comment
    title = movie_dict.get(movie_id, "Unknown Title")
    return [movie_id, title, created_at, content]


@app.route('/load-user-profile-comments', methods=["POST"])
def load_user_profile_comments():
    username = request.form.get("username")

    user_id = get_user_id(str(username).strip())

    list_of_comments = get_comments(user_id)
    print(list_of_comments)

    list_of_movies = get_movies_and_movie_ids()
    print(list_of_movies)

    movie_dict = dict((movie_id, title) for movie_id, title in list_of_movies)

    combined_lists = list(map(partial(combine_lists, movie_dict=movie_dict), list_of_comments))
    print(combined_lists)

    if len(combined_lists) == 0:
        return jsonify({"list": [["None", "None", "None", "No comments yet!"]]})

    return jsonify({"list": combined_lists})


@app.route('/delete-comment', methods=["POST"])
def delete_comment():
    username = request.form.get("username")
    user_id = get_user_id(str(username).strip())

    created_at = request.form.get("created_at")

    print("username (to_delete): ", username)
    print("created_at: ", created_at)

    delete_comment_by_id_and_created_at(user_id, created_at)

    return jsonify({"success": True, "message": "Comment deleted successfully"})


@app.route('/create-review-summary', methods=["POST"])
def create_summary_from_existing_movie_reviews():
    data = request.get_json()

    title = data.get('title')

    if len(title) == 0:
        return jsonify({"summary": "Empty title!"})

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Select all comments for the given title
    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    movie_id = c.fetchone()[0]

    c.execute("SELECT content FROM comments WHERE movie_id=?", (movie_id,))
    comments = c.fetchall()

    conn.close()

    # Convert the result to a list of strings
    comments_list = [comment[0] for comment in comments]
    print("Comment list: ", comments_list)

    string = "\n\n".join(comments_list)

    if len(comments_list) == 0:
        return jsonify({"summary": "No comments yet!"})

    # load movie id for the movie name

    print(" -- -- Title: ", title)

    final_review_string_prompt = " ".join(comments_list)

    from models.llama__ import run_nlp

    summary = run_nlp(final_review_string_prompt)

    return jsonify({"summary": summary})


# likes and dislikes
@app.route('/like-movie', methods=["POST"])
def like():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Select all comments for the given title
    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    movie_id = c.fetchone()[0]

    c.execute("INSERT INTO likes (username, movie_id) VALUES (?, ?)", (username, movie_id))

    # check if the user has disliked the same movie before
    c.execute("SELECT * FROM dislikes WHERE username=? AND movie_id=?", (username, movie_id))

    if c.fetchone() is not None:
        c.execute("DELETE FROM dislikes WHERE username=? AND movie_id=?", (username, movie_id))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Movie liked successfully"})


@app.route('/dislike-movie', methods=["POST"])
def dislike():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Select all comments for the given title
    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    movie_id = c.fetchone()[0]

    c.execute("INSERT INTO dislikes (username, movie_id) VALUES (?, ?)", (username, movie_id))

    # check if the user has liked the same movie before
    c.execute("SELECT * FROM likes WHERE username=? AND movie_id=?", (username, movie_id))

    if c.fetchone() is not None:
        c.execute("DELETE FROM likes WHERE username=? AND movie_id=?", (username, movie_id))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Movie disliked successfully"})


@app.route("/check-likes-and-dislikes", methods=["POST"])
def check_likes_and_dislikes():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("SELECT movie_id FROM movies WHERE title=?", (title,))
    movie_id = c.fetchone()
    if movie_id is None:
        return jsonify({"success": False, "message": "Movie not found"})

    movie_id = movie_id[0]

    c.execute("SELECT * FROM likes WHERE username=? AND movie_id=?", (username, movie_id))
    liked = c.fetchone() is not None

    c.execute("SELECT * FROM dislikes WHERE username=? AND movie_id=?", (username, movie_id))
    disliked = c.fetchone() is not None

    conn.close()

    return jsonify({"success": True, "liked": liked, "disliked": disliked})


@app.route("/load-wikipedia", methods=["POST"])
def load_wikipedia():
    print("inside load wikipedia")
    data = request.get_json()
    title = data.get('title')

    from algorithm.wikipedia_ import get_movie_details
    print("movie/show: ", title)

    # print("MOVIE: :: ", MOVIE)
    #
    # values = get_info(MOVIE)
    #
    # precise_data_info = values[1]
    # print("precise_data_info: ", precise_data_info)

    title += "movie"
    values = get_movie_details(title)

    title_ = values['title']
    summary_ = values['summary']
    url_ = values['url']

    return jsonify({"title": title_, "summary": summary_, "url": url_})


@app.route("/get-trailer", methods=["POST"])
def get_trailer():
    from algorithm.trailer import get_trailer_link

    data = request.get_json()
    movie = data.get('title')

    print("trailer:: movie: ", str(movie))

    link = get_trailer_link(str(movie))
    print(link)

    return jsonify({"id": link})


@app.route('/get-movies-list', methods=["POST"])
def get_movies_list():
    data = request.get_json()

    username = data['username']

    from algorithm.tmdb.data_hard_coded import movies_data

    return jsonify({"list": movies_data})


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
