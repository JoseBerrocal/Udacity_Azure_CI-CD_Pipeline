import time
from locust import HttpUser, task, between, TaskSet

class MyTaskSet(TaskSet):
    @task
    def launch_Url(self):
        self.client.get("/")

class MyLocust(HttpUser):
    tasks = [MyTaskSet]
    min_wait = 1000
    max_wait = 5000

    host =  "https://azure-cicd-pipeline1.azurewebsites.net"