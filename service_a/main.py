from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv()


def generate_db_uri():
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    return f"postgresql://{user}:{password}@{host}/{db_name}"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = generate_db_uri
app.register_blueprint()


if __name__ == "__main__":
    app.run(debug=True)
