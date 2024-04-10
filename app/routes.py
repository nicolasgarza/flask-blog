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

@app.route('api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_or_none(Post.id == post_id)
    if post:
        return jsonify(post.dict())
    else:
        return jsonify({"msg": "Post does not exist"}), 404

@app.route('api/posts/<page>', methods=['GET'])
def get_posts(page):
    query = Post.select().paginate(page, 10)
    posts = [post for post in query.dicts()]
    return jsonify(posts)

@app.route('/api/users/<username>/posts', methods=['GET'])
def get_user_posts(username):
    user = User.get_or_none(User.username == username)
    if user:
        query = Post.select().where(Post.author == username)
        posts = [post for post in query.dicts()]
        return jsonify(posts)
    else:
        return jsonify({"msg": "User does not exist"}), 404

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    user = User.get(User.user_id == current_user)

    title = request.json.get('title', '').strip()
    content = request.json.get('content', '').strip()

    if not title or not content:
        return jsonify({"msg": "Title and content are required"}), 400

    post = Post.create(title=title, content=content, author=user)
    return jsonify(post.dict()), 201

@app.route('/api/posts/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user = get_jwt_identity()
    post = Post.get_or_none(Post.id == post_id)

    if not post:
        return jsonify({"msg": "Post does not exist"}), 404

    if current_user != post.author.user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    title = request.json.get('title', '').strip()
    content = request.json.get('content', '').strip()

    if title:
        post.title = title
    if content:
        post.content = content
        
    post.save()

    return jsonify(post.dict())

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

@app.route('/api/<post_id>/comments/<comment_id>', methods=['GET'])
def get_comment(post_id, comment_id):
    comment = Comment.get_or_none(Comment.post == post_id, Comment.id == comment_id)
    if comment:
        return jsonify(comment.dict())
    else:
        return jsonify({"msg": "Comment does not exist"}), 404

@app.route('/api/users/<username>/comments', methods=['GET'])
def get_user_comments(username):
    user = User.get_or_none(User.username == username)
    if user:
        query = Comment.select().where(Comment.author == user)
        comments = [comment for comment in query.dicts()]
        return jsonify(comments)
    else:
        return jsonify({"msg": "User does not exist"}), 404

@app.route('/api/<post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    current_user = get_jwt_identity()

    user = User.get(User.user_id == current_user)

    content = request.json.get('content', '').strip()
    if not content:
        return jsonify({"msg": "Content is required"}), 400

    post = Post.get(Post.id == post_id)

    comment = Comment.create(content=content, author=user, post=post)
    return jsonify(comment.dict()), 201

@app.route('/api/<post_id>/comments/<comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(post_id, comment_id):
    current_user = get_jwt_identity()
    comment = Comment.get_or_none(Comment.post == post_id, Comment.id == comment_id)

    if not comment:
        return jsonify({"msg": "Comment does not exist"}), 404
    
    if current_user != comment.author.user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    content = request.json.get('content', '').strip()
    if not content:
        return jsonify({"msg": "Content is required"}), 400

    comment.content = content
    comment.save()

    return jsonify(comment.dict())

# USERS

@app.route("api/users/<username>", methods=['GET'])
def get_user(username):
    user = User.get_or_none(User.username == username)
    if user:
        return jsonify(user.dict())
    else:
        return jsonify({"msg": "User does not exist"}), 404

@app.route('/api/users/<page>', methods=['GET'])
def get_users(page):
    query = User.select().paginate(page, 10)
    users = [user.dict() for user in query]
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json.get('username', '').strip()
    password = request.json.get('password', '').strip()

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    
    if User.get_or_none(User.username == username):
        return jsonify({"msg": "Username already exists"}), 400

    user = User.create(username=username)
    user.set_password(password)
    user.save()

    return jsonify(user.dict()), 201

@app.route('/api/users/<username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    current_user = get_jwt_identity()
    user = User.get_or_none(User.user_id == current_user)

    if not user:
        return jsonify({"msg": "User does not exist"}), 404
    
    if user.user_id != current_user:
        return jsonify({"msg": "Unauthorized"}), 401

    new_username = request.json.get('username', '').strip()
    new_password = request.json.get('password', '')

    if new_username:
        user.username = new_username
    if new_password:
        user.set_password(new_password)
    user.save()

    return jsonify(user.dict())