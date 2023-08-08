#!/usr/bin/env python3
import cv2
import mediapipe as mp
import time
import pandas as pd
import numpy as np
from servo import Servo
#from sklearn.ensemble import RandomForestClassifier as rfc
from joblib import load

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class Pose_Estimator():


    def __init__(
        self, 
        static_image_mode               = False, #static mode is for images, for videos use 
        model_complexity                = 1, #model complexity may improve accuracy but decrease speed
        enable_segmentation             = True,
        min_detection_confidence        = 0.5):

        self.static_image_mode          = static_image_mode
        self.model_complexity           = model_complexity
        self.enable_segmentation        = enable_segmentation
        self.min_detection_confidence   = min_detection_confidence

        self.mp_draw                    = mp.solutions.drawing_utils
        self.mp_drawing_styles          = mp.solutions.drawing_styles
        self.mp_pose                    = mp.solutions.pose

        self.pose                       = mp_pose.Pose(
                                            static_image_mode=self.static_image_mode,
                                            model_complexity=self.model_complexity,
                                            enable_segmentation=self.enable_segmentation,
                                            min_detection_confidence=self.min_detection_confidence)

    def estimate_pose(self, image, relational = True, draw = False):

        image_rgb           = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert to rgb
        self.results        = self.pose.process(image_rgb) #estimate

        if self.results.pose_landmarks and draw:
        
            self.mp_draw.draw_landmarks(
                image,
                self.results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        return image

    def get_landmark_data(self):

        landmark_names = {	
            "LEFT_ANKLE": mp_pose.PoseLandmark.LEFT_ANKLE,
            "LEFT_EAR":mp_pose.PoseLandmark.LEFT_EAR,	
            "LEFT_ELBOW":mp_pose.PoseLandmark.LEFT_ELBOW,	
            "LEFT_EYE":mp_pose.PoseLandmark.LEFT_EYE,
            "LEFT_EYE_INNER":mp_pose.PoseLandmark.LEFT_EYE_INNER,
            "LEFT_EYE_OUTER":mp_pose.PoseLandmark.LEFT_EYE_OUTER,
            "LEFT_FOOT_INDEX":mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
            "LEFT_HEEL":mp_pose.PoseLandmark.LEFT_HEEL,
            "LEFT_HIP":mp_pose.PoseLandmark.LEFT_HIP,
            "LEFT_INDEX":mp_pose.PoseLandmark.LEFT_INDEX,
            "LEFT_KNEE":mp_pose.PoseLandmark.LEFT_KNEE,	
            "LEFT_PINKY":mp_pose.PoseLandmark.LEFT_PINKY,	
            "LEFT_SHOULDER":mp_pose.PoseLandmark.LEFT_SHOULDER,
            "LEFT_THUMB":mp_pose.PoseLandmark.LEFT_THUMB,	
            "LEFT_WRIST":mp_pose.PoseLandmark.LEFT_WRIST,
            "NOSE":mp_pose.PoseLandmark.NOSE,
            "RIGHT_ANKLE":mp_pose.PoseLandmark.RIGHT_ANKLE,
            "RIGHT_EAR":mp_pose.PoseLandmark.RIGHT_EAR,
            "RIGHT_ELBOW":mp_pose.PoseLandmark.RIGHT_ELBOW,
            "RIGHT_EYE":mp_pose.PoseLandmark.RIGHT_EYE,
            "RIGHT_EYE_INNER":mp_pose.PoseLandmark.RIGHT_EYE_INNER,
            "RIGHT_EYE_OUTER":mp_pose.PoseLandmark.RIGHT_EYE_OUTER,
            "RIGHT_FOOT_INDEX":mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
            "RIGHT_HEEL":mp_pose.PoseLandmark.RIGHT_HEEL,
            "RIGHT_HIP":mp_pose.PoseLandmark.RIGHT_HIP,
            "RIGHT_INDEX":mp_pose.PoseLandmark.RIGHT_INDEX,
            "RIGHT_KNEE":mp_pose.PoseLandmark.RIGHT_KNEE,
            "RIGHT_PINKY":mp_pose.PoseLandmark.RIGHT_PINKY,
            "RIGHT_SHOULDER":mp_pose.PoseLandmark.RIGHT_SHOULDER,
            "RIGHT_THUMB":mp_pose.PoseLandmark.RIGHT_THUMB,
            "RIGHT_WRIST":mp_pose.PoseLandmark.RIGHT_WRIST
            }

        landmark_data = {}

        
        for landmark in landmark_names:

            if self.results.pose_landmarks:

                landmark_data[f"{landmark}_x"]  = [self.results.pose_landmarks.landmark[landmark_names[landmark]].x] 
                landmark_data[f"{landmark}_y"]  = [self.results.pose_landmarks.landmark[landmark_names[landmark]].y]
                landmark_data[f"{landmark}_z"]  = [self.results.pose_landmarks.landmark[landmark_names[landmark]].z]
                landmark_data[f"{landmark}_v"]  = [self.results.pose_landmarks.landmark[landmark_names[landmark]].visibility]  

            else:
                
                landmark_data[f"{landmark}_x"]  = [np.nan]
                landmark_data[f"{landmark}_y"]  = [np.nan]
                landmark_data[f"{landmark}_z"]  = [np.nan]
                landmark_data[f"{landmark}_v"]  = [np.nan]

        return self.pandize(landmark_data)

    def pandize(self, dictionary:dict)->pd.DataFrame:

        df = pd.DataFrame.from_dict(dictionary)
    
        return df
    
    def track_nose(self) -> dict:
        """
        Tracks nose for camera adjustments.
        Returns dict with x,y,z,visibility
        """
        nose        = {}
        if self.results:
            try:
                nose["x"]   = self.results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
            except:
                #print()
                pass
        return nose
    
class Classifier():

    def __init__(self) -> None:
        
        self.model = load('trained_classifier.joblib') 

    def predict(self, X:pd.DataFrame) -> bool:
        
        X           = X.dropna()   #nan values cannot be predicted
        prediction  = 0            #in case there is no prediction
        if X.shape[0] > 0:
            prediction = self.model.predict(X)[0]

        return True if prediction == 1 else False

def run():

    pose_estimator  = Pose_Estimator()
    classifier      = Classifier()
    servo           = Servo()
    cap             = cv2.VideoCapture(0)


    ## CLOCK ##
    previous_time   = 0
    current_time    = 0
    counter         = 0

    while True:

        success, frame = cap.read()
        frame = cv2.flip(frame,1) #mirror
        frame = pose_estimator.estimate_pose(frame)

        text = "not classified"

        lying = classifier.predict(pose_estimator.get_landmark_data()) # classify if lying

        text = "lying" if lying else ("not lying" if not lying else "not classified") 

        cv2.putText(frame, 
            text, 
            (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, 
            (0, 255, 255), 
            2, 
            cv2.LINE_4)

        ### FPS MONITOR ### 
        current_time    = time.time()
        fps             = 1/(current_time-previous_time)
        previous_time   = current_time
        cv2.putText(frame,str(int(round(fps))),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        
        ### PERSON TRACKING ###
        pose_estimator.track_nose()
        if pose_estimator.track_nose():
            pos_diff = (1-pose_estimator.track_nose()["x"])-0.5 # deviation from the center
            if abs(pos_diff) > 0.25:
                angle = np.degrees(np.arctan(pos_diff))
                servo.direction = int(angle / abs(angle))
                
                if counter == 0:
                    servo.set_angle(servo.last_angle + angle/10)
        
        elif pose_estimator.track_nose() == {}:
            servo.swing()
            time.sleep(.5)
        
        cv2.imshow("Image",frame)
        
        counter = 0 if counter == 2 else 1+counter
        
        if cv2.waitKey(1) == ord('q'): # quit by pressing q
            break
        
    cv2.destroyAllWindows()

if __name__ == '__main__':

    run()
