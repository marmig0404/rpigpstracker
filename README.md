# RPiGPSTracker

A collection of services to record and view gps data on a Raspberry Pi Zero W.

## Details

This package contains two services, one for recording the GPS data, another for displaying the saved data. The recording is handled by *gps_service.py*, running an SQLite3 database to record data from the serial out of a connected GPS module. To view the data, a simple Flask web server serves a generated plot of the recorded coordinates, handled by *web_service.py*. The web service calls *plot_service.py* to generated a new plot with each http get request, using Plotly.express.

## Installation

### Clone from GitHub and enter directory

    git clone https://github.com/marmig0404/rpigpstracker.git;
    cd rpigpstracker

### Install dependencies

    sudo apt-get install python3-numpy python3-pandas;
    sudo pip3 install plotly

### Setup systemd services

    sudo cp systemd/ /etc/systemd/system; # move service files
    sudo systemctl daemon-reload;
    # enable services for auto-start
    sudo systemctl enable gpstracker.service;
    sudo systemctl enable gpswebviewer.service;
    # start services now
    sudo systemctl start gpstracker.service;
    sudo systemctl start gpswebviewer.service;
    # check service status
    sudo systemctl status gpstracker.service;
    sudo systemctl status gpswebviewer.service;
