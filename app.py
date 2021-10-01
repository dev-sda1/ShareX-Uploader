## SpotifyWebPresence
## v1.1 [Python Rewrite]
## by dev_sda1

## GitHub: https://github.com/dev-sda1/spotify-web-presence
## License: GPL-3.0

## app.py

## Imports

import json
import os
import string
import random
from os import access
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import send_from_directory

## Vars

app = Flask(__name__)
api = Api(app)


@app.post('/upload')
def uploadContent():
    #print(request.files)
    #print(request.form)

    uploadedFiles = request.files.getlist('sharex')
    reqParams = request.form

    for file in uploadedFiles:
        print(file.filename)
        #file.save(file.filename)

    print(uploadedFiles)
    print(reqParams)
    
    # Checking if the secret sent in reqParams matches whats in config.json

    with open('server/config.json') as json_file:
        data = json.load(json_file)
        secret = data['secret']

    if reqParams['secret'] == secret:
        print("Secret Matched")
        
        # Uploading the file to the server
        for file in uploadedFiles:
            # Generate a string for the file name

            # Get the file extension
            fileExt = file.filename.split('.')[-1]
            print(fileExt)

            l = string.ascii_lowercase
            fileName = file.filename
            fileName = ''.join(random.choice(l) for i in range(10))+"."+fileExt

            file.save(os.path.join("./uploads/", fileName))
            #print("Uploaded " + file.filename)
        
        # Return the file name
        return jsonify(
            {"file": fileName}
            )

    else:
        return(
            jsonify(
                {"error": "Invalid secret."}
            )
        ),403

    return jsonify(
        {"message":"ok"}
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

if __name__ == '__main__':
    with open('server/config.json') as json_file:
        data = json.load(json_file)
        portNumber = data['webPort']

    app.run(debug=True,port=portNumber)

