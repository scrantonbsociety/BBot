from flask import Flask
from web import main
import dbloader


app = Flask(__name__)
main.dbapi = dbloader.get()
app.register_blueprint(main.my_blueprint)
# app.register_blueprint(index.app)
main.dbapi.user.register("103499409")
if __name__ == "__main__":
    app.run()