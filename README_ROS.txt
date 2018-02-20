===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_base]
Description: This node publishes an "alive" message every 10 seconds.
Publications: 
 * /qt_base/status [std_msgs/String]
 * /rosout [rosgraph_msgs/Log]

Subscriptions: None

Services: 
 * /qt_base/get_loggers
 * /qt_base/set_logger_level

------==------
Useful Topics
------==------
odroid@QT4:~/robot/cuddie/main/data/actions$ rostopic info /qt_base/status
Type: std_msgs/String

Publishers: 
 * /qt_base (http://192.168.100.1:32779/)

Subscribers: None

===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_face]
Description: This node is in charge of showing QT's face in QT's display
Publications: 
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /qt_face/setEmotion_by_filename [unknown type]
 * /qt_face/setEmotion_framerate [unknown type]
 * /qt_face/setEmotion [unknown type]

Services: 
 * /ChangeQTFace
 * /qt_face/set_logger_level
 * /qt_face/get_loggers

------==------
Useful Topics
------==------


Description:   When the name of a emotional face is published  in this topic, the robot shows a new emotion.

--/home/odroid/robot/cuddie/main/data/emotions----


odroid@QT4:~/autostart/logs$ rostopic info /qt_face/setEmotion
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_face (http://192.168.100.1:40904/)

------

Description:   When the name of a emotional face is published in this topic, the robot shows a new emotion. This time it is expected the full path of an avi file (800x600)

odroid@QT4:~/autostart/logs$ rostopic info /qt_face/setEmotion_by_filename 
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_face (http://192.168.100.1:40904/)

------

Description:   Changes the framerate of the emotion presented on QT's face

odroid@QT4:~/autostart/logs$ rostopic info /qt_face/setEmotion_framerate 
Type: std_msgs/Int8

Publishers: None

Subscribers: 
 * /qt_face (http://192.168.100.1:40904/)
 
 ------==------
Useful Service
------==------
Description:  It is used to change robot face  using a ROS service. 

odroid@QT4:~/catkin_ws/src/qt_release$ rosservice info /ChangeQTFace 
Node: /qt_face
URI: rosrpc://192.168.100.1:34979
Type: qt_face/ChangeQTFace
Args: name audio_file_name duration

===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_playsound]
Description: This node plays audio files (wav and mp3)
Publications: 
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /qt_playsound/play_song [unknown type]
 * /qt_playsound/playsoundfile [unknown type]

Services: 
 * /qt_playsound/set_logger_level
 * /qt_playsound/get_loggers

------==------
Useful Topics
------==------

Description:  This topic is used to play the name of an audio file from the directory 
/home/odroid/robot/cuddie/main/data/audios


odroid@QT4:~/autostart/logs$ rostopic info /qt_playsound/play_song
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_playsound (http://192.168.100.1:41358/)
------

Description:  It  plays the name of an audio file using the fullpath in the robot.

odroid@QT4:~/autostart/logs$ rostopic info /qt_playsound/playsoundfile
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_playsound (http://192.168.100.1:41358/)


===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_tts]

Description:  It is a Text To Speech node. This node is a wrapper to ROS sound_play node (based on Festival). 
Publications: 
 * /robotsound [sound_play/SoundRequest]
 * /rosout [rosgraph_msgs/Log]
 * /sound_play/cancel [actionlib_msgs/GoalID]
 * /sound_play/goal [sound_play/SoundRequestActionGoal]

Subscriptions: 
 * /sound_play/result [unknown type]
 * /sound_play/status [unknown type]
 * /sound_play/feedback [unknown type]
 * /qt_tts/say [unknown type]

Services: 
 * /qt_tts/set_logger_level
 * /qt_tts/get_loggers

------==------
Useful Topics
------==------

Description:  This topic receive a string and the robot says this string.

odroid@QT4:~/autostart/logs$ rostopic info /qt_tts/say
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_tts (http://192.168.100.1:46485/)


===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_ent_game]
Description: EXPERIMENTAL - 
This node  moves the head from right to left. It is used for entertainment. 

Publications: 
 * /qt_tts/say [std_msgs/String]
 * /rosout [rosgraph_msgs/Log]
 * /qt_playsound/play_song [std_msgs/String]
 * /qt_face/setEmotion [std_msgs/String]
 * /qt_movement/incrementMotorCallback [std_msgs/Int32MultiArray]
 * /chatter [std_msgs/String]
 * /qt_movement/localMovement [std_msgs/Int32MultiArray]

Subscriptions: 
 * /q_face_detected [unknown type]
 * /head_mov_mode [unknown type]

Services: 
 * /game/get_loggers
 * /game/set_logger_level



===========================================================================
===  ROS NODE
===========================================================================
Node [/qt_movement]ç
Description: This node makes a wrap for YARP interfaces
Publications: 
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /qt_movement/gestureStartRecord [unknown type]
 * /qt_movement/incrementMotorCallback [unknown type]
 * /qt_movement/gestureStopRecord [unknown type]
 * /qt_movement/playGestureFromFile [unknown type]
 * /qt_movement/fullBodyMovement [unknown type]
 * /qt_movement/localMovement [unknown type]

Services: 
 * /qt_movement/get_loggers
 * /qt_movement/set_logger_level

------==------
Useful Topics
------==------

Description: When a String "random_name" is published in this topic, the robot records a new gesture called  "random_name". In this time, all the robot movements will be stored until gestureStopRecord is called.

odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/gestureStartRecord
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)
------

Description:  When the String "stop" is published in this topic, the robot stops record a running StartRecord gesture


odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/gestureStopRecord
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)

------

Description:  When a string "random_name" is published in this topic, the robot plays the previously generated gesture. 

odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/playGestureFromFile
Type: std_msgs/String

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)


------==------
Experimental topics - In development
------==------

Description: Increments the position of the motors 
odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/incrementMotorCallback
Type: std_msgs/Int32MultiArray

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)
 
Description: Moves all the motors to a given position 
odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/fullBodyMovement
Type: std_msgs/Int32MultiArray

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)

Description: moves the motors to certain position.

odroid@QT4:~/catkin_ws/src/qt_release$ rostopic info /qt_movement/localMovement
Type: std_msgs/Int32MultiArray

Publishers: None

Subscribers: 
 * /qt_movement (http://192.168.100.1:34159/)

===========================================================================
===  ROS NODE
===========================================================================

Node [/qt_demo]
Description: This node is used for demo procedures.
Publications: 
 * /rosout [rosgraph_msgs/Log]
 * /qt_playsound/play_song [std_msgs/String]
 * /qt_face/setEmotion [std_msgs/String]
 * /robot/voice [std_msgs/String]
 * /qt_movement/playGestureFromFile [std_msgs/String]

Subscriptions: 
 * /qt_basic_demo/mode [unknown type]
 * /objects [std_msgs/Float32MultiArray]

Services: 
 * /qt_demo/get_loggers
 * /qt_demo/set_logger_level


===========================================================================
===  DEPENDENCIES
===========================================================================

ROS:
find_object2d
Project: http://wiki.ros.org/find_object_2d

YARP
Project: http://www.yarp.it/


QT_YARP interfaces:
LuxAI: http://luxai.com/
