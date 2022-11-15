#file containing functions for analyzing social interaction test DLC data

import numpy as np
import os
import csv

#CONSTANTS
midpoint_x = 345 #to divide mouse position into 4 quadrants
midpoint_y = 268
midchamber_right_boundary = 252
midchamber_left_boundary = 420

# midpoint_x = 1042 #to divide mouse position into 4 quadrants
# midpoint_y = 595
# midchamber_left_boundary = 919
# midchamber_right_boundary = 1154

first_row = 3
likelihood_thresh = 0.9
sniffing_threshold = 120
fps = 30
max_time_in_frames = 30*299  #first 4:59 minutes

mouse_center_x_col = 4
mouse_center_y_col = 5
mouse_center_loss_col = 6
mouse_leftflank_x_col = 10
mouse_leftflank_y_col = 11
mouse_leftflank_loss_col = 12
mouse_rightflank_x_col = 13
mouse_rightflank_y_col = 14
mouse_rightflank_loss_col = 15

# mouse_tail_x_col = 7
# mouse_tail_y_col = 8
# mouse_tail_loss_col = 9

target_x_col = 16
target_y_col = 17
object_x_col = 19
object_y_col = 20

# target_cylinder_x_col = 34 #dont think these are correct, need to fix
# target_cylinder_y_col = 35

# object_cylinder_x_col = 31
# object_cylinder_y_col = 32

def get_obj_and_target_pos(data, midpoint_x, midpoint_y, trgt_csv_x_col = 34, trgt_csv_y_col = 35, obj_csv_x_col = 31, obj_csv_y_col = 32):  

  #returns tuple of strings with position of 1) target chamber and 2) object chamber

  target_xvals = data[:,trgt_csv_x_col]
  target_yvals = data[:,trgt_csv_y_col]

  #this only works for full_test files - could make this a function that reads full text files and just returns mouse chamber position

  if target_xvals[0] > midpoint_x and target_yvals[0] > midpoint_y: 
    target_chamber_pos = 'back left'

  elif target_xvals[0] < midpoint_x and target_yvals[0] > midpoint_y: 
    target_chamber_pos = 'back right'

  elif target_xvals[0] > midpoint_x and target_yvals[0] < midpoint_y: 
    target_chamber_pos = 'front left'  

  elif target_xvals[0] < midpoint_x and target_yvals[0] < midpoint_y: 
    target_chamber_pos = 'front right'

  else:
    print("error")

  obj_x_arr = data[:,obj_csv_x_col]
  obj_y_arr = data[:,obj_csv_y_col]

  if obj_x_arr[0] > midpoint_x and obj_y_arr[0] > midpoint_y: 
    obj_chamber_pos = 'back left'

  elif obj_x_arr[0] < midpoint_x and obj_y_arr[0] > midpoint_y: 
    obj_chamber_pos = 'back right'

  elif obj_x_arr[0] > midpoint_x and obj_y_arr[0] < midpoint_y: 
    obj_chamber_pos = 'front left'  

  elif obj_x_arr[0] < midpoint_x and obj_y_arr[0] < midpoint_y: 
    obj_chamber_pos = 'front right'

  else:
    print("error")

  return target_chamber_pos, obj_chamber_pos

