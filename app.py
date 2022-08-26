from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.secret_key = 'f25e42871b71d695e0edb0deb4404fab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False