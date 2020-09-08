# -*- coding: utf-8 -*-
import pigpio
from time import sleep


def headServo(error_Now, time, past_dc, error_Sum, error_Prev):
    global head_mindc
    global head_maxdc 
    global head_interval
    
    Kp = 0.5
    Ki = 0
    Kd = 0
    
    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/time
    
    ctrlval = -(Kp*error + Ki*error_sum*time + Kd*error_diff)
    
    if abs(ctrlval) < 0.02:
        ctrlval = 0
    ctrlval = round(ctrlval, 1)
           
    head_duty = past_dc - head_interval * ctrlval
    
    if head_duty < head_mindc:
        head_duty = head_mindc
        
    elif head_duty > head_maxdc:
        head_duty = head_maxdc
    
    print('ctrlval',ctrlval)
    
    if head_duty == past_dc:
        print(head_duty, past_dc,'steady')
        head_duty = past_dc
        head.ChangeDutyCycle(0)
    else:
        print(head_duty, past_dc,'move')
        head.ChangeDutyCycle(head_duty)

    return head_duty

def bodyServo(error_Now, time, past_dc, error_Sum, error_Prev):
    global body_mindc
    global body_maxdc 
    global body_interval
    
    Kp = 0.5
    Ki = 0
    Kd = 0
    
    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/time
    
    ctrlval = -(Kp*error + Ki*error_sum*time + Kd*error_diff)
    
    if abs(ctrlval) < 0.02:
        ctrlval = 0
    ctrlval = round(ctrlval, 1)
           
    body_duty = past_dc - body_interval * ctrlval
    
    if body_duty < body_mindc:
        body_duty = body_mindc
        
    elif body_duty > body_maxdc:
        body_duty = body_maxdc
    
    print('ctrlval',ctrlval)
    
    if body_duty == past_dc:
        print(body_duty, past_dc,'steady')
        body_duty = past_dc
        head.ChangeDutyCycle(0)
    else:
        print(body_duty, past_dc,'move')
        body.ChangeDutyCycle(body_duty)

    return body_duty
    

def shake(prev_angle, cycle):
    for i in range(0, cycle):
        left.ChangeDutyCycle(left_mindc + (prev_angle + 1) * left_interval)
        right.ChangeDutyCycle(right_mindc + prev_angle * right_interval)
        sleep(0.02)
        left.ChangeDutyCycle(left_mindc + prev_angle * left_interval)
        right.ChangeDutyCycle(right_mindc + (prev_angle + 1) * right_interval)
        sleep(0.02)
        
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    return prev_angle

def movetogether(prev_angle, goal_angle, speed): # angle: 0-16, speed:1,2,3,5
    
    left_status = left_mindc + left_interval * prev_angle
    right_status = right_mindc + right_interval * prev_angle
    
    stptime = 30/speed
    left_step = left_interval * (goal_angle - prev_angle) / stptime
    right_step = right_interval * (goal_angle - prev_angle) / stptime
    
    for i in range(0, int(stptime)):
        left.ChangeDutyCycle(left_status + left_step * i)
        right.ChangeDutyCycle(right_status + right_step * i)
        sleep(0.02)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    
    return goal_angle


def moveopposite(prev_angle, amount, speed):
    
    left_status = left_mindc + left_interval * prev_angle
    right_status = right_mindc + right_interval * prev_angle
    
    stptime = 30/speed
    
    left_goal = (left_interval * amount)/stptime
    right_goal = (right_interval * amount)/stptime
    
    for i in range(0, int(stptime)):
        left.ChangeDutyCycle(left_status - left_goal * i)
        right.ChangeDutyCycle(right_status + right_goal * i)
        sleep(0.02)
        
    for i in range(1, int(stptime) + 1):
        left.ChangeDutyCycle(left_status + left_goal * (i - int(stptime)))
        right.ChangeDutyCycle(right_status + right_goal * (int(stptime) - i))
        sleep(0.02)
        
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    
    return prev_angle

def headmove(prev_angle, goal_angle, speed):
             
    head_status = head_mindc + head_interval * prev_angle
    
    stptime = 30/speed
    head_step = head_interval * (goal_angle - prev_angle) / stptime
    
    for i in range(0, int(stptime)):
        head.ChangeDutyCycle(head_status + head_step * i)
        sleep(0.02)
    head.ChangeDutyCycle(0)
    return goal_angle


def headsleep():
    head.ChangeDutyCycle(0)


def emoreact(emotion):
    #neutral, happy, surprised, 
    if emotion == 'neutral1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(0.5)
    
    elif emotion == 'neutral2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        
    elif emotion == 'neutral3':
        left.ChangeDutyCycle(left_maxdc)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        
    elif emotion == 'happy1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        
    elif emotion == 'happy2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        
    elif emotion == 'sad1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        prev_angle = 0
        sleep(0.3)
        prev_angle = movetogether(prev_angle, 14, 2)
        sleep(0.5) #### sdflkasjfoasdjf
        prev_angle = movetogether(prev_angle, 0, 0.5)
        
    elif emotion == 'sad2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2)
        prev_angle = 0
        prev_angle = movetogether(prev_angle, 2, 3)
        prev_angle = movetogether(prev_angle, 0, 3)
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        
    elif emotion == 'angry1':
        # Go(-40, 0.5)
        sleep(0.5)
        shake(0, 15)
        # Go(40, 0.5)
    
    elif emotion == 'angry2':
        sleep(1.4)


    elif emotion == 'fear1':
        prev_angle = 14
        sleep(1)
        prev_angle = movetogether(prev_angle, 14, 3)
        sleep(0.2)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        sleep(0.5)
        prev_angle = movetogether(prev_angle, 0, 3)
        
    elif emotion == 'surprised1':
        prev_angle = 0
        sleep(0.1)
        prev_angle = movetogether(prev_angle, 5, 5)
        prev_angle = movetogether(prev_angle, 0, 5)
        sleep(1.5)
    
    elif emotion == 'surprised2':
        left.ChangeDutyCycle(left_maxdc)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        # Rot(-40, 0.1)
        # sleep(0.8)
        # # Rot(40, 0.2)
        # sleep(0.65)
        # Rot(-40, 0.1)

    else:
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        

# servo bound
head_mindc = 1650
head_maxdc = 2150
head_interval = (head_maxdc - head_mindc)/40

body_mindc = 600
body_maxdc = 2400
body_interval = (body_maxdc - body_mindc)/40

right_mindc = 500
right_maxdc = 1300
right_interval = (right_maxdc - right_mindc)/40

left_mindc = 1250
left_maxdc = 2000
left_interval = (left_maxdc - left_mindc)/40


