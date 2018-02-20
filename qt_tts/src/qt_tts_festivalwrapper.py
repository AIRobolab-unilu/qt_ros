#!/usr/bin/env python

import roslib; roslib.load_manifest('qt_tts')
import rospy
from std_msgs.msg import String

from sound_play.libsoundplay import SoundClient

class TalkBack:
    def talk_callback(self, msg):
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)
        
        print self.soundhandle.say(msg.data, self.voice)
        rospy.sleep(1)

    
    def cleanup(self):
        rospy.loginfo("Shutting down talkback node...")
        
    def __init__(self):
         
        self.voice = "voice_kal_diphone"
       
        # Create the sound client object
        self.soundhandle = SoundClient()
       
        rospy.sleep(1)
        self.soundhandle.stopAll()
       
        rospy.sleep(1)
        self.soundhandle.say("Ready", self.voice)
       
        self.false_lock = 0
        rospy.loginfo("Starting the system...")

        # Subscribe to the recognizer output
        rospy.Subscriber('~say', String, self.talk_callback)
       
        rospy.on_shutdown(self.cleanup)
        rospy.spin()


if __name__=="__main__":
    # Initialize the node and name it.
    rospy.init_node('qt_tts')

    try:
        TalkBack()
        
    except rospy.ROSInterruptException: pass