def get_mouse_position(data, fps,
              ft_1_x_col = None, ft_1_y_col = None, ft_1_loss_col = None,
              ft_2_x_col = None, ft_2_y_col = None, ft_2_loss_col = None,
              ft_3_x_col = None, ft_3_y_col = None, ft_3_loss_col = None, 
              analysis_length = 280, likelihood_min = 0):

  #INPUTS - takes coordinates of x value and loss value columns for up to 3 features
  #OUTPUTS - array of mouse x-position 

  frames = fps * analysis_length

  #get data for up to 3 features
  if ft_1_x_col != None: 
    ft_1_xvals = data[:frames,ft_1_x_col]
    ft_1_yvals = data[:frames, ft_1_y_col]
    ft_1_hidden_frames = np.isnan(ft_1_xvals)
    ft_1_loss_vals = data[:frames, ft_1_loss_col]
    ft_1_loss_vals = np.nan_to_num(ft_1_loss_vals) #set cells with NaN (empty cells) to 0
    ft_1_loss_bools = ft_1_loss_vals < likelihood_min


  if ft_2_x_col != None: 
    ft_2_xvals = data[:frames,ft_2_x_col]
    ft_2_yvals = data[:frames, ft_2_y_col]
    ft_2_hidden_frames = np.isnan(ft_2_xvals)
    ft_2_loss_vals = data[:frames, ft_2_loss_col]
    ft_2_loss_vals = np.nan_to_num(ft_2_loss_vals) 
    ft_2_loss_bools = ft_2_loss_vals < likelihood_min

  if ft_3_x_col != None:
    ft_3_xvals = data[:frames,ft_3_x_col]
    ft_3_yvals = data[:frames, ft_3_y_col]
    ft_3_hidden_frames = np.isnan(ft_3_xvals)
    ft_3_loss_vals = data[:frames, ft_3_loss_col]
    ft_3_loss_vals = np.nan_to_num(ft_3_loss_vals)
    ft_3_loss_bools = ft_3_loss_vals < likelihood_min

  start_pos = None
  count = 0

  #if the frame isn't hidden, make it the starting position. 
  #If hidden, check other features.
  #if still hidden, iterate through frames until visible feature is found.  
  while start_pos == None: 
      
    if not ft_1_hidden_frames[count]: 
      start_pos = [ft_1_xvals[count], ft_1_yvals[count]]
    elif not ft_2_hidden_frames[count]:
      start_pos = [ft_2_xvals[count], ft_2_yvals[count]]
    elif not ft_3_hidden_frames[count]:
      start_pos = [ft_3_xvals[count], ft_3_yvals[count]]
    else:
      count += 1
    #print("found mouse starting position on frame " + str(count))
  
  last_visible_frame = start_pos


  pos_arr = start_pos
  #print(pos_arr)

  #if not a hidden frame or a frame with low loss, get mouse's position
  #if conditions not satisfied, check additional features
  #if stlil not satisfied, set position to last visible position
  for frame in range(1,frames):
    if not ft_1_hidden_frames[frame] or not ft_1_loss_bools[frame]: 
      curr_pos = [ft_1_xvals[frame] , ft_1_yvals[frame]]
    elif not ft_2_hidden_frames[frame] or not ft_2_loss_bools[frame]:
      curr_pos = [ft_2_xvals[frame], ft_2_yvals[frame]] 
    elif not ft_3_hidden_frames[frame] or not ft_3_loss_bools[frame]:
      curr_pos = [ft_3_xvals[frame], ft_3_yvals[frame]]
    else:
      curr_pos = last_visible_frame

    pos_arr = np.vstack([pos_arr, curr_pos])
    #pos_arr = np.append(pos_arr,curr_pos)

    last_visible_frame = curr_pos

  return pos_arr

def get_time_in_chambers(pos_arr, fps, trgt_pos, center_right_edge, center_left_edge):

  #INPUTS: 
    # pos_arr -> array of mouse position x coordinates
    # fps     -> frames per second of video
    # trgt_pos -> string of target mouse position (front left, front right, back left, back right)
    # center_left_edge -> x value of left edge of center chamber
    # center_right_edge -> x value of right edge of center chamber

  #OUTPUTS: 
    # tuple of ints with 1) time in target chamber, 2) time in center chamber, and 3) time in object chamber

  fr_left = fr_center = fr_right = 0
  xpos = pos_arr[:,0]
  #print(xpos[:20])
  #print(len(xpos))
  for frame in range(len(xpos)):

    if xpos[frame] < center_right_edge:
      fr_right += 1
    elif xpos[frame] > center_right_edge and xpos[frame] < center_left_edge:
      fr_center += 1
    else: 
      fr_left += 1

  tleft = fr_left / fps
  time_center_chamber = fr_center / fps
  tright = fr_right /fps
    
  if trgt_pos == 'back left' or trgt_pos == 'front left':
    time_trgt_chamber = tleft #swapped these 11/14
    time_obj_chamber = tright
  elif trgt_pos == 'back right' or trgt_pos == 'front right':
    time_trgt_chamber = tright
    time_obj_chamber = tleft
  else:
    print("error")    

  return time_trgt_chamber, time_center_chamber, time_obj_chamber

