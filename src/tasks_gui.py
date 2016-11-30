"""This script contains the Tasks Gui class"""

from Tkinter import Tk, Label, TOP, BOTH, YES
from PIL import ImageTk, Image

class TasksGui(object):
    """A small Tkinter GUI that shows the tasks"""

    def __init__(self):
        self.root = Tk()
        self.image_count = 19
        self.task_index = 0
        self.task_image = Image.open(
            "img/" + str(self.task_index + 1) + ".png"
        )
        self.photo_image = ImageTk.PhotoImage(self.task_image)
        self.panel = Label(
            self.root,
            image=self.photo_image,
            background='white'
        )
        self.panel.pack(side=TOP, fill=BOTH, expand=YES)
        self.root.update()

    def next_task(self):
        """Continues with the next task"""
        self.task_index = self.task_index + 1
        self.task_image = Image.open(
            "img/" + str(self.task_index + 1) + ".png"
        )
        self.photo_image = ImageTk.PhotoImage(self.task_image)
        self.panel.configure(image=self.photo_image)
        self.panel.image = self.photo_image
        self.root.update()

    def is_finished(self):
        """Returns the status of the tasks"""
        if self.task_index >= self.image_count - 1:
            return True
        return False

    def get_task_index(self):
        """Returns the tesk index"""
        return self.task_index
