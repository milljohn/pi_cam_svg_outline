# Pi Cam

Python application that takes an image, converts it to an outline for CAD modeling. SVG outline.

## Setup

Run ``pip install -r requirements.txt``


### Initial Setup
```shell
sudo apt update && sudo apt upgrade -y```
sudo apt install python3-venv vim libopencv-dev python3-opencv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask opencv-python-headless svgwrite
```

### Automated Setup
Fully automated install of dependencies and creates a systemd service. No need for running any other commands.
```shell
./service/install.sh
```


## Using the API
Run the API
```shell
venv/bin/source/activate
python main.py
```

Access from the command line on the same or different device
```shell
curl http://<raspberry_pi_ip>:5000/capture -o image.svg
```

# System
Tested on Debian 11 Bullseye with a UC-346 (Arducam OV5647) camera module connected via CSI. I couldn't get this to work with Debian 12.

``sudo raspi-config`` Enable legacy Camera support
