import cv2
import os
import pandas as pd
from deepface import DeepFace
from .models import User

model_name = 'Facenet'



base_dir = os.path.dirname(os.path.dirname(__file__))
dataset = os.path.join(os.path.dirname(__file__), 'dataset')

def compareFace(username):
	global model_name

	try:
		cam = cv2.VideoCapture(0) # 0 -> index of camera
		if cam.isOpened():
			pass
		else:
			return None
		s, img = cam.read()
		saveimg = os.path.join(base_dir,"{}\{}\{}".format('media', 'temp_storage', 'temp_face.jpg'))

		if s:    # frame captured without any errors
			cv2.namedWindow("cam-test", cv2.WINDOW_NORMAL)
			cv2.imshow("cam-test",img)
			cv2.waitKey(1)
			cv2.destroyWindow("cam-test")
			cv2.imwrite(saveimg,img)
	except:
		return None

	comparison_path = os.path.join(dataset, '{}.jpg'.format(username))

	result = DeepFace.verify(saveimg, comparison_path, model_name=model_name).get('verified')
	os.remove(saveimg)

	return result


def captureFace(username):
	global model_name
	usernames = [user.username for user in User.objects.all()]

	cam = cv2.VideoCapture(0)   # 0 -> index of camera
	if cam.isOpened():
		pass
	else:
		return 0, None 
	s, img = cam.read()
	saveimg = os.path.join(base_dir,"{}\{}\{}".format('media', 'temp_storage', '{}.jpg'.format(username)))

	if s:    # frame captured without any errors
		cv2.namedWindow("cam-test", cv2.WINDOW_NORMAL)
		cv2.imshow("cam-test",img)
		cv2.waitKey(1)
		cv2.destroyWindow("cam-test")
		cv2.imwrite(saveimg,img)

		new_face = os.path.join(dataset, '{}.jpg'.format(username))
		for un in usernames:
			if un != username:
				comparison_path = os.path.join(dataset, '{}.jpg'.format(un))

				result = DeepFace.verify(saveimg, comparison_path, model_name=model_name).get('verified')
				if result is True:
					return 1, saveimg
		
		os.remove(saveimg)
		cv2.imwrite(new_face,img)
		return 0, new_face


def getUsers(url):
	global model_name
	usernames = [user.username for user in User.objects.all()]
	img_path = os.path.join(base_dir,"{}\{}\{}".format('media', 'posts', url[13:]))

	users = []

	for un in usernames:
		comparison_path = os.path.join(dataset, '{}.jpg'.format(un))

		result = DeepFace.verify(img_path, comparison_path, model_name=model_name).get('verified')
		if result is True:
			users.append(un)
	return users		
	
