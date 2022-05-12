import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# GUI
root = tk.Tk()
root.title("FiltersApp")

root.image_canvas = tk.Canvas(root, width=512, height=512, bg='white')
root.image_canvas.grid(column=0, row=0)

root.buttons_frame = tk.Frame(root)
root.buttons_frame.grid(column=1, row=0)

root.fig, root.axis = plt.subplots(3, figsize = (5, 5), dpi = 100)
root.fig.suptitle("HISTOGRAMS")
root.histogram_canvas = FigureCanvasTkAgg(root.fig, master=root)
root.histogram_canvas.get_tk_widget().grid(column=2, row=0)
    

# HISTOGRAM
def get_histogram(image):
    histogram_r = cv2.calcHist([image], [0], None, [256], [0,256])
    histogram_g = cv2.calcHist([image], [1], None, [256], [0,256])
    histogram_b = cv2.calcHist([image], [2], None, [256], [0,256])
    return histogram_r, histogram_g, histogram_b
        
def plot_histogram():
    histograms = get_histogram(root.image)
    colors = ["RED", "GREEN", "BLUE"]
    
    for i in range(len(histograms)):
        root.axis[i].clear()
        root.axis[i].plot(histograms[i], color=colors[i])

    root.histogram_canvas.draw()
       

# IMAGE
def set_image(image):
    root.image = image
    # convert to image format and save reference
    array_image = Image.fromarray(image)
    root.photo_image = ImageTk.PhotoImage(array_image)
    # canvas create image, nw->northwest
    root.image_canvas.create_image(0, 0, anchor='nw', image=root.photo_image)
    # update histogram
    plot_histogram()

def load_image():
    image = cv2.imread('../img/Lenna.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    set_image(image)


# FILTERS
def blur_filter():
    image = cv2.blur(root.image, (5,5))
    set_image(image)
    
    

# BUTTONS
root.load_button = tk.Button(root.buttons_frame, text="LOAD IMAGE", command=load_image)
root.load_button.pack()

root.median_button = tk.Button(root.buttons_frame, text="MEDIAN FILTER", command=blur_filter)
root.median_button.pack()


# MAIN LOOP
root.mainloop()