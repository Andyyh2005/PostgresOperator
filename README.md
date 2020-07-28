# Create a custome Postgres Operator
This blog makes a quick overview of developing a custom PostgreSQL client python operator for SAP Data Intelligence 3.0.
For more details on how to develop a custom operator, please read the blog by  [Jens Rannacher](https://blogs.sap.com/2018/01/23/sap-data-hub-develop-a-custom-pipeline-operator-with-own-dockerfile-part-3/)

## 1. Create a Dockerfile
The custom Postgres operator requires python library [Psycopg2](https://www.psycopg.org/) which is a PostgreSQL database adapter for Python. To use it, we need a custom Docker image that provides Python with that library. You can refer [creating dockerfiles](https://help.sap.com/viewer/aff95eebc2e04c44816e6ff0d21c3c88/3.0.latest/en-US/62d1df08fa384d0e88bbe9b7cbd2c3fb.html) for the detailed steps. 
- Open the **Repository** tab in the SAP Data Intelligence Modeler, navigate to the **dockerfiles** section, right-click and click on **Create Docker File**:

![](images/dockerfileChooseFolder.png)

- Type in a **Name** for the Docker File, in our case we type "demo/psycopg2" and click **OK**:

![](images/dockerfileCreateDockerfile.png)


A new tab opens where you can describe the details of the Dockerfile.
- In the Code Editor, paste the following Dockerfile instructions:

```
FROM python:3.6.4-slim-stretch

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install psycopg2==2.8.5
RUN pip3 install tornado==5.0.2
RUN apt-get autoremove -y gcc

# Add vflow user and vflow group to prevent error
# container has runAsNonRoot and image will run as root
RUN groupadd -g 1972 vflow && useradd -g 1972 -u 1972 -m vflow
USER 1972:1972
WORKDIR /home/vflow
ENV HOME=/home/vflow
```

Next, provide tags for the Docker image to describe its properties:
- Open the Docker File Configuration Pane by clicking on the icon in the upper right corner:

![](images/dockerfileOpenTag.png)

- Add new **Tags** by clicking on the "**+**" icon:

![](images/dockerfileAddTags.png)

- Add the **Tag** "python36": We use this tag to declare that our Docker image includes Python version 3.6.
- Add the **Tag** “tornado” with version 5.0.2 as this is required by the updated Python Subengine.
- Add the **Tag** “psycopg2” with version 2.8.5: We use this tag to declare that the Python library psycopg2 is available in the Docker image.
- Save the Dockerfile by clicking on Save in the upper right corner:

![](images/dockerfileSave.png)

- Build the Docker Image by clicking on the Build icon in the upper right side:

![](images/dockerfileBuild.png)

You can monitor the status of the Docker build process from the Log tab in the bottom pane: