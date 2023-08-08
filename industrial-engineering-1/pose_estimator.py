import cv2
import mediapipe as mp
import os
import math
import pandas as pd
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","dataset")


class Pose_Estimator():

    def __init__(
        self, 
        static_image_mode = True, 
        model_complexity = 2, 
        enable_segmentation = True,
        min_detection_confidence = 0.5):

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

    def estimate_pose(self, image, relational = True):

        image_rgb           = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert to rgb
        self.results        = self.pose.process(image_rgb) #estimate

        if self.results.pose_landmarks:
        
            self.mp_draw.draw_landmarks(
                image,
                self.results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        return image

    def create_landmark_data(self) -> dict:

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

        return landmark_data

def resize(image):

    DESIRED_HEIGHT  = 1000
    DESIRED_WIDTH   = 1000

    h, w = image.shape[:2]

    if h < w:
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    return img

def pandize(image_name:str = None, label:int = None, dictionary:dict = None, live_mode = False)->pd.DataFrame:

    df = pd.DataFrame.from_dict(dictionary)
    if not live_mode:
        df["image_name"] = image_name
        df["label"]= label

    return df

def create_csv_from_images():

    label_df        = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","IE1_labeling.xlsx"))

    pose_estimator  = Pose_Estimator()

    for row in range(label_df.shape[0]):

        image_name      = f"{label_df['Image'][row]}.png"
        label           = label_df["Position"][row]

        image           = cv2.imread(os.path.join(data_folder,image_name))
        
        image           = resize(pose_estimator.estimate_pose(image))   

        temp_df         = pandize(image_name,label,pose_estimator.create_landmark_data())

        if row == 0:
            df = temp_df

        else: 
            df = pd.concat([df, temp_df])

        print(row)

    df.to_csv("data/merged.csv",index=False)


    cv2.imshow("Image",image)
    cv2.waitKey(0)

def run_live(video_path = None, webcam_mode = False, classifier = None, record = False):

    pose_estimator  = Pose_Estimator()

    if record:
        frame_width     = 1000
        frame_height    = math.floor(1080/(1920/1000))
        video_cod       = cv2.VideoWriter_fourcc(*'XVID')
        video_output    = cv2.VideoWriter(
                            'captured_video.avi',
                            video_cod,
                            10,
                            (frame_width,frame_height))

    if not webcam_mode:
        
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            frame = resize(pose_estimator.estimate_pose(frame))
            text = "Not classified"

            if classifier:
                try: 
                    df = pandize(dictionary= pose_estimator.create_landmark_data(), live_mode=True)
                    df = df.dropna()
                    if df.shape[0] > 0:
                        classified = classifier.predict(df)[0]
                        text = "lying" if classified == 1 else "not lying"

                except Exception as e:
                    print(e)
                    print(df)
                    break

            cv2.putText(frame, 
                text, 
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
            
            if record:
                video_output.write(frame)
                cv2.imshow('frame',frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        if record:
            video_output.release()
            
        cv2.destroyAllWindows()

if __name__ == '__main__':
    
    #run_live("data/video/1.mp4")
    create_csv_from_images()