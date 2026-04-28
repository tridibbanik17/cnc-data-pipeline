from flask import Flask
from flask_cors import CORS
from api.ingest import ingest_bp
from api.metrics import metrics_bp
from api.oee import oee_bp
from api.alarms import alarms_bp
from api.anomalies import anomalies_bp
from api.auth import auth_bp
from api.downtime import downtime_bp
from api.history import history_bp
from api.admin import admin_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ingest_bp, url_prefix="/api")
app.register_blueprint(metrics_bp, url_prefix="/api")
app.register_blueprint(oee_bp, url_prefix="/api")
app.register_blueprint(alarms_bp, url_prefix="/api")
app.register_blueprint(anomalies_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(downtime_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"status": "CNC Pipeline Backend Running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    