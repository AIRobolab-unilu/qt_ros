#include "ros/ros.h"
#include "std_msgs/String.h"

#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"

#include "std_msgs/Int32MultiArray.h"



#include <stdio.h>
#include <yarp/os/Network.h>
#include <yarp/os/Time.h>
#include <yarp/dev/PolyDriver.h>            // to open a generic remote driver
#include <yarp/dev/IPositionControl.h>      // for controlling robot in position mode
#include <yarp/dev/IEncoders.h>             // for reading motor encoders
#include <yarp/dev/IControlMode2.h>         // for setting the control modes (postion, velocity, idle)
#include <yarp/dev/IInteractionMode.h>      // for setting the interaction modes (stiff, complient)

using namespace yarp::os;


#include <sstream>


//////////////////////////////// 
//////////////////////////////// 
yarp::os::Network yarpInst;
Port actionPort;
//////////////////////////////// 
//////////////////////////////// 


////////////////////////////////////////
// 0 : Motor 0 Position
// 1 : Motor 1 Position
int increment[8];


int Arr[8];

////////////////////////////////////////
// 0 : Motor id
// 1 : Motor movement degrees
// 2 : Motor speed
int localMovement[3];


// create the desired interfaces
yarp::dev::IPositionControl *iPos;
yarp::dev::IEncoders *iEnc;
yarp::dev::IControlMode2 *iCtrl;
yarp::dev::IInteractionMode* iInteract;


void incrementMotorCallback(const std_msgs::Int32MultiArray::ConstPtr& array)
{

    int i = 0;
    
    //     init vector
    for(int j = 0; j < 8; ++j)
    {
            increment[j] = 0;
    }
    
    // print all the remaining numbers
    for(std::vector<int>::const_iterator it = array->data.begin(); it != array->data.end(); ++it)
    {
            increment[i] = *it;
            i++;
    }
    double encs[8];
    iEnc->getEncoders(encs);
    
    fprintf(stdout, "Motor (Before) n_yaw:[%.2f]  n_pith:[%.2f]  r_should:[%.2f]  r_should:[%.2f]  r_should:[%.2f]  l_should:[%.2f]  l_should::[%.2f] l_should::[%.2f]\n", encs[0],encs[1],encs[2],encs[3],encs[4],encs[5],encs[6],encs[7]);
  
    iCtrl->setControlMode(2, VOCAB_CM_IDLE);

    // setting back the joint 2 in pposition mode (the motor LED should turn to green)
    iCtrl->setControlMode(2, VOCAB_CM_POSITION);


    // setting the joint 2  in stiff mode
    iInteract->setInteractionMode(2, yarp::dev::VOCAB_IM_STIFF);
    // setting back the joint 2 in complient mode
    iInteract->setInteractionMode(2, yarp::dev::VOCAB_IM_COMPLIANT);
    
    

    // All of the above interfaces has the batch functionality to control
    // the multiple joints. For example to move all the joint to the home position,
    // e.g., 0.0  -15  0.0    -60.0  30.0   0.0     60.0   -30.0
    double speeds[] = {80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0};
    double poses[] = {encs[0]+increment[0], encs[1]+increment[1], encs[2]+increment[2], encs[3]+increment[3], encs[4]+increment[4], encs[5]+increment[5], encs[6]+increment[6], encs[7]+increment[7]};
    iPos->setRefSpeeds(speeds);
    iPos->positionMove(poses);
    Time::delay(2.0);
    
    iEnc->getEncoders(encs);
    
    fprintf(stdout, "Motor (After) n_yaw:[%.2f]  n_pith:[%.2f]  r_should:[%.2f]  r_should:[%.2f]  r_should:[%.2f]  l_should:[%.2f]  l_should::[%.2f] l_should::[%.2f]\n", encs[0],encs[1],encs[2],encs[3],encs[4],encs[5],encs[6],encs[7]);

    
    return;
}


void motorCallback(const std_msgs::Int32MultiArray::ConstPtr& array)
{

       int i = 0;
	// print all the remaining numbers
	for(std::vector<int>::const_iterator it = array->data.begin(); it != array->data.end(); ++it)
	{
		localMovement[i] = *it;
		i++;
	}

	
        ROS_INFO("I heard: id[%d]  degrees[%d]  speed[%d]", localMovement[0], localMovement[1], localMovement[2] );
            //////////////////////////////////////////////////////////////////////////////////
    // some more examples
    //////////////////////////////////////////////////////////////////////////////////
    
    // setting the control mode of joint 2 (right shoulder) to Position control mode
    // alternatively iCtrl->setPositionMode(2);
    iCtrl->setControlMode(localMovement[0], VOCAB_CM_POSITION);

    // move the joint to angle 30 with 50% of velocity
    iPos->setRefSpeed(localMovement[0], localMovement[2]);
    iPos->positionMove(localMovement[0], localMovement[1]);

    // wait for two seconds until the motor reach the desire position
    // alternatively we could cal iPos->checkMotionDone(2, &ret) to
    // check whether the motor is in position or not.
    // However, this has not been tested on the reobot yet!!!
    Time::delay(2.0);

    // reading the encoders
    // NOTE: due to gravity force and frictions in the complient mode,
    // the actual motor position may not be exactly the same as the desired one.
    // more accuracy can be achieved by controling  the motor in stiff mode and moving
    // the joint with higher velocity (reference speed).
    double pos;
    iEnc->getEncoder(localMovement[0], &pos);
    fprintf(stdout, "Motor is in position %.2f\n", pos);

    //////////////////////////////////////////////////////////////////////////////////
	return;
}

