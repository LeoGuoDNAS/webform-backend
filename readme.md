# Webform Backend
Used to interact with Strapi APIs
## Dependencies
Python 3.11
Uvicorn
Mangum
fastAPI
## Running the app
```
pip install [dependencies]
```
then
```
python -m uvicorn main:app --reload
```
will run the app on localhost:8000
## API Docs
After running the app. Go to ```localhost:8000/docs```
## Deployment
Deployed to AWS
### Use Magnum

1. Magnum is a handler that allows fastapi projects to run on AWS Lambda
2. If you have not done so, `pip install magnum`
3. `from magnum import Magnum`
4. `handler = Magnum(app)`
5. Put these two lines of code in [main.py](http://main.py/)

### Deploy to AWS Lambda

1. Go to AWS Lambda
2. Create function
3. Select Python 3.11
4. Choose x86_64
5. Under advanced settings, choose Enable function URL and set Auth type to None
6. Create function

### Zipping up local directory

1. Auto generate a requirements.txt using this command `pip freeze > requirements.txt`
2. Download all dependencies to **dep** folder `pip install -t dep -r requirements.txt`
3. Remove packages that you don't need. Otherwise, you will have a very cluttered dep folder with a lot of unnecessary files.
4. Package content in dep to lambda_artifact.zip using `Compress-Archive -Path .\\dep\\* -DestinationPath .\\lambda_artifact.zip -Force`
    - Note: this is for PowerShell, which does not come with zip command. If you are using Linux shells, use `(cd dep; zip ../lambda_artifact.zip -r .)`
5. Add main.py and other python scripts to the zipped file `Compress-Archive -Path .\\main.py -Update -DestinationPath .\\lambda_artifact.zip`
    - Similarly, in Linux shells, use `zip lambda_artifact.zip -u main.py`...

### Handler and Configuration

1. Now upload to Lambda
2. Choose Upload from -> zip file and select the packed zip file
3. Under Runtime settings, choose Edit
4. Change Handler to main.hanlder, which is the name of our handler object, created from Mangum.

### .env files

Zip the .env file together with everything else.