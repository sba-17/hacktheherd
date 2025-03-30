def clear():
   try:
      os.remove("./trash_app/static/frame.jpg")
   except:
      pass
   try:
      os.remove("./trash_app/static/photo.jpg")
   except:
      pass