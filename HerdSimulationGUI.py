from Tkinter import *
import threading
import SimulationEngine

def start_sim():
	set_velocity()
    set_too_close()
    set_sight_range()
    set_angle_range()
    set_rule1()
    set_rule3()
    if not SimulationEngine.IS_RUNNING:
        SimulationEngine.IS_RUNNING = True
        t = threading.Thread(target=SimulationEngine.start)
        t.daemon = True
        t.start()
    else:
        print "Simulation is still running"


def set_velocity():
    selection = "MAX_VELOCITY = " + str(velocity_value.get())
    SimulationEngine.MAX_VELOCITY = velocity_value.get()
    print selection


def set_too_close():
    selection = "TOO_CLOSE_RANGE = " + str(to_close_val.get())
    SimulationEngine.TOO_CLOSE_RANGE = to_close_val.get()
    print selection


def set_sight_range():
    selection = "SIGHT_RANGE = " + str(sight_range_value.get())
    SimulationEngine.SIGHT_RANGE = sight_range_value.get()
    print selection

def set_angle_range():
    selection = "SIGHT_ANGLE = " + str(sight_angle_value.get())
    SimulationEngine.SEE_ANGLE = sight_angle_value.get()
    print selection
    

def set_rule1():
    selection = "RULE1_DIVIDER = " + str(rule_1_val.get())
    SimulationEngine.RULE1_DIVIDER = rule_1_val.get()
    print selection


def set_rule3():
    selection = "RULE3_DIVIDER = " + str(rule_3_val.get())
    SimulationEngine.RULE3_DIVIDER = rule_3_val.get()
    print selection

############################################################

root = Tk()
frame = Frame(root)
frame.pack()

velocity_value = DoubleVar()
to_close_val = DoubleVar()
sight_range_value = DoubleVar()
sight_angle_value = DoubleVar()
rule_1_val = DoubleVar()
rule_3_val = DoubleVar()

############################################################

vel_frame = Frame(frame)
vel_frame.pack(side=TOP)

velocity_label = Label(vel_frame, text="Max velocity")
velocity_label.pack(side=LEFT)

velocity_scale = Scale(vel_frame, from_=1, to=15, orient=HORIZONTAL, length=300, variable=velocity_value)
velocity_scale.pack(side=LEFT)
velocity_scale.set(SimulationEngine.MAX_VELOCITY)

velocity_set_bt = Button(vel_frame, text="Set", command=set_velocity)
velocity_set_bt.pack(side=LEFT)

############################################################

sight_range_frame = Frame(frame)
sight_range_frame.pack(side=TOP)

sight_range_label = Label(sight_range_frame, text="Sight Range")
sight_range_label.pack(side=LEFT)

sight_range_scale = Scale(sight_range_frame, from_=1, to=SimulationEngine.MAX_POSITION_X, orient=HORIZONTAL, length=300,
                          variable=sight_range_value)
sight_range_scale.pack(side=LEFT)
sight_range_scale.set(SimulationEngine.SIGHT_RANGE)

sight_range_bt = Button(sight_range_frame, text="Set", command=set_sight_range)
sight_range_bt.pack(side=LEFT)



############################################################

sight_angle_frame = Frame(frame)
sight_angle_frame.pack(side=TOP)

sight_angle_label = Label(sight_angle_frame, text="Sight Angle")
sight_angle_label.pack(side=LEFT)

sight_angle_scale = Scale(sight_angle_frame, from_=0, to=360, orient=HORIZONTAL, length=300,
                          variable=sight_angle_value)
sight_angle_scale.pack(side=LEFT)
sight_angle_scale.set(SimulationEngine.SEE_ANGLE)

sight_range_bt = Button(sight_angle_frame, text="Set", command=set_angle_range)
sight_range_bt.pack(side=LEFT)

############################################################

to_close_frame = Frame(frame)
to_close_frame.pack(side=TOP)

to_close_label = Label(to_close_frame, text="Too Close Range")
to_close_label.pack(side=LEFT)

to_close_scale = Scale(to_close_frame, from_=1, to=SimulationEngine.MAX_POSITION_X, orient=HORIZONTAL, length=300,
                       variable=to_close_val)
to_close_scale.pack(side=LEFT)
to_close_scale.set(SimulationEngine.TOO_CLOSE_RANGE)

to_close_bt = Button(to_close_frame, text="Set", command=set_too_close)
to_close_bt.pack(side=LEFT)

############################################################


rule1_frame = Frame(frame)
rule1_frame.pack(side=TOP)

rule1_label = Label(rule1_frame, text="Rule1 Divider")
rule1_label.pack(side=LEFT)

rule1_scale = Scale(rule1_frame, from_=1, to=1000, orient=HORIZONTAL, length=300, variable=rule_1_val)
rule1_scale.pack(side=LEFT)
rule1_scale.set(SimulationEngine.RULE1_DIVIDER)

rule1_bt = Button(rule1_frame, text="Set", command=set_rule1)
rule1_bt.pack(side=LEFT)

############################################################

rule3_frame = Frame(frame)
rule3_frame.pack(side=TOP)

rule3_label = Label(rule3_frame, text="Rule3 Divider")
rule3_label.pack(side=LEFT)

rule3_scale = Scale(rule3_frame, from_=1, to=1000, orient=HORIZONTAL, length=300, variable=rule_3_val)
rule3_scale.pack(side=LEFT)
rule3_scale.set(SimulationEngine.RULE3_DIVIDER)

rule3_bt = Button(rule3_frame, text="Set", command=set_rule3)
rule3_bt.pack(side=LEFT)

############################################################

start_bt = Button(frame, text="Start", command=start_sim)
start_bt.pack(side=BOTTOM)
root.mainloop()


