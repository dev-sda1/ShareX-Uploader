## ShareX-Custom-Uploader
## v1.1
## by dev_sda1

## GitHub: https://github.com/dev-sda1/ShareX-Uploader
## License: GPL-3.0

## app.py

## Imports

import json
import os
import string
import random
from os import access
from flask import Flask,redirect
from flask import jsonify
from flask import request
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import send_from_directory

## Vars

app = Flask(__name__)
api = Api(app)

def fileHandler(request):
    uploadedFiles = request.files.getlist('sharex')
        
    for file in uploadedFiles:
        print(file.filename)
        #file.save(file.filename)

    print(uploadedFiles)

    for file in uploadedFiles:
        # Generate a string for the file name

        # Get the file extension
        fileExt = file.filename.split('.')[-1]
        print(fileExt)

        l = string.ascii_lowercase
        fileName = file.filename
        fileName = random_string(6)+"."+fileExt

        file.save(os.path.join("./uploads/", fileName))
        #print("Uploaded " + file.filename)
            
        # Return the file name
        
    return jsonify(
        {"file": fileName}
    )

def urlHandler(request):
    url = request.form.get('url')
    
    # Check if urls.json exists in uploads folder if not create it
    if not os.path.exists("./uploads/urls.json"):
        with open("./uploads/urls.json", "w") as f:
            f.write("{}")
    
    # Read the urls.json file
    with open("./uploads/urls.json", "r") as f:
        data = json.load(f)

    id = random_string(6)
    data[id] = url

    # Write the urls.json file
    with open("./uploads/urls.json", "w") as f:
        json.dump(data, f)

    # Return the id

    return jsonify(
        {"file": "go/"+id}
    )

def random_string(length):  # Generate a random string for use in URLs.
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.post('/upload')
def uploadContent():
    print("OwO an upload")
    r = None
    reqParams = request.form
    #print(request.files)
    with open('server/config.json') as json_file:
        data = json.load(json_file)
        secret = data['secret']

    if reqParams['secret'] == secret: ## Secret has been matched, upload can commence
        print("Secret Matched")
        
        if(request.form['url']) != '':
            print("URL Shortening")
            r = urlHandler(request)
        else:
            print("File upload")
            r = fileHandler(request)

    else: ## Secret did not match, 403.
        return(
            jsonify(
                {"error": "Invalid secret."}
            )
        ),403

    return(
        r
    )

@app.route("/<file_name>")
def callback(file_name):
    fn = file_name
    print("They are looking for: "+fn)

    if fn == "":
        return jsonify(
            {"error": "No file specified."}
        ),400

    else:
        ##Look for the file in folder set in config.json and return it
        
        if access(os.path.join("./uploads/")+fn, os.F_OK):
            print("Found file")
            
            # Return the file as an attachment with environ
            return send_from_directory("./uploads/", fn, environ=request.environ)
        else:
            return jsonify(
                {"error": "File not found."}
            ),404

# Shortened URLs
@app.route("/go/<url_id>")
def url_route(url_id):
    url = url_id

    print("Looking for: "+url)
    if url == "":
        return jsonify({
            "error": "No URL specified."
        }),400
    else:
        ## Look for the URL in the urls.json file and return the file
        with open("./uploads/urls.json", "r") as f:
            data = json.load(f)
        
        if url in data:
            print("Found URL")
            
            # Redirect browser to the URL
            return redirect(data[url], code=302)
        else:
            return jsonify(
                {"error": "URL not found."}
            ),404


if __name__ == '__main__':
    with open('server/config.json') as json_file:
        data = json.load(json_file)
        portNumber = data['webPort']

    app.run(debug=True,host="0.0.0.0")

