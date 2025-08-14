# Simple Leaderboard Server

![image](https://github.com/eternity336/Leaderboard/blob/main/screenshot/ScreenshotLeaderboard.png)


Intended as a simple Leaderboard server. This is not inherently secure and I would not advise making this public facing. However it will work great internally. It was built with Python, HTML, JQuery and Javascript.

## Features

- Monitor Players/Teams Scores
- Push Scores via an API

## Docker Setup

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

## Usage

To push player data to the server use a POST request:

```bash
curl --location 'localhost:8000/update_players' --header 'Content-Type: application/json' --data '["joshua, 100","john, 316","sam, 56"]'
```

## Linux Setup

I deployed using gunicorn and developed this using Python 3.11.
So make sure you have Python 3 installed and install the requirements.txt using:

```bash
pip install -r requirements.txt
```

Then add the systemd config `/etc/systemd/system/leaderboard.service`:

```ini
[Unit]
Description=Leaderboard Service
After=network.target

[Service]
User=username
ExecStart=/bin/gunicorn -b 0.0.0.0:8000 app:app
WorkingDirectory=/path/to/app/
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

Once you set the config in place, enable and start it:

```bash
sudo systemctl enable leaderboard.service
sudo systemctl start leaderboard.service
```

You can check the process status via:

```bash
sudo systemctl status leaderboard.service
```

And restart via:

```bash
sudo systemctl restart leaderboard.service
```

Then you can access the site with:

```
http://<serverIP>:<port>
```

If you want a different port than 8000, just add the port to the above config after `0.0.0.0` with `:<port>`.

## Windows Setup

Make sure to pip install the requirements_windows.txt:

```bash
pip install -r requirements_windows.txt
```

Then run with waitress since gunicorn doesn't work on Windows:

```bash
waitress-serve --listen=*:8000 app:app
```

## Configuration

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

## Running Locally

To run the application locally:

1. Install Python 3.9
2. Install dependencies using `pip install -r requirements.txt`
3. Start the server using Gunicorn: `gunicorn --bind 0.0.0.0:8000 app:app`

## References

Font from [https://www.1001fonts.com/saiba-45-font.html](https://www.1001fonts.com/saiba-45-font.html)
```