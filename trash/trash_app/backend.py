import os
from inference_sdk import InferenceHTTPClient
import cv2
from time import sleep

COMPOST = ["BIODEGRADABLE","CARDBOARD","PAPER"]
RECYCLABLE = ["GLASS","METAL","PLASTIC"]

CLIENT = InferenceHTTPClient(
   api_url="https://detect.roboflow.com",
   api_key="QK1mQ4OGvf93llz7n3Ub"
)

prev_items = []

def main():
   output=""
   cap = cv2.VideoCapture('http://10.112.190.88:4747/video')
   ret, frame = cap.read()

   if ret:
      cv2.imwrite("frame.jpg", cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
      sleep(0.1)
      result = CLIENT.infer("frame.jpg", model_id="trashclass-zuu3r/1")
      if result["predictions"]:
         items = []
         res = result["predictions"]
         for obj in res:
            items.append(obj["class"])
            if obj["class"] not in prev_items:
               if obj["class"] not in COMPOST:
                  output = "You put %s into compost, which should go in the recycle!" % obj["class"]
                  cam = cv2.VideoCapture(0)
                  s, img = cam.read()
                  if s:
                     cv2.imwrite("victim.jpg", img)
         # print(items)
         prev_items = items
   return output