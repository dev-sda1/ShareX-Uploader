# ShareX Uploader
A custom uploader for ShareX and others written in Python with Flask.

# Prerequisites
- Python 3 and pip
- Webserver to host the endpoint on
- ShareX

# Setting up server
1) Visit your directory of choice where you wish the project to be located on your server and run ``git clone https://github.com/dev-sda1/ShareX-Uploader.git``
2) CD into the directory with ``cd ShareX-Uploader``
3) Open ``server/config.json`` in your text editor of choice. This is where your client secret will be stored along with a webport which the server will run off of, if you wish to change it.
4) Make sure your client secret is long and stored safely. A password generator site like [this one](https://passwordsgenerator.net/), or the generator tool in your password manager software can be used to create a long key.
5) Save the config file and 

# Running the server
These steps are for NGINX users. Apache users can find links to their own steps at the footer. 
Users running this off of serverless solutions like Heroku should consult their service's documentation for how to deploy.

