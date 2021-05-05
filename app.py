from flask import Flask,render_template,redirect,session,flash
from flask_debugtoolbar import DebugToolbarExtension
from modals import db,connect_db,User,Feedbacks
from forms import Register,Login,Feedback
import os 
app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///feedback_db')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY","Hell_So_SECRET_12_AA")

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def hello_world():
    return redirect('/register')


@app.route("/register",methods=["POST","GET"])
def register():
    form = Register()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username=username,
            password=password,
            email=email,
            first=first_name,
            last=last_name)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect('/secret')

    return render_template("register.html",form=form)


@app.route("/login",methods=["POST","GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            session['username'] = user.username
            return redirect(f"/user/{user.username}")
        else: 
            form.username.errors = ["Please Provide a valid Username or Password"]

    return render_template("login.html",form=form)

@app.route("/secret")
def secret():
    if "username" not in session:
        flash("Please Login")
        return redirect("/login")
    return "You make it"

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/user/<username>")
def the_user(username):
    if "username" not in session:
        flash("please login first")
        return redirect('/login')
    
    current_user = User.query.get_or_404(username)
    return render_template("user.html",user=current_user)

@app.route('/feedback/<int:feedback_id>/update',methods=["POST","GET"])
def edit_feedback(feedback_id):
    if "username" not in session:
        flash("Please Login")
        return redirect("/login")
    current_fb = Feedbacks.query.get_or_404(feedback_id)
    form = Feedback(obj=current_fb)
    if form.validate_on_submit():
        current_fb.title = form.title.data
        current_fb.content = form.content.data
        current_fb.username = current_fb.user.username
        db.session.commit()
        return redirect(f'/user/{current_fb.user.username}')
    
    return render_template("efeedback.html",form=form,feedback=current_fb)

@app.route('/feedback/<int:feedback_id>/delete',methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedbacks.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f"/user/{feedback.username}")


@app.route('/users/<username>/feedback/add',methods=["POST","GET"])
def add_feedback(username):
    if "username" not in session:
        return redirect("/login")

    current_user = User.query.get_or_404(username)
    form = Feedback()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = current_user.username
        new_fb = Feedbacks(title=title,content=content,username=username)
        db.session.add(new_fb)
        db.session.commit()
        return redirect(f"/user/{username}")
    return render_template("afeedback.html",form=form,user=current_user)

@app.route("/users/<username>/delete",methods=["POST"])
def delete_user(username):
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")
