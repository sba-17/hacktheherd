from time import sleep
import os
from inference_sdk import InferenceHTTPClient
import cv2
from time import sleep
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response

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
                     cv2.imwrite("./trash_app/static/photo.jpg", img)
         # print(items)
         prev_items = items
   return output

# Create your views here.
@api_view(['GET'])
def index_api(request):
     global prev_output
     output = main()
     if output != "":
        context = {"text":output}
        prev_output = output
     else:
        context = {"text": prev_output}
     return Response(context)