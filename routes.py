#import libraries
from flask import Flask, flash, render_template, request, url_for, redirect, session
from models import db, User, Post
from forms import SignupForm, LoginForm, NewpostForm
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "cscie14a-hw3"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/hw3_db'

db.init_app(app)

#routes
@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        session_user = User.query.filter_by(username=session['username']).first()
        posts = Post.query.filter_by(author=session_user.uid).all()
        return render_template('index.html', title='Home', posts=posts,
        session_username=session_user.username)
    else:
        all_posts = Post.query.all()
        return render_template('index.html', title='Home', posts=all_posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('The username already exists. Please pick another one.')
            return redirect(url_for('signup'))
        else:
            user = User(username=username, password=sha256_crypt.hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    else:
        return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        check_pw = sha256_crypt.verify(password, user.password)

        if user is None or not check_pw:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            return redirect(url_for('index'))
            #return username
    else:
        return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    form = NewpostForm()

    if request.method == 'POST':
        session_user = User.query.filter_by(username=session['username']).first()
        content = request.form['content']
        new_post = Post(author=session_user.uid, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newpost.html', title='Newpost', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_user = request.form['search']
    #user = User.query.filter_by(username=search_user).first()
    #posts = Post.query.filter_by(author=user.uid).all()
    #return render_template('profile.html', title='Profile', username=search_user, user=user, posts=posts)
    return redirect(url_for('profile', username=search_user))

@app.route('/profile/<string:username>', methods=['GET', 'POST'])
def profile(username):
    #search_user = username
    follow_flag = False
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user.uid).all()
    return render_template('profile.html', title='Profile', user=user, posts=posts, follow_flag = follow_flag)

if __name__ == "__main__":
    app.run(debug=True)
