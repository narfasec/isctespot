<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<br />
<div align="center">
  <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fconhecimentoinovacao.iscte-iul.pt%2F&psig=AOvVaw0-uupha0N7JwPwGMv9M4kQ&ust=1725037244802000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOje-tLWmogDFQAAAAAdAAAAABAE" alt="Logo" width="80" height="80">

  <h3 align="center">IscteSpot</h3>

  <p align="center">
    A Damn vulnerable SaaS application for ISCTE - Software and Application Security
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is targeted to the students of ISCTE that are enlisted in Software and Application Security course subject.
The students will use this project to understand the implications of security in modern web applications and understand the risks on the business level.

## Getting Started

There are 2 options to run the application, you can use Docker or you can install and run it locally. Below there will be 2 sections with installation steps for both cases.
First you can git clone this project to your desired location:
   ```sh
   git clone https://github.com/narfasec/isctespot.git
   ```
### Docker (Quick start)

[Install Docker](https://docs.docker.com/engine/install/), if not installed in your system.
* After installing docker, make sure docker deamon is running (opening the desktop app of Docker is enough)
* Change directory to iscte_spot and execute docker compose to build and start the project
  ```
  cd iscte_spot/
  docker-compose up --build
  ```
* Execute the setup script (**setup.ps1** for windows, **setup.sh** for Mac and Linux) to populate the database with testing data.
  ```
  .\setup.ps1
  ```
* At this stage your app should be ready. You can run health checks to check if everything is in order. You can go to you browser and paste **http://localhost:5173** and see the application interface.
  ```
  docker exec project-server-1 python /app/tests/health_checks/test_flow_1.py
  ```

## Local Setup (Optional)

_Below are the steps to setup the project on your local environment. This is also the developer setup, with this setup you can easily make changes and debug issues._

### Requirements
* python 3.9 https://www.python.org/downloads/
* node 18 https://nodejs.org/dist/v18.16.0/node-v18.16.0-x64.msi (Windows) | `brew install node 18.16` (Mac OS)
* mariadb community https://mariadb.com/downloads/
### Installation
* Change directory to iscte_spot and start by installing the frontend
  ```
  cd iscte_spot/frontend/admin-one-vue-tailwind-master
  npm install
  ```
* Change directory to server and install the python requirements
  ```
  cd iscte_spot/server
  python install -r requirements.txt
  ```
### Run application
* open one terminal to execute the frontend
  ```
  cd iscte_spot/frontend/admin-one-vue-tailwind-master
  npm run dev
  ```
* open another terminal to execute the server
  ```
  cd iscte_spot/server
  python appserver.py
  ```
* execute setup script according to your system (**setup.ps1** for windows, **setup.sh** for Mac and Linux)
* execute health checks to check if everything is in order
  ```
  cd iscte_spot/server
  python .\tests\health_checks\test_flow_1.py
  ```
  
### Built With

* python
* Flask
* Vue
* Mariadb
  
## ⚠️ WARNING!
This is a vulnerable application, don't use it for real life scenario and specially don't expose it to the internet, it may compromise your systems
