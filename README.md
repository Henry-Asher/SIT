readme for social interaction test analysis -- Henry Asher -- 04/22/24


- deeplabcut generated CSV files are in these folders on the NAS: 

- Test Cohort: "\\SHANE-NAS\data\Behavior_Data\Cohort11_optoTMS_DREADDs\Stress_Cohort\SIT"

- Cohorts 11A/B/C/D: "\\SHANE-NAS\data\Behavior_Data\Cohort11_optoTMS_DREADDs\new\SIT\raw videos  and dlc_csv"


**IMPORTANT: 
The videos of the test cohort and cohort 11ABCD were taken with a different camera position. As a result, in the analysis functions, the values of relevant variables (i.e., location of the chamber boundaries) is different between the test cohort and the full cohort. However, the camera is position across all Cohort11ABCD videos.  

The values of the different b oundary variables were obtained through taking a screenshot of the video frame (you can also extract a single frame from the video), opening it in imageJ, and obtaining the (x,y) pixel values of the locations in question. 

Apparatus dimensions:
- entire arena: 60cm x 40.5cm
- each chamber: 20cm x 40.5cm
- cylinder: diameter 10cm, height 20cm

Analysis information:

All python functions used to analyze data are here on Github: 
https://github.com/Henry-Asher/SIT/tree/main

please reference this notebook to see how to call the master function to analyze the data: https://github.com/Henry-Asher/SIT/blob/main/cohort11A.ipynb


COHORT 11ABCD specific variables
	# cohort 11A/B/C/D videos
	midpoint_x = 345 #to divide mouse position into 4 quadrants
	midpoint_y = 268
	midchamber_right_boundary = 252
	midchamber_left_boundary = 420

COHORT STRESS/TEST specific variables
	# test cohort videos
	midpoint_x = 1042 #to divide mouse position into 4 quadrants
	midpoint_y = 595
	midchamber_right_boundary = 919
	midchamber_left_boundary = 1154


Other global variables: 

length of habituation period: 5 minutes (I think variables are set to 4 min and 59 seconds)
length of testing period: 5 minutes (I think variables are set to 4 min and 59 seconds)
