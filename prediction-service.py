import logging, json
from flask import Flask, request
from joblib import load

app = Flask(__name__)

clf = load('model.joblib') 


@app.route("/predict", methods=["POST"])
def predict():
    data =  request.get_json()["instances"]
    pred = clf.predict(data)
    return {"predictions": pred.tolist() }

@app.route("/predict-proba", methods=["POST"])
def predict_prob():
    data =  request.get_json()["instances"]
    pred = clf.predict_proba(data)
    return {"predictions": pred.tolist() }


@app.route("/health-check", methods=["GET"])
def health():
    return ('', 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')