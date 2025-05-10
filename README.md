# JetCert 🚀

In this Artifact, we have implemented a framework called JetCert. Additionally, we have implemented a self-adaptive system using JetCert, which we will proceed to install and run in the following steps.

## Getting Started Guide
To install and set up this self-adaptive system, you only need to have Docker installed on your system. You can install Docker using [this link](https://www.docker.com/)

After installing Docker on your system, pull jetcert image using the command below:
```bash
docker pull armanheids/jetcert
```
After pulling the JetCert image, you can begin running and testing the self-adaptive system.


## Step-by-Step Instructions
After successfully completing the steps in the Getting Started Guide, you should first create a container from the JetCert image:
```bash
docker run --name jetcert_container -it armanheids/jetcert
```
After executing the above command, a container from the JetCert image will be created and it will log the execution stages of the self-adaptive system for you through the terminal.

The general structure of the log is as follows:
```python
start MAPE round [period number]
[log 1]
[log 2]
...
[log n]
start MAPE round [period number]
```
The period of each MAPE iteration is 16 seconds, meaning that the process of writing logs for each MAPE iteration takes 16 seconds. We appreciate your patience.

After the following logs are displayed in the terminal:
```python
2025-04-29 10:15:23 [INFO] - Parsing <Module cryptography> was successful.
2025-04-29 10:15:25 [INFO] - Parsing <Module physics> was successful.
2025-04-29 10:15:25 [INFO] - Parsing <Module login> was successful.
2025-04-29 10:15:25 [INFO] - Parsing <Module finance> was successful.
2025-04-29 10:15:25 [INFO] - Parsing 4 modules successfully.

2025-04-29 10:15:25 [INFO] - start MAPE round 0
2025-04-29 10:15:25 [INFO] - <Module cryptography in version triple_des>
2025-04-29 10:15:25 [INFO] - <Module physics in version numba_njit_array_optimized>
2025-04-29 10:15:25 [INFO] - <Module login in version safe_basic_auth>
2025-04-29 10:15:25 [INFO] - <Module finance in version numpy_optimized>
2025-04-29 10:15:25 [INFO] - Serving on http://127.0.0.1:5000
```

you can run the unit tests of the self-adaptive system using the command below to evaluate its correct execution:
```bash
docker exec -it jetcert_container python3 /home/self-adaptive-system/tests
```

After traversing 3 cycles of MAPE, the experiments are generated in the directory /home/self-adaptive-system/main/modules/__jetcert__ of the Docker container. You can copy and view these experiments from the Docker container to your system using the command below:
```bash
docker cp jetcert_container:/home/self-adaptive-system/main/modules/__jetcert__ [your_system_path]/jetcert_experiments
```
In the above command, replace [your_system_path] with the path where you want the JetCert experiments to be copied.

You can also access the experiments through this method:
```bash
docker exec -it jetcert_container bash
cd /home/self-adaptive-system/main/modules/__jetcert__
ls -la
```

To view the complete source code of the project, you can use [this GitHub link](https://github.com/armanheidarii/JetCert).
