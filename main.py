# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       amir                                                         #
# 	Created:      1/3/2024, 9:30:43 AM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

import urandom


# Brain should be defined by default
brain=Brain()


# Robot configuration code
claw_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
leftIntake = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
rightIntake = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
leftMotors_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotors_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
leftMotors = MotorGroup(leftMotors_motor_a, leftMotors_motor_b)
rightMotors_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
rightMotors_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
rightMotors = MotorGroup(rightMotors_motor_a, rightMotors_motor_b)
digital_out = DigitalOut(brain.three_wire_port.h)




# wait for rotation sensor to fully initialize
wait(30, MSEC)




def play_vexcode_sound(sound_name):
   # Helper to make playing sounds from the V5 in VEXcode easier and
   # keeps the code cleaner by making it clear what is happening.
   print("VEXPlaySound:" + sound_name)
   wait(5, MSEC)


# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")




# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True


# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
   global controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
   # process the controller input every 20 milliseconds
   # update the motors based on the input values
   while True:
       if remote_control_code_enabled:
           # check the buttonL1/buttonL2 status
           # to control leftIntake
           if controller_1.buttonL1.pressing():
               leftIntake.spin(FORWARD)
               controller_1_left_shoulder_control_motors_stopped = False
               rightIntake.spin(FORWARD)
               controller_1_right_shoulder_control_motors_stopped = False
           elif controller_1.buttonL2.pressing():
               leftIntake.spin(REVERSE)
               controller_1_left_shoulder_control_motors_stopped = False
               rightIntake.spin(REVERSE)
               controller_1_right_shoulder_control_motors_stopped = False
           elif not controller_1_left_shoulder_control_motors_stopped:
               leftIntake.stop()
               rightIntake.stop()
               # set the toggle so that we don't constantly tell the motor to stop when
               # the buttons are released
               controller_1_left_shoulder_control_motors_stopped = True
               controller_1_right_shoulder_control_motors_stopped = True
       wait(20, MSEC)


       # wait before repeating the process
       wait(20, MSEC)


# define variable for remote controller enable/disable
remote_control_code_enabled = True


rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)




# ----------------------------------------------------------------------------
#                                                                           
#    Project:        Tank Control                                        
#    Description:    This example will use the left Y and right Y
#                    Controller axis to control the Clawbot.
#    Configuration:  V5 Clawbot (Individual Motors)
#                    Controller
#                    Claw Motor in Port 3
#                    Arm Motor in Port 8
#                    Left Motor in Port 1
#                    Right Motor in Port 10  
#                                                                           
# ----------------------------------------------------------------------------

# Library imports
from vex import *

# Begin project code
#Functions
def linear_movement(distance):
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Linear Movement")
   distance2 = distance * 40
   circumference = 3.25 * 3.14
   rotation = distance2 / circumference
   leftMotors.set_velocity(100, PERCENT)
   rightMotors.set_velocity(100, PERCENT)
   allmotors = MotorGroup(rightMotors_motor_a, rightMotors_motor_b, leftMotors_motor_a, leftMotors_motor_b)
   allmotors.spin_for(FORWARD, rotation, TURNS)
   brain.screen.clear_screen()


def turn_counter(turnCount):
   brain.screen.clear_screen()
   brain.screen.set_cursor(1, 1)
   brain.screen.print("Turning")
   leftMotors.set_velocity(15, PERCENT)
   rightMotors.set_velocity(15, PERCENT)
   turnCounter = turnCount * 1.35
   rightMotors.spin_for(FORWARD, turnCounter, TURNS)
   leftMotors.spin_for(REVERSE, turnCounter, TURNS)


def intake_ball():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Intake tri-ball")
   leftIntake.set_velocity(15, PERCENT)
   rightIntake.set_velocity(15, PERCENT)
   intakeGroup = MotorGroup(leftIntake, rightIntake)
   intakeGroup.spin_for(FORWARD, 1, TURNS)

def output_ball():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Output tri-ball")
   leftIntake.set_velocity(90, PERCENT)
   rightIntake.set_velocity(90, PERCENT)
   intakeGroup = MotorGroup(leftIntake, rightIntake)
   intakeGroup.spin_for(REVERSE, 1, TURNS)
"""
def :
   brain.screen.print("Turning")
   leftMotors.set_velocity(15, PERCENT)
   rightMotors.set_velocity(15, PERCENT)
   turnCounter = turnCount
   rightMotors.spin_for(FORWARD, turnCounter, TURNS)
   leftMotors.spin_for(REVERSE, turnCounter, TURNS)
"""
#Robot Competition Phases
def pre_autonomous():
   # actions to do when the program starts
   brain.screen.clear_screen()
   brain.screen.print("Pre Auton mode")
   wait(1, SECONDS)


def autonomous():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Autonomous")
   linear_movement(0.4)
   output_ball()
   linear_movement(-0.1)
   linear_movement(0.1)

def user_control():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Driver Control mode")
   # place driver control in this while loop
   while True:
       straight = controller_1.axis3.position()
       turn = controller_1.axis1.position()
       leftSpeed =  straight + turn
       rightSpeed = straight - turn
       leftMotors.set_velocity(leftSpeed, PERCENT)
       rightMotors.set_velocity(rightSpeed, PERCENT)
       rightMotors.spin(FORWARD)
       leftMotors.spin(FORWARD)
       if controller_1.buttonA.pressing():
          brain.screen.print("Pneumatic Button: Pressed")
          digital_out.set(True)
          wait(5, SECONDS)
          digital_out.set(False)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()




        
