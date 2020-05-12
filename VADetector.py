from mtcnn.mtcnn import MTCNN
from imports.helpers import rect_to_bb, shape_to_np
from imports.facealigner import FaceAligner
import numpy as np
import os

import cv2

# keras
import tensorflow as tf
from keras import backend as K
from keras.models import load_model, Model
from keras.backend.tensorflow_backend import set_session

from losses import ccc, loss_ccc
from metrics import expr_score, f1_score


def init_session():
    config = tf.ConfigProto()
    # dynamically grow the memory used on the GPU
    config.gpu_options.allow_growth = True
    # to log device placement (on which device the operation ran)
    config.log_device_placement = True
    # (nothing gets printed in Jupyter, only if you run it standalone)
    sess = tf.Session(config=config)
    # set this TensorFlow session as the default session for Keras
    set_session(sess)
# init_session


class VADetector:
    def __init__(self):
        init_session()
        path = './weights/t15_affwild2_expr_va_image_weights_200222212717_epoch-29_loss-2.70_class-0.63_0.63_0.42_reg-0.02_0.03_0.05.h5'
        self.model = load_model(path, custom_objects={
            'loss_ccc': loss_ccc, 'ccc': ccc, 'f1_score': f1_score, 'expr_score': expr_score})
        self.detector = MTCNN()
        self.fa = FaceAligner(self.detector)

## capture_period: time the camera is opened in seconds
## return array of two values: valence, arousal
    def __call__(self, capture_period=30):
        fr = 30                         ## frame rate
        frames_left = capture_period * fr
        faces = []
        frames = []
        SIZE = 224
        
        ## open the camera then capture the frames
        cap = cv2.VideoCapture(0)
        while(cap.isOpened() and frames_left > 0):
            ret, frame = cap.read()
            ## only store 10 frames per second
            if frames_left % 3 == 0:
                frames.append(frame)
            frames_left -= 1
        cap.release()

        ## detect and align the main face in each frame then store the faces
        for frame in frames:
            try:
                h, w, d = frame.shape
                detects = self.detector.detect_faces(frame)
                detect = max(detects, key=lambda x: x['confidence'])
                (x, y, w, h) = detect['box']
                faceAligned = self.fa.alignMTCNN(
                    frame, detect['keypoints'], desired_shape=(SIZE, SIZE))
                # faceAligned = cv2.normalize(
                #     faceAligned, None, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                faces.append(faceAligned)
            except Exception as err:
                print(err)
                return [-2, -2]    

            
        faces_np = np.array(faces)
        _, ar_arr, va_arr, _ = self.model.predict(faces_np)
        
        arousal = np.mean(ar_arr)
        valence = np.mean(va_arr)
        
        return [valence, arousal]



# print(VADetector()())
