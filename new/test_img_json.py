import face_recognition
import json
import os

def img2encoding():

    with open("face/face_list.json", "r") as f:
        face_list = json.load(f)
    
    names = []
    images = os.listdir("face/img/")
    for image in images:
        name = image.split('.')[0]
        names.append(name)
        if name in face_list.keys():
            pass
        else:
            name_image = face_recognition.load_image_file(f"face/img/{image}")
            name_encoding = face_recognition.face_encodings(name_image)[0]
            face_list[name] = name_encoding.tolist()
    
    for key, value in list(face_list.items()):
        if key not in names:
            del face_list[key]

    with open("face/face_list.json", "w") as f:
        json.dump(face_list, f, indent=2)

img2encoding()