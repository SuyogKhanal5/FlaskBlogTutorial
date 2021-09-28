from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)

@views.route("") # Makes it so that if you got to / or /home you get the same
@views.route("home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", posts = posts, user = current_user) 
    # create variable, can pass into html document

# When creating html5 file, write html:5 then press tab

# templates folder must be called templates

@views.route("create-post", methods = ['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category = 'error')
        else:
            post = Post(text = text, author = current_user.id)
            db.session.add(post)
            db.session.commit()

            flash('Post Created!', category = 'success')

            return redirect(url_for('views.home'))

    return render_template('create_post.html', user = current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("Post does not exist", category = 'error')
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post", category = 'error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category = "success")

    return redirect(url_for('views.home'))
        