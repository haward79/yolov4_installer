
from ctypes import *
import random
import os
import cv2
from datetime import datetime
import darknet
import argparse
from threading import Thread
from queue import Queue


def getConstFps():

    return 1


def getConstThresh():

    return 0.25


def args_parser():

    parser = argparse.ArgumentParser(description="Yolo v4 Object Detection")
    parser.add_argument("--cam_index", type=int, default=0, help="Index of camera (default = 0)")
    parser.add_argument("--output_filename", type=str, default="", help="Output video stream to file (default = no output, auto to auto generate filename)")
    parser.add_argument("--draw_output", type=bool, default=True, help="Draw detected objects on the output video")
    parser.add_argument("--weights_file", type=str, default="yolov4-tiny.weights", help="path to weights file")
    parser.add_argument("--config_file", type=str, default="cfg/yolov4-tiny.cfg", help="path to config file")
    parser.add_argument("--data_file", type=str, default="cfg/coco.data", help="path to data file")
    
    return parser.parse_args()


def check_arguments(args):

    if not os.path.exists(args.cam_index):
        raise(ValueError("Invalid camera index {}".format(args.cam_index)))

    if not os.path.exists(args.weights_file):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights_file))))

    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))

    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))


def convert2relative(bbox):

    """
    YOLO format use relative coordinates for annotation
    """

    x, y, w, h  = bbox
    _height     = darknet_height
    _width      = darknet_width

    return x/_width, y/_height, w/_width, h/_height


def convert2original(image, bbox):

    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x       = int(x * image_w)
    orig_y       = int(y * image_h)
    orig_width   = int(w * image_w)
    orig_height  = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


def convert4cropping(image, bbox):

    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_left    = int((x - w / 2.) * image_w)
    orig_right   = int((x + w / 2.) * image_w)
    orig_top     = int((y - h / 2.) * image_h)
    orig_bottom  = int((y + h / 2.) * image_h)

    if(orig_left < 0):
        orig_left = 0

    if(orig_right > image_w - 1):
        orig_right = image_w - 1

    if(orig_top < 0):
        orig_top = 0

    if(orig_bottom > image_h - 1):
        orig_bottom = image_h - 1

    bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

    return bbox_cropping


def video_capture(frame_queue, darknet_image_queue):

    while videoStream.isOpened():
        isRead, frame = videoStream.read()

        # Failed to read from camera.
        if not isRead:
            print('Failed to read frame from camera.')
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height), interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)

    videoStream.release()


def inference(darknet_image_queue, detections_queue):
    
    while videoStream.isOpened():
        if not darknet_image_queue.empty():
            darknet_image = darknet_image_queue.get()
            detections = darknet.detect_image(network, class_names, darknet_image, thresh=getConstThresh())
            detections_queue.put(detections)
            darknet.print_detections(detections, True)
            darknet.free_image(darknet_image)

    videoStream.release()


def drawing(frame_queue, detections_queue):

    random.seed(3)  # Determine bbox colors.
    serialNo = 0
    output_filename = args.output_filename

    if output_filename != '':
        # Set current datetime as video filename.
        if output_filename == 'auto':
            output_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + '.mp4'

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        videoOutputStream = cv2.VideoWriter(output_filename, fourcc, getConstFps(), (darknet_width, darknet_height))
        
    while videoStream.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))

            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            if output_filename != '':
                serialNo += 1

                videoOutputStream.write(image)
                cv2.imwrite('Snapshot/' + str(serialNo) + '.jpg', image)

    videoStream.release()
    videoOutputStream.release()


if __name__ == '__main__':
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)

    args = args_parser()
    check_arguments(args)

    network, class_names, class_colors = darknet.load_network(args.config_file, args.data_file, args.weights_file, batch_size=1)
    darknet_width = darknet.network_width(network)
    darknet_height = darknet.network_height(network)

    videoStream = cv2.VideoCapture(args.cam_index)

    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue)).start()

