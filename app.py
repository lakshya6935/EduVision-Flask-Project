from flask import Flask
from database.db import init_database


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    init_database()

    from routes.home import home_bp
    from routes.upload import upload_bp
    from routes.analytics import analytics_bp
    from routes.performance import performance_bp
    from routes.learner import learner_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(learner_bp)

    return app


app = create_app()

if __name__ == "__main__":
    
    app.run(debug=True)
  

    
