# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       amir                                                         #
# 	Created:      1/22/2024, 4:08:04 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()



# Robot configuration code
claw_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
Intake = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
leftMotors_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotors_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
leftMotors = MotorGroup(leftMotors_motor_a, leftMotors_motor_b)
rightMotors_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
rightMotors_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
rightMotors = MotorGroup(rightMotors_motor_a, rightMotors_motor_b)
digital_out = DigitalOut(brain.three_wire_port.h)
launch_motor_left = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
launch_motor_right = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
launch_motor = MotorGroup(launch_motor_left, launch_motor_right)



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
autonactive = True

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
   global controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled, autonactive
   # process the controller input every 20 milliseconds
   # update the motors based on the input values
   while True:
       if remote_control_code_enabled:
           # check the buttonL1/buttonL2 status
           # to control leftIntake
           if controller_1.buttonL1.pressing():
               Intake.set_velocity(100, PERCENT)
               Intake.spin(FORWARD)
               controller_1_left_shoulder_control_motors_stopped = False
               controller_1_right_shoulder_control_motors_stopped = False
           elif controller_1.buttonL2.pressing():
               Intake.spin(REVERSE)
               controller_1_left_shoulder_control_motors_stopped = False
               controller_1_right_shoulder_control_motors_stopped = False
           elif not controller_1_left_shoulder_control_motors_stopped:
               Intake.set_velocity(100, PERCENT)
               Intake.stop()
               # set the toggle so that we don't constantly tell the motor to stop when
               # the buttons are released
               controller_1_left_shoulder_control_motors_stopped = True
               controller_1_right_shoulder_control_motors_stopped = True
           if autonactive == False :
               if controller_1.buttonB.pressing():   
                     launch_motor.set_velocity(100, PERCENT)
                     launch_motor.spin(FORWARD)
                     
                     
               if not controller_1.buttonB.pressing():
                     launch_motor.stop()

           if controller_1.buttonR1.pressing():
               brain.screen.clear_screen()
               brain.screen.print("Pneumatic Button: Pressed")
               digital_out.set(True)
               """
               wait(5, SECONDS)
               digital_out.set(False)
               """
           else :
               digital_out.set(False)
            



       # wait before repeating the process
       wait(10, MSEC)


# define variable for remote controller enable/disable
remote_control_code_enabled = True


rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
autonthread = Thread(autonactive)

#Functions
def linear_movement(distance):
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Linear Movement")
   distance2 = distance * 24
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

def right_turn():
   leftMotors.set_velocity(10, PERCENT)
   leftMotors.spin_for(FORWARD, .2, TURNS)

def left_turn():
   rightMotors.set_velocity(10, PERCENT)
   rightMotors.spin_for(FORWARD, 1, TURNS)

def intake_ball():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Intake tri-ball")
   Intake.set_velocity(90, PERCENT)
   intakeGroup = MotorGroup(Intake)
   intakeGroup.spin_for(REVERSE, 1, TURNS)

def output_ball():
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Output tri-ball")
   Intake.set_velocity(100, PERCENT)
   intakeGroup = MotorGroup(Intake)
   intakeGroup.spin_for(FORWARD, 4, TURNS)

def pneumatic():
    while True:
        if controller_1.buttonA.pressing():
            brain.screen.clear_screen()
            brain.screen.print("Pneumatic Button: Pressed")
            digital_out.set(True)
            wait(5, SECONDS)
            digital_out.set(False)
       
#Robot Competition Phases
def pre_autonomous():
   # actions to do when the program starts
   brain.screen.clear_screen()
   brain.screen.print("Pre Auton mode")
   wait(1, SECONDS)

def skills_autonomous():
   global autonactive
   autonactive = True
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Autonomous mode")
   allmotors.set_velocity(100, PERCENT)
   allmotors.spin_for(FORWARD, .5, SECONDS)
   output_ball()
   allmotors.spin_for(REVERSE, .5, SECONDS)
   turn_counter(-3)
   launch_motor.set_velocity(100, PERCENT)
   launch_motor.spin_for(FORWARD, 60, SECONDS)

   
def user_control():
   global autonactive 
   brain.screen.clear_screen()
   brain.screen.set_cursor(1,1)
   brain.screen.print("Driver Control mode")
   autonactive = False
   # place driver control in this while loop
   while True:
       straight = controller_1.axis3.position() 
       turn = controller_1.axis1.position() * .65
       leftSpeed =  (straight + turn) 
       rightSpeed = (straight - turn)
       leftMotors.set_velocity(leftSpeed, PERCENT)
       rightMotors.set_velocity(rightSpeed, PERCENT)
       rightMotors.spin(FORWARD)
       leftMotors.spin(FORWARD)

# Thread Section
       
pneumaticControl = Thread(pneumatic)

# Competition Instance

autonomous = skills_autonomous
Comp = Competition(user_control, autonomous)

