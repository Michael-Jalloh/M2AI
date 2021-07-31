from flaskapp.app import app, db
from flaskapp import commands

commands.init_app(app)
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


