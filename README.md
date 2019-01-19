# VehicleGPS
## Hardware requirements
- Raspberry Pi Model B (2B, 3B, 3B+)
- SD card with Raspbian Stretch Lite installed
- [Adafruit PiTFT 2.8"](https://www.adafruit.com/product/2423)
- u-blox NEO-M8N GPS chip
- GNSS antenna

## How to set up
Plug your SD card into your computer and add a file called `ssh` into the root directory.

Next plug your SD card into the Pi and turn it on.

### Raspberry Pi Configuration
When the Pi has booted, run `sudo raspi-config`, go to `Advanced Options` and then `Expand Filesystem`.

Next go to `Interfacing Options` and select `Serial`. Then select `No` to `Would you like a login shell to be accessible over serial?` and `Yes` to `Would you like the serial port hardware to be enabled?`

### PiTFT Screen Drivers
Install the drivers for the Adafruit PiTFT screen with these commands.

```
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
chmod +x adafruit-pitft.sh
sudo ./adafruit-pitft.sh
```

When running the `adafruit-pitft.sh` file select `3, 1, N, Y` if you are using a capacitive screen.

### Install Openbox and X11
Install a desktop environment to display the VehicleGPS program in.
```
sudo apt-get install xorg openbox
```

### Install Python 3.6
The VehicleGPS code requires Python 3.6. To install:
```
sudo apt-get update
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
sudo make altinstall
```
These last three lines take a few minutes so be patient.

Then clean up the installation and remove unused files.
```
cd ..
sudo rm -r Python-3.6.5
rm Python-3.6.5.tar.xz
sudo apt-get --purge remove build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

sudo apt-get autoremove
sudo apt-get clean


```
Then install packages required by the VehicleGPS program.
```
sudo pip3.6 install pyserial obd geopy RPi.GPIO dropbox python-tk
```

### Edit file `/boot/config.txt`
Add this text to the bottom of the file:
```
enable_uart=1
dtoverlay=pi3-miniuart-bt

dtoverlay=pitft28-capacitive,rotate=90,speed=32000000,fps=20
dtoverlay=pitft28-capacitive,touch-swapxy=true,touch-invx=true
```

### Edit file `.bashrc`
Add this line to the file:
```
startx -- -nocursor
```

TODO: To be continued...
