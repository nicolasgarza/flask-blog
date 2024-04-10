from flask import jsonify, request
from app import app, db
from app.models import User, Post, Comment

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# AUTHENTICATION

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.get_or_none(User.username == username)

    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


# POSTS

@app.route('/api/posts', methods=['GET'])
def get_posts():
    query = Post.select()
    posts = [post for post in query.dicts()]
    return jsonify(posts)

@app.route('api/posts/<slug>', methods=['GET'])
def get_post(slug):
    query = Post.get(Post.slug == slug)
    post = query.dicts()
    return jsonify(post)

@app.route('api/posts/<page>', methods=['GET'])
def get_posts(page):
    query = Post.select().paginate(page, 10)
    posts = [post for post in query.dicts()]
    return jsonify(posts)

@app.route('/api/users/<username>/posts', methods=['GET'])
def get_user_posts(username):
    query = Post.select().where(Post.author == username)
    posts = [post for post in query.dicts()]
    return jsonify(posts)

# COMMENTS

@app.route('/api/<post_id>/comments', methods=['GET'])
def get_comments(post_id):
    query = Comment.select().where(Comment.post == post_id)
    comments = [comment for comment in query.dicts()]
    return jsonify(comments)

@app.route('/api/<post_id>/comments/<page>', methods=['GET'])
def get_comments(post_id, page):
    query = Comment.select().where(Comment.post == post_id).paginate(page, 10)
    comments = [comment for comment in query.dicts()]
    return jsonify(comments)

@app.route('/api/<post_id>/comments/<slug>', methods=['GET'])
def get_comment(post_id, slug):
    query = Comment.get(Comment.post == post_id, Comment.slug == slug)
    comment = query.dicts()
    return jsonify(comment)

@app.route('/api/users/<username>/comments', methods=['GET'])
def get_user_comments(username):
    query = Comment.select().where(Comment.author == username)
    comments = [comment for comment in query.dicts()]
    return jsonify(comments)

# USERS

@app.route('/api/users', methods=['GET'])
def get_users():
    query = User.select()
    users = [users for users in query.dict()]
    return jsonify(users)

@app.route("api/users/<username>", methods=['GET'])
def get_user(username):
    query = User.get(User.username == username)
    user = query.dict()
    return jsonify(user)

@app.route('/api/users/<page>', methods=['GET'])
def get_users(page):
    query = User.select().paginate(page, 10)
    users = [user for user in query.dict()]
    return jsonify(users)