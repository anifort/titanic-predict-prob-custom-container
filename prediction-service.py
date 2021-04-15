import json, pickle, os,logging
from google.cloud import storage
from argparse import ArgumentParser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger


gunicorn_error_logger = logging.getLogger("gunicorn.error")
# (you could probably just use = instead extend below)
logging.root.handlers.extend(gunicorn_error_logger.handlers)
logging.root.setLevel(gunicorn_error_logger.level)

app = FastAPI()

obj = {}

@app.on_event("startup")
async def startup_event():
    
    if "model_dir" not in obj:
        obj['model_dir'] = os.environ['AIP_STORAGE_URI'] if 'AIP_STORAGE_URI' in os.environ else ""
    
    scheme, bucket, path, file = process_gcs_uri(obj['model_dir'])
    if scheme != "gs:":
            raise ValueError("URI scheme must be gs")
     
    if file is None:
        file="model.pkl"
        
    # Upload the model to GCS
    b = storage.Client().bucket(bucket)
    
    file_path = os.path.join(path, file)
    blob = b.blob(file_path)
    print(file_path)
    obj['clf'] = pickle.loads(blob.download_as_string())
    
    
def process_gcs_uri(uri: str) -> (str, str, str, str):
    '''
    Receives a Google Cloud Storage (GCS) uri and breaks it down to the sheme, bucket, path and file
    
            Parameters:
                    uri (str): GCS uri

            Returns:
                    scheme (str): uri scheme
                    bucket (str): uri bucket
                    path (str): uri path
                    file (str): uri file
    '''
    url_arr = uri.split("/")
    if "." not in url_arr[-1]:
        file = None
    else:
        file = url_arr.pop()
    scheme = url_arr[0]
    bucket = url_arr[2]
    path = "/".join(url_arr[3:])
    path = path[:-1] if path.endswith("/") else path
    
    return scheme, bucket, path, file


#@app.route("/predict", methods=["POST"])
@app.post("/predict")
async def predict(request: Request):
    req = await request.json() # concour object
    try:
        data = req["instances"]
    except:
        print("No instances key found in post request")
    
    params = {}
    if "parameters" in req:
        params =  req["parameters"]
    
    pred = None
    if hasattr(obj['clf'],'predict_proba') and "predict_proba" in params and params['predict_proba']==True:
        pred = obj['clf'].predict_proba(data)
    else:
        pred = obj['clf'].predict(data)
        
    return {"predictions": pred.tolist() }


# If the server is not ready to handle prediction requests, do not respond to the health check request within 10 seconds,
# or respond with any status code except for 200 OK. For example, respond with status code 503 Service Unavailable.
@app.get("/health-check")
#@app.route("/health-check", methods=["GET"])
def health():
    return {}
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '--model_dir',
        help = 'location of the model in gs://', 
        default =  os.environ['AIP_STORAGE_URI'] if 'AIP_STORAGE_URI' in os.environ else "",
        type = str
    )

    args = parser.parse_args()   
    obj['model_dir'] = args.model_dir
    
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)