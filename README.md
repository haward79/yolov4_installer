# What's this
This is an installer for [yolo-v4](https://github.com/AlexeyAB/darknet) based on bash.
This script runs with a poor UX, but it works.

yolo is a software for quick object detection based on darknet.  
You can find the installation script for yolov3 from [here](https://github.com/haward79/yolov3_installer).

# Pre-requirements
Please ensure the environment is compatible to run this script.

- Hardware
  - [Raspberry Pi 4 (4GB RAM)](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)

- Software
  - [Ubuntu server 20.04](https://old-releases.ubuntu.com/releases/focal/ubuntu-20.04.1-preinstalled-server-arm64+raspi.img.xz)
  - bash shell

If all things get ready, you can download this project and run *0_main.bash* .
For more information, please reference to *Install section*.

# Usage
1. Download this project.

        git clone 'https://github.com/haward79/yolov4_installer'
        cd yolov4_installer

2. Please ensure the user has privilege to run the scripts.

        chmod u+x *.bash

3. Run the main script  
   Have a cup of coffee and take a rest !

        ./0_main.bash

4. (Optional) Checkout the usage of yolo.

        ./4_usage.bash

# Changelog
- 08/16 2021
    1. Add v4l-ctl checks before executing in scripts/yolov4-realtime.

- 08/07 2021
    1. Add new scripts to install script.

- 07/27 2021
    1. First commit

# Copyright
These scripts are written by [haward79](https://www.haward79.tw/).
They are free to use for both education and business.