void fullBodyMovementCallback(const std_msgs::Int32MultiArray::ConstPtr& array)
{

    int i = 0;
    // print all the remaining numbers
    for(std::vector<int>::const_iterator it = array->data.begin(); it != array->data.end(); ++it)
    {
            Arr[i] = *it;
            i++;
    }
    
    // setting the joint 2 in idle mode
    // NOTE: this is also clear any hardware fault and error of the motor (no more blinking red light :p)
    // NOTE: velocity mode has not been tested yet and better to be avoided
    // Especially when the motor is in stiff mode, any malfunction in this mode
    // can cause severe damage to the motor!!!
    iCtrl->setControlMode(2, VOCAB_CM_IDLE);
    // now the motor torque is released and you can move
    // the joint by hand (the motor LED should turn to pink)
//     Time::delay(5.0);

    // setting back the joint 2 in pposition mode (the motor LED should turn to green)
    iCtrl->setControlMode(2, VOCAB_CM_POSITION);


    // setting the joint 2  in stiff mode
    iInteract->setInteractionMode(2, yarp::dev::VOCAB_IM_STIFF);
    // setting back the joint 2 in complient mode
    iInteract->setInteractionMode(2, yarp::dev::VOCAB_IM_COMPLIANT);


    // All of the above interfaces has the batch functionality to control
    // the multiple joints. For example to move all the joint to the home position,
    // e.g., 0.0  -15  0.0    -60.0  30.0   0.0     60.0   -30.0
    double speeds[] = {30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0};
    double poses[] = {0.0, -15.0, 0.0, -60.0, 30.0, 0.0, 60.0, -30.0};
    iPos->setRefSpeeds(speeds);
    iPos->positionMove(poses);
    Time::delay(2.0);
    double encs[8];
    iEnc->getEncoders(encs);
    for (i=0; i<8;i++)
        fprintf(stdout, "Motor [%d] is in position  %.2f \n", i, encs[i]);

    
    return;
}



void playGestureCallback(const std_msgs::String::ConstPtr& msg)
{

    ROS_INFO("File name %s", msg->data.c_str());
    Bottle cmd, reply;
    cmd.addString("play");
    cmd.addString(msg->data.c_str());
    cmd.addDouble(0.5); // speed
    actionPort.write(cmd,reply);
    
    return;
}


void startRecordGesture(const std_msgs::String::ConstPtr& msg)
{

    
    ROS_INFO("Recording gestions***** %s", "cadena");

    Bottle cmdRelease, replyRelease;
    cmdRelease.addString("idleParts");
    cmdRelease.addString("all");
    actionPort.write(cmdRelease,replyRelease);

    Bottle cmd, reply;
    cmd.addString("record");
    cmd.addString(msg->data.c_str());
    cmd.addString("all");
    actionPort.write(cmd, reply);

    return;
}


void stopRecordGesture(const std_msgs::String::ConstPtr& msg)
{
    Bottle cmd, reply;
    cmd.addString("stopRecording");
    actionPort.write(cmd, reply);
    ROS_INFO("Robot ends record ***** %s",reply.toString().c_str());

    return;
}

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
}


/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char **argv)
{
 
  ros::init(argc, argv, "qt_movement");
  ros::NodeHandle n;

  ros::Subscriber sub_localMovement = n.subscribe("/qt_movement/localMovement", 10, motorCallback);
  ros::Subscriber sub_fullBodyMovement = n.subscribe("/qt_movement/fullBodyMovement", 10, fullBodyMovementCallback);
  ros::Subscriber sub_incrementMotorCallback = n.subscribe("/qt_movement/incrementMotorCallback", 10, incrementMotorCallback);
  ros::Subscriber sub_playGestureCallback = n.subscribe("/qt_movement/playGestureFromFile", 10, playGestureCallback);
  ros::Subscriber sub_stopRecordGesture = n.subscribe("/qt_movement/gestureStopRecord", 10, stopRecordGesture);
  ros::Subscriber sub_startRecordGesture = n.subscribe("/qt_movement/gestureStartRecord", 10, startRecordGesture);
    


  ros::Rate loop_rate(10);

    // initializing yarp network
    yarp::os::Network yarp;

    // Note: robotInterface should be already up
    // configure the drivers' options
    Property option("(device remote_controlboard)");
    option.put("remote", "/cuddie/motors");     // must be "/cuddie/motors"
    option.put("local","/motorControl/motors"); // can be any yarp port name (e.g. /foo/bar)
    // NOTE: all the yarp ports should be started with a '/'.

    // create and open the remote driver
    yarp::dev::PolyDriver driver;
    if (!driver.open(option)) {
        fprintf(stdout, "Cannot open the remote driver!\n");
        return 0;
    }


    driver.view(iPos);
    driver.view(iEnc);
    driver.view(iCtrl);
    driver.view(iInteract);

    bool ret = actionPort.open("...");

    ret &= NetworkBase::connect(actionPort.getName(), "/cuddie/actionManager:rpc");
    
  
  int count = 0;
  while (ros::ok())
  {


    ros::spinOnce();
    
    loop_rate.sleep();
    ++count;
   
    
    
  }

     // closing the driver
    driver.close();
  return 0;
}
