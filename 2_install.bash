#!/bin/bash


owd=$(pwd)


echo '> Create work directory'

mkdir "$HOME/Workspace/yolov4"
cd "$HOME/Workspace/yolov4"

if [[ $? -ne 0 ]]
then
	echo "Failed to chnage directory to '$HOME/Workspace/yolov4'"
	exit 1
fi


echo '> Clone yolov4 project from github'

git clone 'https://github.com/AlexeyAB/darknet.git'
cd darknet

if [[ $? -ne 0 ]]
then
	echo "Failed to chnage directory to $(pwd)/darknet"
	exit 1
fi


echo '> Install OpenCV by apt'
sudo apt install python3-opencv libopencv-dev -y


echo '> Change settings in Makefile'
tmp=$(date +'%Y%m%d_%H%M%S')
cp Makefile "Makefile_$tmp.bak"
sed -i 's/OPENCV=0/OPENCV=1/1' Makefile
sed -i 's/LIBSO=0/LIBSO=1/1' Makefile


echo '> Get number of cpu cores'
numCores=$(cat /proc/cpuinfo | grep processor | sort | wc -l)

if [[ $numCores -gt 0 ]]
then
	echo "$numCores cores available on this computer."
else
	echo 'Failed to retrieve number of cpu cores !'
	exit 1
fi

echo '> make darknet'
make -j "$numCores"

echo '> Download pre-trained module'
wget 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights'

echo '> Copy main.py'
cp "$owd/main.py" .


