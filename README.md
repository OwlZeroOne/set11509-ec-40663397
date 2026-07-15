# Coursework - Share Trader Application

> Mateusz Pasternak\
> 40663397\
> MEng Software Engineering

## Start-Up Instructions

### 1. Start the Docker engine.

To start the docker engine on desktop, simply open the desktop GUI application.

<img src="resources/open-docker.png" alt="open-docker.png" width=400>

### 2. Start the containers.

To start the containers, navigate to the `src` directory. From there, run the following docker command:
```
docker compose up --build
```
<img src="resources/start-containers.png" alt="start-containers.png" width="600">

This should start creating images of all registered microservices.

<img src="resources/start-containers-2.png" alt="start-containers-2.png" width="500">

### Start the GUI Application

To launch and use the application, navigate to the `src/app` and run

```
python main.py
```

This should start a TKinter GUI application from the user login page.

<img src="resources/pages/gui-login.png" alt="gui-login.png" width="500">