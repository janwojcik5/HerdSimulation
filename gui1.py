from Tkinter import *


def set_velocity():
    selection = "Value= " + str(velocity_value.get())
    print selection



def set_velocity1():
    selection = "Value1= " + str(velocity_value1.get())
    print selection


def set_velocity2():
    selection = "Value2 = " + str(velocity_value1.get())
    print selection


def set_velocity3():
    selection = "Value3= " + str(velocity_value1.get())
    print selection

def set_velocity4():
    selection = "Value4 = " + str(velocity_value1.get())
    print selection

def set_velocity5():
    selection = "Value5 = " + str(velocity_value1.get())
    print selection




root = Tk()
frame = Frame(root)
frame.pack()


############################################################

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

velocity_label = Label(bottomframe, text="Max velocity")
velocity_label.pack(side=LEFT)

velocity_value = DoubleVar()
velocity_scale = Scale( bottomframe, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value )
velocity_scale.pack(side=LEFT)

velocity_set_bt = Button(bottomframe, text="Set", command=set_velocity)
velocity_set_bt.pack(side=LEFT)

############################################################

bottomframe1 = Frame(frame)
bottomframe1.pack(side=BOTTOM)

velocity_label1 = Label(bottomframe1, text="Max velocity")
velocity_label1.pack(side=LEFT)

velocity_value1 = DoubleVar()
velocity_scale1 = Scale(bottomframe1, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value1)
velocity_scale1.pack(side=LEFT)

velocity_set_bt1 = Button(bottomframe1, text="Set", command=set_velocity1)
velocity_set_bt1.pack(side=LEFT)

############################################################

bottomframe2 = Frame(frame)
bottomframe2.pack(side=BOTTOM)

velocity_label2 = Label(bottomframe2, text="Max velocity")
velocity_label2.pack(side=LEFT)

velocity_value2 = DoubleVar()
velocity_scale2 = Scale(bottomframe2, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value2)
velocity_scale2.pack(side=LEFT)

velocity_set_bt2 = Button(bottomframe2, text="Set", command=set_velocity2)
velocity_set_bt2.pack(side=LEFT)

############################################################

bottomframe3 = Frame(frame)
bottomframe3.pack(side=BOTTOM)

velocity_label3 = Label(bottomframe3, text="Max velocity")
velocity_label3.pack(side=LEFT)

velocity_value3 = DoubleVar()
velocity_scale3 = Scale(bottomframe3, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value3)
velocity_scale3.pack(side=LEFT)

velocity_set_bt3 = Button(bottomframe3, text="Set", command=set_velocity3)
velocity_set_bt3.pack(side=LEFT)

############################################################

bottomframe4 = Frame(frame)
bottomframe4.pack(side=BOTTOM)

velocity_label4 = Label(bottomframe4, text="Max velocity")
velocity_label4.pack(side=LEFT)

velocity_value4 = DoubleVar()
velocity_scale4 = Scale(bottomframe4, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value4)
velocity_scale4.pack(side=LEFT)

velocity_set_bt4 = Button(bottomframe4, text="Set", command=set_velocity4)
velocity_set_bt4.pack(side=LEFT)

############################################################

bottomframe5 = Frame(frame)
bottomframe5.pack(side=BOTTOM)

velocity_label5 = Label(bottomframe5, text="Max velocity")
velocity_label5.pack(side=LEFT)

velocity_value5 = DoubleVar()
velocity_scale5 = Scale(bottomframe5, from_=1, to=10, orient=HORIZONTAL, length=300, variable=velocity_value5)
velocity_scale5.pack(side=LEFT)

velocity_set_bt5 = Button(bottomframe5, text="Set", command=set_velocity5)
velocity_set_bt5.pack(side=LEFT)


root.mainloop()
