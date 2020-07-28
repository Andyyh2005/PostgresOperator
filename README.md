# Create a custome Postgres Operator
This blog makes a quick overview of developing a custom PostgreSQL client python operator for SAP Data Intelligence 3.0.
For more details on how to develop a custom operator, please read the blog by  [Jens Rannacher](https://blogs.sap.com/2018/01/23/sap-data-hub-develop-a-custom-pipeline-operator-with-own-dockerfile-part-3/)

## 1. Create a Dockerfile
The custom Postgres operator requires python library [Psycopg2](https://www.psycopg.org/) which is a PostgreSQL database adapter for Python. To use it, we need a custom Docker image that provides Python with that library. You can refer [creating dockerfiles](https://help.sap.com/viewer/aff95eebc2e04c44816e6ff0d21c3c88/3.0.latest/en-US/62d1df08fa384d0e88bbe9b7cbd2c3fb.html) for the detailed steps. 
- Open the **Repository** tab in the SAP Data Intelligence Modeler, navigate to the **dockerfiles** section, right-click and click on **Create Docker File**:
- Type in a **Name** for the Docker File, in our case we type "demo/psycopg2" and click **OK**: