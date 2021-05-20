from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sys
import numpy as np
from sklearn.datasets import load_digits
import pylab as pl
from PIL import Image, ImageDraw, ImageOps

# constants, counters, global variables
epoch = 20
maxerr = [[], [], [], [], [], [], [], [], [], []]
learning_rate = 0.7
momentum = 0.3
IMG_L = 8
Input_layer = np.zeros(IMG_L**2)
# Functions for normalizing inputs from 2d image array to 1d array [-1,1]


def normalize_inputs(z):
    return z/7.5 - 1


def normalize_gray(a):
    b = np.array([])
    for lay in a:
        b_lay = np.array([])
        for px in lay:
            b_lay = np.append(b_lay, np.round(np.sum(px) / 51))
        if len(b) < 2:
            b = b_lay
        else:
            b = np.append([b], [b_lay])
    return b
# Class for NN layer


class Layer:
    def __init__(self, neuron_count, input_count):
        self.ncount = neuron_count
        self.icount = input_count

        self.error = np.zeros(neuron_count)
        self.sum = np.zeros(neuron_count)
        # bias, I1, I2
        self.weight = np.zeros((input_count + 1)*neuron_count)
        self.weight.shape = (neuron_count, input_count + 1)
        self.adj = np.zeros((input_count + 1)*neuron_count)
        self.adj.shape = (neuron_count, input_count + 1)
        self.out = np.zeros(neuron_count)
        self.inp = np.zeros(input_count)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def d_sigmoid(self, z):
        return np.multiply(z, 1 - z)

    def weight_randomize(self):
        self.weight = np.multiply(np.random.rand(
            self.ncount, self.icount+1), 2) - 1

    def forward_sum(self, i):
        # Add Bias
        imputs1 = np.append([1], self.inp)
        res = np.sum(np.multiply(imputs1, self.weight[i]))
        return res

    def output_calc(self):
        for i in range(self.ncount):
            self.out[i] = self.sigmoid(self.forward_sum(i))

    def output_error(self, expectation):
        for i in range(self.ncount):
            self.error[i] = (expectation[i] - self.out[i]) * \
                self.d_sigmoid(self.out[i])

    def hidden_error(self, next_error, next_weights):
        for i in range(self.ncount):
            buffer = next_weights[:, i+1]
            self.error[i] = (np.sum(np.multiply(next_error, buffer))
                             )*self.d_sigmoid(self.out[i])

    def weight_correction(self):
        global learning_rate
        global momentum
        for i in range(self.ncount):
            inertion = np.multiply(momentum, self.adj[i])
            self.adj[i] = np.multiply(learning_rate, np.multiply(
                np.append([1], self.inp), self.error[i])) - inertion
            self.weight[i] += self.adj[i]


# creating neural network
H1_layer = Layer(64, 64)
H2_layer = Layer(32, 64)
O_layer = Layer(10, 32)
# Set weights
H1_layer.weight_randomize()
H2_layer.weight_randomize()
O_layer.weight_randomize()
# Paint class


class ImageGenerator:
    def __init__(self, parent, posx, posy, *kwargs):

        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = Canvas(
            self.parent, width=self.sizex, height=self.sizey, bg="white")
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = Button(self.parent, text="Done!",
                             width=10, bg='white', command=self.save)
        self.button.place(x=self.sizex/7, y=posy+self.sizey+20)
        self.button1 = Button(self.parent, text="Clear!",
                              width=10, bg='white', command=self.clear)
        self.button1.place(x=(self.sizex/7)+80, y=posy+self.sizey+20)

        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def save(self):
        filename = "temp.bmp"
        inverted_image = ImageOps.invert(self.image)
        scaled_image = inverted_image.resize((8, 8), Image.ANTIALIAS)
        scaled_image.save(filename)
        im = Image.open("temp.bmp")
        a = np.array(im)
        b = normalize_inputs(normalize_gray(a))
        global Input_layer
        Input_layer = np.array(b).flatten()

    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(
                    self.xold, self.yold, event.x, event.y, smooth='true', width=8, fill='black')
                self.draw.line(
                    ((self.xold, self.yold), (event.x, event.y)), (0, 0, 0), width=8)

        self.xold = event.x
        self.yold = event.y
# Top error graphics class


class ErrorGraphics:
    def __init__(self, master):
        errFrame = Frame(master, bg="gray")
        errFrame.pack()
        # initialize graphics
        self.f = Figure(figsize=(7, 2), dpi=100)
        self.a = self.f.add_subplot(111)
        self.s = [[], [], [], [], [], [], [], [], [], []]
        # initialize matplotlib canvas
        self.err_canvas = FigureCanvasTkAgg(self.f, master=errFrame)
        self.err_canvas.draw()
        self.err_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        # initialize matplotlib navigation panel
        self.toolbar = NavigationToolbar2TkAgg(self.err_canvas, errFrame)
        self.toolbar.update()
        self.err_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def refresh_plot(self):
        self.a.clear()
        for xx in self.s:
            self.a.plot(range(len(xx)), xx)
        self.err_canvas.draw()
        plt.gcf().canvas.draw()


