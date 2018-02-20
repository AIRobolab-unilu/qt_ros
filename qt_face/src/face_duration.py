#!/usr/bin/env python

# Import required Python code.
import roslib
roslib.load_manifest('qt_face')
import rospy
import cv2
#import cv2.cv as cv
import time
import sys
import fnmatch
import os

from random import randrange, uniform

from std_msgs.msg import String
from std_msgs.msg import Int8


from qt_face.srv import *



EMOTIONS_PATH='/home/odroid/robot/cuddie/main/data/emotions/'
AUDIO_PATH =  '/home/odroid/robot/cuddie/main/data/audios/'
DEBUG=False    

# Node example class.
class NodeExample():
    def talk_duration(self, file_path):
        print file_path
        bashCommand = "soxi -D "+ file_path + " > tmp.txt"
        os.system(bashCommand)
        duration = float(open('tmp.txt', 'r').read())
        print "Duration in the call" + str(duration)
        return duration
    
    def callback(self, data):
        if (DEBUG):
            rospy.loginfo(rospy.get_caller_id() + " I will change the face %s", data.data)
            
        self.face_change_name = data.data
        self.face_change_path = EMOTIONS_PATH+data.data+'.avi'  
        self.face_change_status = 1
    
    def callback_framerate(self, data):
        
        self.value_framerate = data.data
        self.value_framerate_in_miliseconds = int ( 1000 / data.data)
        if (DEBUG):
            rospy.loginfo(rospy.get_caller_id() + " Estrablising a frame rate of  %d, which means every [%d] miliseconds", self.value_framerate, self.value_framerate_in_miliseconds)
            
         
        
    def callback_namefile(self, data):
        if (DEBUG):
            rospy.loginfo(rospy.get_caller_id() + " I should charge the face for the one in the path %s", data.data)
            
        self.face_change_name = data.data
        self.face_change_path = data.data 
        self.face_change_status = 1
        
    def handle_new_face(self, req):
        print "New face called: face name [%s], audio_file_name [%s], and duration  %d "%(req.name, req.audio_file_name, req.duration)
          #It is necessary to split the address by elements
        v_path_list = req.audio_file_name.split("/")
        v_path_list_len = len(v_path_list)
        v_extra_path_tmp = ''
        
        if v_path_list_len == 1:
            v_audio_file_name =  req.audio_file_name
        else :
            v_audio_file_name = v_path_list[v_path_list_len-1];
            v_path_list.pop()
            for element in v_path_list:
                v_extra_path_tmp = v_extra_path_tmp+element+"/"
        
        v_audio_path = AUDIO_PATH+v_extra_path_tmp
        
        v_audio_file_name = str(v_audio_file_name)+'.*'
        print 'Callback: ' + v_audio_file_name 
        v_file_exists = False
        
        #We do a rough lip sinchronization here 
        
        for file in os.listdir(v_audio_path):
            if fnmatch.fnmatch(file, v_audio_file_name):
                print 'I found the file **' + file
                req.duration = self.talk_duration(v_audio_path+file)
                v_file_exists = True
                break
        
        if not v_file_exists:
            print "There is no file with this name or we are running the fake wav"
            v_total_chars = len(v_audio_file_name)
            print len(v_audio_file_name)
            req.duration = (v_total_chars / 10 ) 
            if (req.duration < 3):
                req.duration = 1
            elif (req.duration == 4):
                req.duration = 5
            print "Duration of a fake talk "+str(req.duration)
            
            
        
        self.face_change_name = req.name
        self.face_change_path = EMOTIONS_PATH + req.name + '.avi'  
        self.face_change_status = 1
                
        if (req.duration > 2 ):
            self.duration_end_loops = req.duration  - 3
        if (req.duration == 1 ):
            self.duration_end_loops = req.duration  
            
            
        print "Runnin new face"
        print "Duration "+str(self.duration_end_loops)
        while self.face_change_status != 0:
                rospy.sleep(0.5)
        print "New face finish"        
        return True    
        
        
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        rate = float(rospy.get_param('~rate', '1.0'))
        rospy.loginfo('rate = %d', rate)

        # Create a publisher for our custom message.
        rospy.Subscriber("~setEmotion", String, self.callback)
        rospy.Subscriber("~setEmotion_by_filename", String, self.callback_namefile)
        rospy.Subscriber("~setEmotion_framerate", Int8, self.callback_framerate)

  
        
        self.duration_end_loops = 0
        
        self.face_change_status = 0
        
        self.value_framerate = 10
        self.value_framerate_in_miliseconds = 110
        
        self.gesture_duration = 0
        
        face_status = 'logo'

        resource_name = EMOTIONS_PATH + 'logo.avi'

        resource = resource_name
        print "Trying to open resource: " + resource_name
        cap = cv2.VideoCapture(resource)
        if not cap.isOpened():
            print "Error opening resource: " + str(resource)
            print "Maybe opencv VideoCapture can't open it"
            exit(0)


        s = rospy.Service('ChangeQTFace', ChangeQTFace, self.handle_new_face)

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        
        
        if int(major_ver)  < 3 :
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
            print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
        else :
            fps = cap.get(cv2.CAP_PROP_FPS)
            print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)
        

        print "Correctly opened resource, starting to show feed."
        rval, frame = cap.read()
        frame_counter=0
        
        load_new_face = False
        running_face  = True
        rval = True
        
        local_status_loops_by_duration = 0
        
        #We set the window size
        cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        #Different resolutions for QT display 1300, 730), 1300, 730), 640, 480)
        cv2.resizeWindow('image', 800, 480)


        #With this method we maintain the opencv approach and to close with ros tools
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        while rval and not rospy.is_shutdown():
        
                    if (DEBUG):
                        print "frame_counter: >> "+str(total) +  " .."+str(frame_counter)
                    rval, frame = cap.read()
                    cv2.imshow('image', frame)
                    key = cv2.waitKey(self.value_framerate_in_miliseconds)
                    
                                        
                    if ( self.face_change_status == 1) and not (running_face):
                            print "Change Face called: >> "
                            resource_tmp = self.face_change_path
                            face_status = self.face_change_name
                            load_new_face = True
                            self.face_change_status = 2
                            running_face = True
                            frame_counter = 0 
                            local_status_loops_by_duration = 0
                    else:
                        if not (load_new_face) and (face_status != 'blink') and not (running_face):
                            print "Stablishing Blinking: >> " + str(self.face_change_status)
                            resource_tmp = EMOTIONS_PATH + 'blink.avi'
                            face_status = 'blink'
                            load_new_face = True
                            frame_counter = 0;
                            
                    if (load_new_face):
                        print "Opening new face: >> "
                        cap = cv2.VideoCapture(resource_tmp)
                        load_new_face = False
                        if not cap.isOpened():
                            print "Error opening resource: " + str(resource_tmp)
                            print "Maybe opencv VideoCapture can't open it"
                            resource_tmp = EMOTIONS_PATH + 'blink.avi'
                            cap = cv2.VideoCapture(resource_tmp)
                            print "=======================================" 
                        
                
                  
                    
                    if (face_status == 'logo'):
                        if (frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-4):
                            print "==== "
                            frame_counter = 0 
                            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)    
                            running_face = False
                            
                    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    if (frame_counter == total-1) and (face_status == 'blink'):
                        total -= 1 
                    

                    if ((frame_counter == 8 ) and (local_status_loops_by_duration <  self.duration_end_loops) and (face_status == 'ava_talking')):
                        if (DEBUG):
                            print ":> Ava Talking ~ "+face_status+ "we are in the loop"+str(local_status_loops_by_duration)
                        frame_counter = 0 
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        local_status_loops_by_duration += 1
                        now = rospy.get_rostime()
                        rospy.loginfo("Current time %i %i", now.secs, now.nsecs)
                        if (self.duration_end_loops == 1):
                            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        
                            if (self.face_change_status == 2):
                                self.face_change_status = 0
                            
                            running_face = False
                    elif (frame_counter == (int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1) ):
                        if(DEBUG):
                            print ":> Face_status ~ "+face_status
                        frame_counter = 0 
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        
                        if (self.face_change_status == 2):
                            self.face_change_status = 0
                            
                        running_face = False

                    else:
                        if(DEBUG):
                            print ":> +1 ~ "+face_status
                        frame_counter += 1
                    
                    
     
        cv2.destroyWindow("preview")
    


# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('qt_face')
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        ne = NodeExample()
    
    except rospy.ROSInterruptException: pass
