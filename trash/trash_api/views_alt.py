from time import sleep
import os
from transformers import AutoImageProcessor, SiglipForImageClassification
import torch
from PIL import Image
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMPOST = ["Biological", "Cardboard", "Compostable", "Paper"]
NOT_COMPOST = ["Battery", "Clothes", "Glass", "Metal", "Plastic", "Shoes", "Trash"]

# Initialize model and image processor
torch.manual_seed(3)
image_processor = AutoImageProcessor.from_pretrained("rubysmac/compostable-plates-classifier-v0", use_fast=True)
model = SiglipForImageClassification.from_pretrained("rubysmac/compostable-plates-classifier-v0")

global items
items = []
global prev_output
prev_output = ""

# Function to process the image
def main():
    output = ""
    cap = cv2.VideoCapture('http://10.112.190.88:4747/video')
    ret, frame = cap.read()

    if ret:
        cv2.imwrite("./trash_app/static/frame.jpg", cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
        sleep(0.1)
        # Process the image with transformers model
        image = Image.open("./trash_app/static/frame.jpg")
        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        # Model predicts one of the classes
        predicted_class_idx = logits.argmax(-1).item()
        classif = model.config.id2label[predicted_class_idx]
        items.append(classif)
        logger.info(items)
        logger.info(classif)
        # Check if item should be in compost
        if classif not in COMPOST:
            output = "You put %s into compost, which doesn't belong there!" % classif
            cam = cv2.VideoCapture(0)
            s, img = cam.read()
            if s:
                cv2.imwrite("./trash_app/static/photo.jpg", img)

    return output


# API View
@api_view(['GET'])
def index_api(request):
    global prev_output
    output = main()
    if output != "":
        context = {"text": output}
        prev_output = output
    else:
        context = {"text": prev_output}
    return Response(context)