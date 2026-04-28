import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.trained = False

    def train(self, data):
        X = np.array(data)
        if len(X) < 20:
            return False
        self.model.fit(X)
        self.trained = True
        return True

    def detect(self, sample):
        if not self.trained:
            return False, 0.0

        X = np.array([sample])
        score = self.model.decision_function(X)[0]
        pred = self.model.predict(X)[0]
        is_anomaly = bool(pred == -1)

        severity = float(abs(score))
        return is_anomaly, severity
    

detector = AnomalyDetector()