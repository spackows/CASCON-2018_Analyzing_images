## Prerequisite

- Install Python: https://www.python.org/downloads/
- Install IBM Cloud CLI: https://console.bluemix.net/docs/cli/reference/ibmcloud/download_cli.html#install_use


## 1. Run the app locally

1.1 Install the dependencies listed in the requirements.txt file to be able to run the app locally:
```
pip install -r requirements.txt
```

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
