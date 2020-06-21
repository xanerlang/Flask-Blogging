from flask import Flask, request, redirect,url_for
from flask_blogging import signals, views
from flask_login import UserMixin, LoginManager, login_user, logout_user


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    def get_name(self):
        return "Paul Dirac"  # typically the user's name

def plugin(app,engine):
    
    add_static = views.Blueprint('plugin_login',__name__,static_folder='./html/',static_url_path='/login') 
    app.register_blueprint(add_static)

    login_manager = LoginManager(app) 
    
    @login_manager.user_loader
    @engine.user_loader
    def load_user(user_id):
        return User(user_id)
    
    @app.route("/login/", methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            if request.form["username"] == "root":
                user = User("root")
                login_user(user)
                return redirect("/blog")
            else:
                error = "Invalid username"
       
        return redirect(url_for('plugin_login.static',filename='login.html'))
    
    @app.route("/logout/")
    def logout():
        logout_user()
        return redirect("/")

def register(app):
    signals.engine_initialised.connect(plugin)
    return
