from Tkinter import *
import time
import sys
import random
import pigpio

NUM_GPIO = 32

MIN_WIDTH = 1000
MAX_WIDTH = 2000

step = [0]*NUM_GPIO
width = [0]*NUM_GPIO
used = [False]*NUM_GPIO


def set_angle(angle, pi ):

    if not pi.connected:
        exit()
    
    if len(sys.argv) == 1:
        G = [4]
    else:
        G = []
        for a in sys.argv[1:]:
           G.append(int(a))
       
    # for g in G:
    #     used[g] = True
    #     step[g] = random.randrange(5, 25)
    #     if step[g] % 2 == 0:
    #        step[g] = -step[g]
    #     width[g] = random.randrange(MIN_WIDTH, MAX_WIDTH+1)
    
    # print("Sending servos pulses to GPIO {}, control C to stop.".
    #         format(' '.join(str(g) for g in G)))
    this_width = angle/float(180) * (MAX_WIDTH - MIN_WIDTH) + MIN_WIDTH 

    try:
        for g in G:
            pi.set_servo_pulsewidth(g, this_width)
            time.sleep(0.1)
    except KeyboardInterrupt:
        for g in G:
            pi.set_servo_pulsewidth(g, 0)
            

class App:

    def __init__(self, master, pi):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=180,
              orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)
        self.pi = pi

    def update(self, angle):
        duty = float(angle) / 10.0 + 2.5
        # pwm.ChangeDutyCycle(duty)
        set_angle(angle, self.pi)
    

if __name__=='__main__':
    
    pi = pigpio.pi()
    root = Tk()
    root.wm_title('Servo Control')
    app = App(root, pi)
    root.geometry("200x50+0+0")
    root.mainloop()
    pi.stop()


