# Simple Leaderboard Server

![image](https://github.com/eternity336/Leaderboard/blob/main/screenshot/ScreenshotLeaderboard.png)


Intended as a simple Leaderboard server.  This is not inherently secure and I would not advise making this public facing.  However it will work great internally.  It was built with Python, HTML, JQuery and Javascript.
---

Currently this allows you to:
- Monitor Players/Teams Scores
- Push Scores via an API

---
To push player data to server use a post

    curl --location 'localhost:8000/update_players' --header 'Content-Type: application/json' --data '["joshua, 100","john, 316","sam, 56"]'


---LINUX---

I deployed using gunicorn and developed this using the latest python3.11.
So make sure you have python3 install and install the requirements.txt using

    pip install -r requirements.txt

and then add the systemd config /etc/systemd/system/leaderboard.service

    [Unit]
    Description=Leaderboard Service
    After=network.target

    [Service]
    User=username
    ExecStart=/bin/gunicorn -b 0.0.0.0:8000 app:app  <-- Make sure this location is correct
    WorkingDirectory=/path/to/app/ <-- Working directory of app
    ExecReload=/bin/kill -s HUP $MAINPID
    KillMode=mixed
    TimeoutStopSec=5
    Restart=always

    [Install]
    WantedBy=multi-user.target

Once you set the config in place you enable and start it

    sudo systemctl enable leaderboard.service
    sudo systemctl start leaderboard.service

You can check the process status via

    sudo systemctl status leaderboard.service

And restart via

    sudo systemctl restart leaderboard.service

Then you can access the site with 
    
    http://< serverIP >:< port >

If you want a different port then 8000 just add the port to the above config after 0.0.0.0 with :port

---DOCKER---

A Docker Compose setup is included to run the application in a containerized environment. To use it:

1. Make sure you have Docker and Docker Compose installed
2. Navigate to the project directory containing `docker-compose.yml` and `Dockerfile`
3. Run `docker-compose up` to build and start the container
4. The application will be accessible at http://localhost:8080

The Docker setup uses:
- Python 3.9 slim image
- Gunicorn as WSGI server (as specified in requirements.txt)
- Port 5000 exposed for the Flask application
- Volume mounting for development (code changes reflected immediately)

---WINDOWS---

Make sure to pip install the requirements_windows.txt
and then run with waitress since gunicorn doesn't work on Windows.

    waitress-serve --listen=*:8000 app:app

### Configuration

To configure the leaderboard, you can use a YAML file named `config.yaml`. Here is an example configuration:

```yaml
leaderboard:
  tasks:
    - name: task_1
      weight: 20
    - name: task_2
      weight: 30
    - name: task_3
      weight: 50
```

### Usage

To push player data to the server, use the following cURL command:

```bash
curl --location 'localhost:8000/update_players' --header 'Content-Type: application/json' --data '["joshua, 100","john, 316","sam, 56"]'
```

### Running Locally

To run the application locally:

- Install Python 3.9
- Install dependencies using `pip install -r requirements.txt`
- Start the server using Gunicorn: `gunicorn --bind 0.0.0.0:8000 app:app`

### Docker Setup

For a Docker-based setup:

1. Ensure you have Docker and Docker Compose installed.
2. Navigate to your project directory containing `docker-compose.yml` and `Dockerfile`.
3. Run `docker-compose up` to build and start the container.

The application will be accessible at http://localhost:8080

---REFERENCES---

Font from 

https://www.1001fonts.com/saiba-45-font.html
```