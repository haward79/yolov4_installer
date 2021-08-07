#!/bin/bash

echo 'Usage :'
echo '# Detect objects in image'
echo './darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights'
echo ''
echo '# Detect objects in video stream'
echo '# Replace trailing 0 to your camera id'
echo './darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights -c 0'
echo ''
echo '# Run customed script'
echo 'python3 main.py'
echo ''
echo '# Get connected camera list'
echo 'v4l2-ctl --list-devices'
echo ''
echo '# Get more info from https://github.com/AlexeyAB/darknet'
echo ''