# FORM
root = Tk()
root.wm_title("Embedding in TK")
root.wm_geometry("%dx%d+%d+%d" % (520, 520, 10, 10))
# Error graphics obj
errPlot = ErrorGraphics(root)
# Paint obj
lab_paint = Label(root, text="Paint here:")
lab_paint.place(y=240, x=10)
canvas = ImageGenerator(root, 10, 260)
# button functions


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def save_inputs():
    np.savetxt("test_imput.out", Input_layer, delimiter=',')


def save_weights():
    global H1_layer
    global H2_layer
    global O_layer
    np.save("H1.npy", H1_layer.weight)
    np.save("H2.npy", H2_layer.weight)
    np.save("O.npy", O_layer.weight)
    np.savetxt("H1.out", H1_layer.weight)
    np.savetxt("H2.out", H2_layer.weight)
    np.savetxt("O.out", O_layer.weight)


def load_weights():
    global H1_layer
    global H2_layer
    global O_layer
    H1_layer.weight = np.load("H1.npy")
    H2_layer.weight = np.load("H2.npy")
    O_layer.weight = np.load("O.npy")


def shake_weights():
    global H1_layer
    global H2_layer
    global O_layer
    H1_layer.weight_randomize()
    H2_layer.weight_randomize()
    O_layer.weight_randomize()


def training():
    digits = load_digits()
    global H1_layer
    global H2_layer
    global O_layer
    global epoch
    global errPlot
    epoch_buffer = epoch
    while epoch_buffer > 0:
        print(f"\n{epoch_buffer}")
        for i in range(len(digits.images)):
            H1_layer.inp = normalize_inputs(
                np.array(digits.images[i]).flatten())
            H1_layer.output_calc()
            H2_layer.inp = H1_layer.out
            H2_layer.output_calc()
            O_layer.inp = H2_layer.out
            O_layer.output_calc()
            train_expect = np.zeros(10)
            train_expect[digits.target[i]] = 1
            O_layer.output_error(train_expect)
            O_layer.weight_correction()
            H2_layer.hidden_error(O_layer.error, O_layer.weight)
            H2_layer.weight_correction()
            H1_layer.hidden_error(H2_layer.error, H2_layer.weight)
            H1_layer.weight_correction()
            test_err = np.max(np.abs(O_layer.error))
            errPlot.s[digits.target[i]].append(test_err)
            # print(digits.target[i], "ans:", np.argmax(
            #     O_layer.out), ":", O_layer.out)
        epoch_buffer -= 1
        errPlot.refresh_plot()


def image_recognition():
    global canvas
    global Input_layer
    global tb_Result
    canvas.save()
    H1_layer.inp = Input_layer
    H1_layer.output_calc()
    H2_layer.inp = H1_layer.out
    H2_layer.output_calc()
    O_layer.inp = H2_layer.out
    O_layer.output_calc()
    print(np.argmax(O_layer.out))
    tb_Result.delete('1.0', END)
    tb_Result.insert(INSERT, np.argmax(O_layer.out))


# Epoch (Я хотел сделать бокс для ввода длины эпохи. Оставлено на потом)
'''
lab_epoch = Label(root, text = "Epoch:")
lab_epoch.place(y = 240, x = 180)
entry_epoch = Entry(root, width = 10)
entry_epoch.place(y = 240, x = 225)
c_epoch = StringVar()
lab_CURRepoch = Label(root, textvariable = c_epoch)
c_epoch.set("current epoch:", epoch)
lab_CURRepoch.place(y = 240, x = 280)
'''

# BUTTONS
# Save weights
bt_Save = Button(root, text="save weights", command=save_weights, width=15)
bt_Save.place(x=225, y=260)
# Load weights
bt_Save = Button(root, text="load weights", command=load_weights, width=15)
bt_Save.place(x=225, y=290)
# Trainings
bt_Train = Button(root, text="training", command=training, width=15)
bt_Train.place(x=225, y=320)
# Clear
bt_Set = Button(root, text="randomize weights",
                command=shake_weights, width=15)
bt_Set.place(x=225, y=350)
# Drawing_Chech
bt_Input = Button(root, text="recognition",
                  command=image_recognition, width=15)
bt_Input.place(x=225, y=380)
# Output
tb_Result = Text(font=('times', 30), width=1, height=1, wrap=CHAR)
tb_Result.place(x=350, y=300)

diapason = 0
root.mainloop()
