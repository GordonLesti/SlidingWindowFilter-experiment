"""This script contains the Tasks Gui class"""

from PIL import ImageTk
import PIL.Image
from Tkinter import *

class TasksGui(object):
    def __init__(self):
        self.root = Tk()
        self.image_count = 10
        self.task_index = 0
        self.task_image = PIL.Image.open("img/" + str(self.task_index + 1) + ".png")
        self.photo_image = ImageTk.PhotoImage(self.task_image)
        self.panel = Label(self.root, image=self.photo_image, background='white')
        self.panel.pack(side=TOP, fill=BOTH, expand=YES)
        self.root.update()

    def update(self):
        self.root.update()

    def next_task(self):
        self.task_index = self.task_index + 1
        self.task_image = PIL.Image.open("img/" + str(self.task_index + 1) + ".png")
        self.photo_image = ImageTk.PhotoImage(self.task_image)
        self.panel.configure(image=self.photo_image)
        self.panel.image = self.photo_image
        self.root.update()

    def is_finished(self):
        """Returns the status of the tasks"""
        if self.task_index >= self.image_count:
            return True
        return False

    def get_task_index(self):
        return self.task_index
