![Python application test with Github Actions](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/workflows/Python%20application%20test%20with%20Github%20Actions/badge.svg)

# Udacity_Azure_CI-CD_Pipeline
We will test the creation of the pipeline
 
The prove the github action was successful

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/github_action_build.png "GitHub Action Passed")

# Overview

There are two components to this project: CI (Continuous Integration) and CD (Continuous Delivery).

In this project, you will build a Github repository from scratch and create a scaffolding that will assist you in performing both Continuous Integration and Continuous Delivery. You'll use Github Actions along with a Makefile, requirements.txt and application code to perform an initial lint, test, and install cycle. Next, you'll integrate this project with Azure Pipelines to enable Continuous Delivery to Azure App Service.

This project will give you an opportunity to demonstrate your ability to perform continuous delivery for a Python-based machine learning application using the Flask web framework. You will apply the skills you have acquired in this course to operationalize a Machine Learning Microservice API.

You are given a pre-trained, sklearn model that has been trained to predict housing prices in Boston according to several features, such as average rooms in a home and data about highway access, teacher-to-pupil ratios, and so on. You can read more about the data, which was initially taken from Kaggle, on the data source site. This project tests your ability to operationalize a Python flask app—in a provided file, app.py—that serves out predictions (inference) about housing prices through API calls. This project could be extended to any pre-trained machine learning model, such as those for image recognition and data labeling.

## Project Plan

* [Trello board for the project](https://trello.com/b/cdioDvZb/building-a-ci-cd-pipeline)
* [Spreadsheet Original and Final Project](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/Template-Project-Planning.xlsx)

## Instructions

* Architectural Diagram 
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/Architectural_Diagram.jpg)

<TODO:  Instructions for running the Python project.  How could a user with no context run this project without asking you for any help.  Include screenshots with explicit steps to create that work. Be sure to at least include the following screenshots:


### 1. Running the application in a standalone environment

After cloning the repo it is required to create a virtual environment with the following commands
```bash
git clone https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline.git

python3 -m venv ~/.udacity-devops
source ~/.udacity-devops/bin/activate
```
Now it is required to dowload the prebuilt binary`hadolint`, and put it in `~/.udacity-devops/bin/`
```bash
sudo wget -O ~/.udacity-devops/bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.17.5/hadolint-Linux-x86_64 && sudo chmod +x ~/.udacity-devops/bin/hadolint
```
To prepare the environment and test the files, we can make use of the `Makefile`
```bash
make all
```
The output must as the following
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_make_all.png "make all")

To run ML locally it will require to do some adjusments in the code

First in `app.py` "clf" must exist before "app.run" as the following:
```python
    scaled_payload = scale(inference_payload)
    #clf = joblib.load("./model_data/boston_housing_prediction.joblib")
    prediction = list(clf.predict(scaled_payload))
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    # load pretrained model as clf
    clf = joblib.load("./model_data/boston_housing_prediction.joblib")
    app.run(host='0.0.0.0', port=8000, debug=True) # specify port=80
```
Then `make_prediction.sh` must have enable the port 8000 and the IP must change to `0.0.0.0` as the following:
```python
#!/usr/bin/env bash

PORT=8000
echo "Port: $PORT"
.
.
     -H "Content-Type: application/json" \
     -X POST http://0.0.0.0:$PORT/predict
```
Now you can execute the following commands to make the prediction
```bash
python app.py
#Run the script in a new terminal
sh make_prediction.sh
```

### 2. Running the application in a docker

All the same preparations as in 1. need to be executed, the only difference is:

Then `make_prediction.sh` must have enable the port 9000, this port was configured to reach the app in the docker container,  and the IP must change to `0.0.0.0` as the following:
```python
#!/usr/bin/env bash

PORT=9000
echo "Port: $PORT"
.
.
     -H "Content-Type: application/json" \
     -X POST http://0.0.0.0:$PORT/predict
```
Now you can execute the following commands to create the docker image, run the docker container and make the prediction
```bash
sh run_docker.sh
#Run the script in a new terminal
sh make_prediction.sh
```
If the creation of the docker image and the running of the docker container was successful the following output will appear
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_locally_docker.png)

### 3. Running the application in Azure App Service

Firts we need to clone the app in the [Azure Cloud Shell](https://shell.azure.com/)
```bash
git clone https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline.git
```
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_clone_azure_cloud_shell.png)

As part of the requirents of the project I will modify Makefile to run "make all" command  considering hello.py and test_hello.py files

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_azure_shell_make_all.png)

To deploy the application in the App Service execute the following, in this case the App Service name will be "azure-cicd-pipeline" and will be located in westus2
```bash
#Option 1
sh commands.sh
#Option 2
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
az webapp up --sku F1 -n azure-cicd-pipeline --location westus2
```
The following output is expected:

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_deploy_App_Service.png)

Search of the deployed app in the App Service and select Browser

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_app_service.png)

We can observe the app is running

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_app_service_sklearn_browser.png)

The we need to run the following command
```bash
sh make_prediction.sh
```
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_azure_shell_make_prediction.png)

A small testing can be do using Locust
```bash
locust -f locustfile.py
```
You can get the following output

![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_locust.png)

### 4. Running the application in Azure App Service using Azure DevOps

For this purpose it is required to execute the following steps:

Create and AzureDevOps Project. Only follow the steps [Prerequisites and Create a project](https://docs.microsoft.com/en-us/azure/devops/organizations/projects/create-project?view=azure-devops&tabs=preview-page)

Then is neccesarry to stablish a conneccion between the [App Service and the Devops Project and authorize continuous deployment](https://docs.microsoft.com/en-us/azure/app-service/deploy-continuous-deployment). For the Source Control select GitHub, for the build provider select Azure Pipeline. In the Configure part select the ci-cd_pipeline repo and for the Build select the project you created and any Web App Framework, later after executing azure-pipelines.yml this will change to python due to "runtimeStack: 'PYTHON|3.7'" in "task: AzureWebApp@1".
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_app_service_deploymet_center.png)


Enter the Azure DevOps Project, select the project, select the pipeline and run the pipeline
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_devops_project_pipeline.png)

The expected output:
![alt text](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_devops_project_pipeline_logs.png)

Then we need to run the following command, can be executed either from the Azure Cloud Shell or your local machine
```bash
sh make_prediction.sh
```

## Enhancements

To improve the project will be good to have more detailed explanation on what steps to execute on the documents provided. That will help in the development of the project. And for new topics will be good to add material, for example gunicorn.

## Demo 

Please click on the images to see the videos

Part 1:

[![screencast screenshot](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_demo_part1.png)](https://youtu.be/faU-M6ktlAQ)

Part 2:

[![screencast screenshot](https://github.com/JoseBerrocal/Udacity_Azure_CI-CD_Pipeline/blob/master/images/cicdpipeline_demo_part2.png)](https://youtu.be/0Vtifi9GIqM)