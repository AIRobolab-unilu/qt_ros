#!/usr/bin/env python
import roslib
roslib.load_manifest('qt_playsound')
import rospy
import subprocess

import os


from std_msgs.msg import String


DEMO_MODE=False


class qt_playsound_node():
    
    def game_start_callback(self, event):
        directory_path = self.directory_folder + str(event.data) 
        directory_path_ext = directory_path + ".mp3"
        if os.path.isfile(directory_path_ext) == True:
            bashCommand = "play "+directory_path_ext
        else:
            bashCommand = "play "+directory_path + ".wav"
        os.system(bashCommand)

    def playsound_callback(self, event):
        bashCommand = "play "+ str(event.data)
        os.system(bashCommand)

    
    def __init__(self):


        rospy.Subscriber("~play_song", String, self.game_start_callback)
        rospy.Subscriber("~playsoundfile", String, self.playsound_callback)

        
        self.directory_folder = rospy.get_param('~soundPath')
        
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('qt_playsound')

    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        ne = qt_playsound_node()
    except rospy.ROSInterruptException: pass
