"""
Routes and views for the Flask application.
"""
from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db
from FlaskWebProject.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import msal
import uuid

# Base URL for images in blob storage
imageSourceUrl = f"https://{app.config['BLOB_ACCOUNT']}.blob.core.windows.net/{app.config['BLOB_CONTAINER']}/"


# ------------------------------
# Home Page
# ------------------------------
@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template('index.html', title='Home Page', posts=posts)


# ------------------------------
# Create New Post
# ------------------------------
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        app.logger.info(f"New post created by {current_user.username}: {form.title.data}")
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', title='Create Post', form=form, imageSource=imageSourceUrl)


# ------------------------------
# Edit Existing Post
# ------------------------------
@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files['image_path'], current_user.id)
        app.logger.info(f"Post edited by {current_user.username}: {form.title.data}")
        flash('Post updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', title='Edit Post', form=form, imageSource=imageSourceUrl)


# ------------------------------
# Local Username/Password Login
# ------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            app.logger.warning("Invalid login attempt.")
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.info(f"User '{user.username}' logged in successfully.")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    # MS Login - Create auth URL
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)


# ------------------------------
# Microsoft Authentication (Redirect)
# ------------------------------
@app.route(Config.REDIRECT_PATH)
def authorized():
    if request.args.get('state') != session.get("state"):
        app.logger.warning("Invalid state returned during Microsoft authentication.")
        return redirect(url_for("home"))

    if "error" in request.args:
        app.logger.error(f"Microsoft auth error: {request.args.get('error_description')}")
        return render_template("auth_error.html", result=request.args)

    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Config.SCOPE,
            redirect_uri=url_for("authorized", _external=True)
        )

        if "error" in result:
            app.logger.error(f"Token acquisition error: {result.get('error_description')}")
            return render_template("auth_error.html", result=result)

        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
        app.logger.info("Microsoft user logged in successfully.")

        # For this project, use admin account for MS users
        user = User.query.filter_by(username="admin").first()
        if user:
            login_user(user)
            app.logger.info("Admin logged in through Microsoft.")
        else:
            app.logger.error("Admin account not found in database.")

    return redirect(url_for('home'))


# ------------------------------
# Logout (Both Local + Microsoft)
# ------------------------------
@app.route('/logout')
def logout():
    logout_user()
    if session.get("user"):  # Used Microsoft Login
        session.clear()
        app.logger.info("Microsoft user logged out.")
        return redirect(
            Config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("login", _external=True)
        )
    app.logger.info("User logged out.")
    return redirect(url_for('login'))


# ------------------------------
# MSAL Helper Functions
# ------------------------------
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app.config["CLIENT_ID"],
        authority=authority or Config.AUTHORITY,
        client_credential=app.config["CLIENT_SECRET"],
        token_cache=cache
    )


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state,
        redirect_uri=url_for("authorized", _external=True)
    )
