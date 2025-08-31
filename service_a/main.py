from app_factory import create_app
from config import CeleryBeatConfig


app = create_app()
celery_app = app.extensions["celery"]
celery_app.conf.beat_schedule = CeleryBeatConfig.BEAT_SCHEDULE


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
