from app_factory import create_app


app = create_app()


if __name__ == "__main__":
    app.run(port=8081, host="0.0.0.0", use_reloader=False)
