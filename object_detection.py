import streamlit as st
from PIL import Image
import cv2
import numpy as np

MODEL = r'D:\Project\model\MobileNetSSD_deploy.caffemodel'
PROTOTXT = r'D:\Project\model\MobileNetSSD_deploy.prototxt.txt'


def process_image(image):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    net.setInput(blob)
    detections = net.forward()
    return detections


def annotate_image(
        image, detections, confidence_threshold=0.5
):
    # loop over the detections
    (h, w) = image.shape[:2]
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            _ = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startx, starty, endx, endy) = box.astype("int")
            cv2.rectangle(image, (startx, starty), (endx, endy), 70, 2)
    return image


st.title('Object Detection For Images')
file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])
if file is not None:
    st.image(file)
    image = Image.open(file)
    image = np.array(image)
    detections = process_image(image)
    processed_image = annotate_image(
        image, detections, confidence_threshold=0.5)
    st.image(processed_image)
