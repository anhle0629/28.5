from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from werkzeug.exceptions import Unauthorized ###did not know i could do that###
from forms import UserForm, LoginForm, DeleteForm, feedbackform

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

app.app_context().push()
connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    return render_template('base.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate.submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username, password, email, first_name, last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template("register.html", form = form)
        session['user_username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect("/secert")
    
    return render_template("register.html", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    
    if user in session:
        return redirect(f"/secert{session['username']}") ##not sure if this is right??###

    if form.validate.submit():
        username = form.username.data
        password = form.password.data 

        user = User.authenticate(username, password)
        if user:
            flash(f"welcome back {user.username}!")
            session['user_username']= user.username 
            return redirect("/secert")
        else: 
            form.username.errors = ['Invalid passsword/username!']
            return render_template("login.html", form = form)

    return render_template('login.html', form = form)


@app.route('/logout')
def logout_user():
    session.pop('user_username')
    flash('see you later')
    return redirect("/")@app.route("/user/<")

@app.route('/user/<username')
def showuser(username):
   
   if "username" not in session or username != session['username']:
       raise Unauthorized()
   
   user = User.query.all(username)
   form = DeleteForm() ##why leave this blank?### 

   return render_template('show.html', user= user, form= form)

@app.route('/user/<username/delete', methods = ["POST"])
def remove_user(username):
    """delete user"""

    if "user_username" not in session:
        flash("please login in me first, before deleting!")
        return redirect("/login")
    user = User.query.get_or_404(username)
    if user.user_username == session["user_username"]:
        db.session.delete(user)
        db.session.commit()

        flash("the user has been deleted")
        return redirect("/user/<username")
    flash("You don't have persmission to do that!")
    redirect('/user/<username')

@app.route('/user/<username>/feedback/add', methods=["GET", "POST"])
def feedback_form(username):
    
    if "user_username" not in session or username != session["username"] :
        flash("please login in me first, before deleting!")
        return redirect("/login")
    
    form = feedbackform()
    if form.validate.submit():
        title = form.title.data
        content = form.content.data
        username = username
        
        new_feeback = Feedback(title = title, content = content, username = username)
        db.session.add(new_feeback)
        db.session.commit()

        flash("you have add a new feedback!")
        return redirect("/user/{feedback.username}", form = form)
    else:
        return render_template("feedback.html", form = form)
    
@app.route("/feedback/<int:feedback.id>/update", methods = ["GET", "POST"])
def update_feedback(feedback_id):

    feedback = feedback.query.get(feedback_id)
    
    if "user_username" not in session or feedback != session["username"] :
        flash("please login in me first, before deleting!")
        return redirect("/login")

    form = feedback_form(obj= feedback)
    if form.validate.submit():
        form.title.data = feedback.title
        form.content.data = feedback.content

        db.session.commit()

        flash("you have update your feedback!")
        return redirect("/user/{feedback.username}")
    else: 
        return render_template("edit.html", form = form, feedback = feedback)
    
@app.route("/feedback/<int:feedback.id>/delete", methods = ["POST"])
def remove_update(feedback_id):
   
    if "user_username" not in session or feedback != session["username"] :
        flash("please login in me first, before deleting!")
        return redirect("/login")
    
    feedback = Feedback.query.get_or_404(feedback_id)
    form = DeleteForm()
    if form.validate.submit():
        db.session.delete(feedback)
        db.session.commit()

        flash("you have deleted your feedback!")
        return redirect("/user/{feedback.username}")



    


    

