from azure.storage.blob import BlobClient
import requests,uuid

import json
from flask import Flask, flash, request, redirect, url_for, render_template



app = Flask(__name__)


#UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST','GET'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        id = str(uuid.uuid1())
        blob = BlobClient.from_connection_string(
            conn_str="DefaultEndpointsProtocol=https;AccountName=imageclassification1;AccountKey=R0X33tP9FY0TfKwZ+O2BznpwDUZZWxbF2lJE3ToLhF4Dox/2V+frwVYUmEq3yDXAg+M5bszachzBpZDfT05CDA==;EndpointSuffix=core.windows.net",
            container_name="checkimage", blob_name=id)
        blob.upload_blob(file)
        url = 'https://imageclassification1.blob.core.windows.net/checkimage/' + str(id)
        test = json.dumps({"data": url})
        headers = {'Content-Type': 'application/json'}
        service = 'http://cfd31e9f-f00e-4cd7-b4de-42acbaedff31.centralus.azurecontainer.io/score'
        resp = requests.post(service, test, headers=headers)
        m = resp.text
        flash(m)
        return render_template('index.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)



if __name__ == '__main__':
     app.run(debug=True)