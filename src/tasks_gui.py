"""This script contains the Tasks Gui class"""

from Tkinter import Tk, Label, TOP, BOTH, YES
from PIL import ImageTk, Image

class TasksGui(object):
    """A small Tkinter GUI that shows the tasks"""

    def __init__(self):
        self.root = Tk()
        self.size = (
            2560,
            self.root.winfo_screenheight()
        )
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % self.size)
        self.image_count = 19
        self.task_index = 0
        self.task_images = range(self.image_count)
        self.photo_images = range(self.image_count)
        for i in range(self.image_count):
            self.task_images[i] = Image.open(
                "img/" + str(i + 1) + ".png"
            )
            self.task_images[i] = self.task_images[i].resize(self.size, Image.ANTIALIAS)
            self.photo_images[i] = ImageTk.PhotoImage(self.task_images[i])
            print "Preload img/" + str(i + 1) + ".png"
        self.panel = Label(
            self.root,
            image=self.photo_images[0],
            background='white'
        )
        self.panel.pack(side=TOP, fill=BOTH, expand=YES)
        self.root.update()

    def next_task(self):
        """Continues with the next task"""
        self.task_index = self.task_index + 1
        self.panel.configure(image=self.photo_images[self.task_index])
        self.panel.image = self.photo_images[self.task_index]
        self.root.update()

    def is_finished(self):
        """Returns the status of the tasks"""
        if self.task_index >= self.image_count - 1:
            return True
        return False

    def get_task_index(self):
        """Returns the task index"""
        return self.task_index

    def quit(self):
        self.root.quit()
        self.root.update()
