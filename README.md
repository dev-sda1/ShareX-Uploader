# ShareX Uploader
A custom uploader for ShareX and others written in Python with Flask.

# Setting up server
1) Run ``sudo apt update`` then Install the required Python packages with: ``sudp apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools`` (how you acquire them depends on your distribution)
2) Run ``sudo apt install python3-venv``.
3) Visit your directory of choice where you wish the project to be located on your server and run ``git clone https://github.com/dev-sda1/ShareX-Uploader.git``
2) CD into the directory with ``cd ShareX-Uploader``
3) Open ``server/config.json`` in your text editor of choice. This is where your client secret will be stored.
4) Make sure your client secret is long and stored safely. A password generator site like [this one](https://passwordsgenerator.net/), or the generator tool in your password manager software can be used to create a long key.
5) Save the config file and cd back to the projects root directory
6) Run ``python3 -m venv sharexupload-env``, then ``source sharexupload-env/bin/activate``. Your prompt should change to something along the lines of ``(sharexupload-env)user@host``.
7) Now it's time to install the pip packages that make the server work - run ``pip3 install -r pip.txt`` to install them.
8) Test that uwsgi installed properly by running ``uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app`` and checking in your browser that a 404 message returns with ``http://your_server_ip:5000``. You can change the 5000 port to anything else, if you want to.
9) Exit the env by running ``deactivate``, and enter ``ShareXUploader.service`` in the text editor of your choice.
10) Change ``ADD_USER_HERE`` and all instances of ``USER_HERE`` to your username.
11) Change all instances of ``ADD_DIRECTORY_HERE`` to where you cloned the repository. (e.g ``/home/pyxlwuff/ShareX-Uploader/``)
12) Change all instances of ``ENV_FOLDER`` to ``sharexupload-env``

## Configuring SystemD and NGINX
1) Copy the resulting .service file to ``/etc/systemd/system/``
2) Run ``sudo systemctl start ShareXUploader`` and then ``sudo systemctl enable ShareXUploader``
3) Check the status to ensure there's no errors by running ``sudo systemctl status ShareXUploader``. If there are any errors, ensure to correct them before continuing and restarting the service with ``sudo systemctl restart ShareXUploader.service``
4) Now that we know our server is up and running, we can now configure our NGINX endpoint. Create a new file with ``sudo nano /etc/nginx/sites-available/sharex-uploader``
5) Copy the following block below, replacing ``your_domain`` with the domain of your choice, and DIRECTORY_HERE with where you stored the repository:

```server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:DIRECTORY_HERE/ShareXUploader/app.sock;
    }
}
```
6) Run ``sudo ln -s /etc/nginx/sites-available/sharex-uploader /etc/nginx/sites-enabled`` to link it to the sites-enabled directory, making it resolvable, followed by ``sudo nginx -t`` to test the configuration is OK. If you get any errors, make sure to resolve them first.
7) Restart nginx with ``sudo systemctl restart nginx``, then navigate to your domain to see if it worked! (You should see a file not found error - this is normal)

## Setting up ShareX


# Running the server
These steps are for NGINX users. Apache users can find links to their own steps at the footer. 
Users running this off of serverless solutions like Heroku should consult their service's documentation for how to deploy.

