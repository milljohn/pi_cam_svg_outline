#!/bin/bash

CWD="$(pwd)"
SERVICE="$CWD/py_cam_svg_outline.service"
PARENT="$(dirname $CWD)"
APP_PATH="$PARENT/main.py"
VENV="$PARENT/venv"
PIP="$VENV/bin/pip"
PYTHON="$VENV/bin/python3"
REQUIREMENTS="$PARENT/requirements.txt"
USERNAME="$(who am i | awk '{print $1}')"

SYSTEMD="/etc/systemd/system"


PACKAGES=("python3" "python3-pip" "python3-venv" "python3-opencv" "libopencv-dev")
MISSING_PACKAGES=()


check_install() {
    PACKAGE=$1
    if ! dpkg -l | grep -q "^ii  $PACKAGE "; then
        MISSING_PACKAGES+=($PACKAGE)
    else
        echo "$PACKAGE is already installed."
    fi
}

for PACKAGE in "${PACKAGES[@]}"; do
    check_install $PACKAGE
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "Installing missing packages: ${MISSING_PACKAGES[@]}"
    sudo apt-get update
    sudo apt-get install -y ${MISSING_PACKAGES[@]}

fi

if [ ! -d $VENV ]; then
	echo "Attempting to create venv"
	
	if command -v python3 &>/dev/null; then
		echo "Python 3 is installed, installing venv"
		python3 -m venv $VENV

	else
    		echo "Python 3 is not installed."
		echo "Something has gone terribly wrong..."
		exit -1
	fi
fi


if [ -d $VENV ] && [ -f $REQUIREMENTS ]; then
	echo "Installing requirements.txt"
	$PIP install --upgrade pip
	$PIP install -r $REQUIREMENTS
else
	echo "$VENV does not exist, exiting..."
	exit -1
fi


if [ -f $SERVICE ]; then
	
	echo "Installing $SERVICE"
	
	sed -i "s|WORKINGDIR|$PARENT|" $SERVICE
	sed -i "s|PYTHON|$PYTHON|" $SERVICE
	sed -i "s|APP|$APP_PATH|" $SERVICE
	sed -i "s|pi|$USERNAME|" $SERVICE
	
	echo "Attempting to copy $SERVICE to $SYSTEMD"
	sudo cp $SERVICE $SYSTEMD
	sudo systemctl daemon-reload
	sudo systemctl enable $SERVICE
	sudo systemctl start $SERVICE
fi

