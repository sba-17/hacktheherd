from django.shortcuts import render
from inference_sdk import InferenceHTTPClient
import cv2
from time import sleep
import os
import playsound

try:
   os.remove("./trash_app/static/frame.jpg")
except:
   pass
try:
   os.remove("./trash_app/static/photo.jpg")
except:
   pass

COMPOST = ["BIODEGRADABLE","CARDBOARD","PAPER"]
RECYCLABLE = ["GLASS","METAL","PLASTIC"]

CLIENT = InferenceHTTPClient(
   api_url="https://detect.roboflow.com",
   api_key="QK1mQ4OGvf93llz7n3Ub"
)

global prev_items
prev_items = []
global prev_output
prev_output = ""

def main():
   output=""
   global prev_items
   cap = cv2.VideoCapture('http://10.112.190.88:4747/video')
   ret, frame = cap.read()

   if ret:
      cv2.imwrite("./trash_app/static/frame.jpg", cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
      sleep(0.1)
      result = CLIENT.infer("./trash_app/static/frame.jpg", model_id="trashclass-zuu3r/1")
      print(result)
      if result["predictions"]:
         items = []
         res = result["predictions"]
         for obj in res:
            if obj["confidence"] > 0.5:
               items.append(obj["class"])
               if obj["class"] not in prev_items:
                  if obj["class"] not in COMPOST:
                     # playsound.playsound("./sound-effect.mp3", False)
                     output = "You put a %s into compost! Please move it to the recycle!" % obj["class"].lower()
                     cam = cv2.VideoCapture(0)
                     s, img = cam.read()
                     if s:
                        cv2.imwrite("./trash_app/static/photo.jpg", img)
                  if obj["class"] in COMPOST:
                     output = "Good job! You put a %s into compost!" % obj["class"].lower()
            print(items)
         prev_items = items
   return output

# Create your views here.
def index(request):
     global prev_output
     output = main()
     if output != "":
        context = {"text":output}
        prev_output = output
     else:
        context = {"text": prev_output}
     return render(request, "index.html",context)