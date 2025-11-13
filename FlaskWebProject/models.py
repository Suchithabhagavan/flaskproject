from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from azure.storage.blob import BlockBlobService
import string, random
from werkzeug.utils import secure_filename
from flask import flash

# Azure Blob Storage Configuration
blob_container = app.config['BLOB_CONTAINER']
blob_service = BlockBlobService(
    account_name=app.config['BLOB_ACCOUNT'],
    account_key=app.config['BLOB_STORAGE_KEY']
)

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    """Generate a random filename string for blob uploads."""
    return ''.join(random.choice(chars) for _ in range(size))


# ------------------------------
# User Model
# ------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    """Flask-Login user loader."""
    return User.query.get(int(user_id))


# ------------------------------
# Post Model
# ------------------------------
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.title}>'

    def save_changes(self, form, file, user_id, new=False):
        """Save post details and upload image to Azure Blob Storage."""
        self.title = form.title.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = user_id

        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            random_filename = id_generator()
            new_filename = f"{random_filename}.{file_extension}"

            try:
                # Upload new file
                blob_service.create_blob_from_stream(blob_container, new_filename, file)

                # Delete old image if it exists
                if self.image_path:
                    try:
                        blob_service.delete_blob(blob_container, self.image_path)
                    except Exception as e:
                        app.logger.warning(f"Could not delete old blob: {e}")

                self.image_path = new_filename
                app.logger.info(f"Image uploaded successfully: {new_filename}")

            except Exception as e:
                app.logger.error(f"Error uploading image: {e}")
                flash("Error uploading image. Please try again.", "danger")

        if new:
            db.session.add(self)

        db.session.commit()
        app.logger.info(f"Post '{self.title}' saved successfully.")