def get_time_sniffing(pos_arr, full_data_arr, trgt_cyl_x_col, trgt_cyl_y_col,obj_cyl_x_col, obj_cyl_y_col, 
                      trgt_pos, obj_pos, center_right_edge, center_left_edge, fps, sniff_threshold = 120):

  #at any given point, get cartesian x and y position. Then subtract x and y by the center x and y point. 

  cartesian_xpos = pos_arr[:,0]
  cartesian_ypos = pos_arr[:,1]
  
  target_pos_arr = np.asarray([full_data_arr[:,trgt_cyl_x_col], full_data_arr[:,trgt_cyl_y_col]])
  object_pos_arr = np.asarray([full_data_arr[:,obj_cyl_x_col], full_data_arr[:,obj_cyl_y_col]])

  target_pos_xy = np.mean(target_pos_arr, axis = 1)
  object_pos_xy = np.mean(object_pos_arr, axis = 1)

  # print("test mouse first position is: " + str(cartesian_xpos[0]) + ", " + str(cartesian_ypos[0]))
  # print("mean raw target mouse position is: " + str(target_pos_xy))

  polar_xpos = np.abs(cartesian_xpos - target_pos_xy[0]) #fix tomorrow
  polar_ypos = np.abs(cartesian_ypos - target_pos_xy[1])

  distance_arr = np.sqrt(np.square(polar_xpos) + np.square(polar_ypos))

  # print("distance array first element is: " + str(distance_arr[0]))

  in_target_chamber = []

  if trgt_pos == 'back left' or trgt_pos == 'front left':
    #boundary = midchamber_left_boundary
    in_target_chamber = np.where(cartesian_xpos > center_left_edge, True, False)
    # print(in_target_chamber)
    # print(np.count_nonzero(in_target_chamber))
    # print("h")

  elif trgt_pos == 'back right' or trgt_pos == 'front right':
    #boundary = center_right_edge
    in_target_chamber = np.where(cartesian_xpos < center_right_edge, True, False)
    # print(in_target_chamber)
  else:
    print("error")

  #print(in_target_chamber)

  count = 0

  for frame in range(len(distance_arr)):
    if distance_arr[frame] < sniff_threshold and in_target_chamber[frame]:
      count += 1
  
  #print(np.min(distance_arr))
  
  t_sniff = count / fps

  #handscore to see if this is correct

  return t_sniff

def to_excel(data, new_file_name):

#function that writes data to excel

#INPUTS - 
    # data - data to go to csv file
    # filename - full path of new file to create

  #import csv

  f = open(new_file_name, 'w+', newline= '')
  writer = csv.writer(f)
  writer.writerows(data)
  f.close()

  return  

def temp_master(folder_path):

  slash = '\\'

  files = os.listdir(folder_path)
  #print(files)

  results = []
  header = ['mouseID', 'time_trgt_zone', 'time_cntr_zone', 'time_obj_zone', 'sniffing_time']
  results.append(header)

  for file in files:

    full_path = folder_path + slash + file
    data_arr= np.genfromtxt(full_path, delimiter=',', skip_header=first_row)

    target_pos, object_pos = get_obj_and_target_pos(data_arr,midpoint_x, midpoint_y, target_x_col, target_y_col, object_x_col, object_y_col)
    
    mouse_pos_arr = get_mouse_position(data_arr, fps,
                      mouse_center_x_col, mouse_center_y_col, mouse_center_loss_col, 
                      mouse_leftflank_x_col, mouse_leftflank_y_col, mouse_leftflank_loss_col,
                      mouse_rightflank_x_col, mouse_rightflank_y_col, mouse_rightflank_loss_col,
                      analysis_length=299)
    

    target_time, center_time, object_time = get_time_in_chambers(mouse_pos_arr, fps, target_pos, midchamber_right_boundary, midchamber_left_boundary)

    sniffing_time = get_time_sniffing(mouse_pos_arr,data_arr,target_x_col,target_y_col, object_x_col, object_y_col, 
                                    target_pos, object_pos,midchamber_right_boundary, midchamber_left_boundary, fps, sniffing_threshold)


    mdata = [file, target_time, center_time, object_time, sniffing_time]
    results.append(mdata)

  return(results)

