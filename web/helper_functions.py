from flask import Flask, redirect, url_for, render_template, request, session, flash

# Returns the appropriate text which fills the button at the top right,
# depending on if the user is signed in or not
# If the user is signed in, make the button say "home", otherwise, make
# it say "Login"
def getLoginStatus() -> str:
    if "user" in session:
        return "Home"
    return "Login"