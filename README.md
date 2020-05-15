# Dave

Dave is a desktop application that aims to measure user’s emotion and heart rate by
taking periodic video samples from user’s webcam. Dave generates analysis reports
containing statistical information on user’s emotion and heart rate in the last period and
notifies the user to take a rest if he looks tired or has abnormal heart rate.

#### Note: Heart rate is not supported yet

#### You must first download the deep learning model and put it in the main directory

Link to download the Valence-Arousal model:  
https://drive.google.com/file/d/1sdMy0Fu8tghjmLOu59NOr-fhJidlIV2l/view?usp=sharing  

### Demo

The application opens the camera every period specified by the user and captures the frames for 15 sec then the model measures the valence and arousal in the captured frames and based on that user's mood is determined. when the calculations are finished, a report is generated provide the user with some stats.

Note: We didn't have time to merge user's reaction video and screen recorder video so we uploaded only the screen recorder video [here](https://www.youtube.com/watch?v=L8ID1zTPTeQ&fbclid=IwAR10HsNnx8KPP9w79QH1M0PU95ZSdwW7d3RPqveFsafKFQKBrYxmgOO5X7g).

### Team Members:

Code          | Name	     | Section
------------- | -------------| -------------
1500913  | Omar Fathy | 2
1500927  | Omar Shafik | 2
1500948  | Amr Hossam | 2
