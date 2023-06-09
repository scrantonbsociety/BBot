from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from web.helper_functions import getLoginStatus

second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@second.route("/index")
@second.route("/")
def index():
    return "<h1>Welcome to the admin page!</h1>"

@second.route("/test")
def test():
    return "<h1>test</h1>"