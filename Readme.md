# Staff Promotion API :rocket:

The purpose of this README.md file is to explain the steps required to setup this project in your local environment for testing.

### Set up? :pushpin:

### Requirements 
* Python
* Docker
* Git

## Setting up with Python ### 

**Clone Repo**
```
git clone https://github.com/Arnold-git/staff-promotion-api
```

**Change current working directory**
```
cd staff-promotion-api
```

**Create a Virtual environment**
```
python -m venv .venv
```
**Activate virutual Environment**
```
#windows
source .venv/Scripts/activate
#linux
source .venv/bin/activate
```

**Install dependencies**
```
pip install -r app/requirements.txt
```

### Run FastAPI App
```
uvicorn app.main:app --reload
```

### Build Docker Image

```
docker build -t staff-promotion-api .
```

### Run Docker Image
```
docker run -p 9000:80 -e PORT=80 -e API_KEY="xxxx" staff-promotion-api
```

### Deploy to Google Cloud Run

#### Requirements
* Google cloud account
NOTE: Ensure you have billing

Steps
1. On your Google cloud create a new project
2. Under this project go [Cloud Run](https://cloud.google.com/run?hl=en)
3. Click Create service to display the Create service form
    * In the form,
    * Select Continuously deploy new revisions from a source repository.
    * Click Set up with Cloud Build.

4. In the right panel
    * Click Enable Cloud Build API.
    * Under Repository, select the newly created repository.
    * Check the confirmation agreement about GitHub and Google Cloud interactivity.
    * Click Next.
    * Under Build Type, select Dockerfile.
    * Click Save.
5. In the "Create service" form,
    * Confirm the name of the service. It will be automatically populated with the repository name.
    * In the Region pulldown menu, select the region where you want your service located.
    * Under Authentication, select Allow unauthenticated invocations.
    * Expand the Container tap 
    * Select 1GB for container 
    * Also add the API_KEY on the environmental variable tab
    * Click Create to deploy the sample repository to Cloud Run and wait for the deployment to finish.
6. When the deployment is finished you should find the URL for API under service detail in your cloud Run home page.

