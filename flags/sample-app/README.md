## Prerequisite

- Install Python: https://www.python.org/downloads/

    - Make sure to have the installer add Python to your environment variables
    - Mac users, also install pip by issuing this command:
        ```
        sudo easy_install pip
        ```
    - Mac users, also add your user base binary directory to your path:
    
        1.  Find the user base binary directory by running this command:
            ```
            python -m site --user-base
            ```
        2.  Add your user base binary directory to the file `/etc/paths`
        
        See: [Complete instructions](https://www.architectryan.com/2012/10/02/add-to-the-path-on-mac-os-x-mountain-lion/)


- Install IBM Cloud CLI: https://console.bluemix.net/docs/cli/reference/ibmcloud/download_cli.html#install_use


## 1. Run the app locally

1.1 Install the dependencies:
<pre>
pip install -r requirements.txt
</pre>
    
Mac users, run this command instead:
<pre>
pip install --user -r requirements.txt
</pre>

1.2 Update server.py with your Visual Recognition apikey and model id

1.3 Run the app:
```
python server.py
```

1.4 View your app at: http://localhost:8000



## 2. Create a new Python Flask app starter in IBM Cloud:

https://console.bluemix.net/catalog/starters/python



## 3. Prepare the local app code for deployment

Update manifest.yml.

Replace 'app-name' with the app name you chose for your Python Flask app starter:
```
applications:
- name: app-name
  memory: 128M
```



## 4. Deploy the app

4.1 Login to your IBM Cloud account:
```
bx login
```

4.2 Target the CloudFoundry API endpoint:
```
bx target --cf
```

4.3 From within the app working directory (where the file server.py is located) push your app to IBM Cloud:
```
bx app push
```


### Citations
File:Star Spangled Banner instrumental.ogg. (2018, July 9). Wikimedia Commons, the free media repository.  https://commons.wikimedia.org/w/index.php?title=File:Star_Spangled_Banner_instrumental.ogg&oldid=310263642.

File:United States Navy Band - O Canada.ogg. (2018, July 24). Wikimedia Commons, the free media repository. https://commons.wikimedia.org/w/index.php?title=File:United_States_Navy_Band_-_O_Canada.ogg&oldid=312247270. 
