# ShareX Uploader
A custom uploader for ShareX images and files for your server written in Python with Flask.
Currently in beta, there may be some issues. If you do find any please raise a GH issue to let me know

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E1HLTE)

# Setting up and running the server
These steps are for NGINX users. Apache users can find links to their own steps at the footer. 
Users running this off of serverless solutions like Heroku should consult their service's documentation for how to deploy.

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
1) Download the example template [here](https://github.com/dev-sda1/ShareX-Uploader/blob/main/example_upload.sxcu)
2) Double click it and select "yes" on the prompt that shows up 

![image](https://user-images.githubusercontent.com/43112896/135697173-7dc395c8-da8c-49cf-947d-b32f7af7fa98.png)

3) Your custom upload defaults should now change to the template you just imported. Begin by editing the Request URL to your domain.

![image](https://user-images.githubusercontent.com/43112896/135697195-b9385b6b-3b98-4e17-b677-7115c3a4544e.png)

4) Add the secret you added to your server's config.json earlier into the form value.

![image](https://user-images.githubusercontent.com/43112896/136977404-e89c32f6-b6f2-4c2c-b7e9-761b9bb868d1.png)

5) Scroll down to the URL section and change ``yourdomain.here`` to your domain.

![image](https://user-images.githubusercontent.com/43112896/135697227-804eef68-5964-4f74-8171-b6003460f1bf.png)

6) Click the "Test" button next to Image uploader and see if you get a response. If you get something similar to the screenshot below, you're good to go! Otherwise, you might need to check your secret or URL settings. If it's not that, it might be something on the server. 

![image](https://user-images.githubusercontent.com/43112896/135697261-f50ad6bf-146a-4baf-90dc-7df56ab5d419.png)


# Other server instructions
If you use another solution like Apache, you can find instructions tailored to your server here:
https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft

Note that as said earlier if you use a serverless service like Heroku to host this, you will need to consult your service's documentation for the best way to deploy without issues.

