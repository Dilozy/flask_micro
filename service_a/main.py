from app_factory import create_app


app = create_app()
celery_app = app.extensions["celery"]


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
