from flask import Blueprint
my_blueprint = Blueprint("main",__name__)
dbapi = object
@my_blueprint.route('/')
def index():
    return dbapi.user.register("10406902")

@my_blueprint.route("/about")
def about():
    return "This is the about page"