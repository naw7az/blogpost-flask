# 48:49 (Databases and CRUD operations) :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# config shows path where database will be store using sqlite(can also use MySQL)
# '///' after sqlite means relative path and '////' means absolute
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# SQLAlchemy object
db = SQLAlchemy(app)
# we created a database file check notes.txt(point 4) on how to do it.
# Designing Database Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False means cannot be null, 100 is max_length
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

# the index.html and posts.html files HAS TO BE in a folder named 'templates'
@app.route("/")  
def home():
    return render_template('index.html')

@app.route("/posts2", methods=['GET', 'POST'])
def sending_posts():
    if request.method == 'POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        postAuthor = request.form['author']
        newPost = BlogPost(title=postTitle, content=postContent, author=postAuthor)
        # add the input to database for this session
        db.session.add(newPost)
        # to save the input in database
        db.session.commit()
        return redirect('/posts2')
    # here method is 'GET'
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts2.html', posts=all_posts)
    
# the id is different for all post,hence we need it to delete a post
@app.route('/posts2/delete/<int:id>')
def deletePost(id):
    post = BlogPost.query.get_or_404(id)
    # deleting
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts2')

# if we edit then we need to post the edited one again, hence POST
@app.route('/posts2/edit/<int:id>', methods=['GET', 'POST'])
def editPost(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        # editing
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts2')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts2/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        # creating
        postTitle = request.form['title']
        postAuthor = request.form['author']
        postContent = request.form['content']
        newPost = BlogPost(title=postTitle, content=postContent, author=postAuthor)
        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts2')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":  
    app.run(debug=True)   


    