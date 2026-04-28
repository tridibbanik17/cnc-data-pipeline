from flask import Flask
from flask_cors import CORS
from api.ingest import ingest_bp
from api.metrics import metrics_bp
from api.oee import oee_bp
from api.alarms import alarms_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ingest_bp, url_prefix="/api")
app.register_blueprint(metrics_bp, url_prefix="/api")
app.register_blueprint(oee_bp, url_prefix="/api")
app.register_blueprint(alarms_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"status": "CNC Pipeline Backend Running"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)