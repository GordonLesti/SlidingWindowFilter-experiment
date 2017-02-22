"""This script contains the Experiment class"""

import time

class Experiment(object):
    """A class that represents a experiment with accel data"""

    def __init__(self, tasks):
        self.output = ""
        self.task_index = 0
        self.start_time = int(round(time.time() * 1000))
        self.tasks = tasks
        self.button_b_down = False

    def accel(self, x_value, y_value, z_value, rec_time):
        """Store accel data"""
        self.output += self.__get_experiment_time_string(rec_time) + " " \
        + str(x_value) + " " + str(y_value) + " " + str(z_value) + "\n"

    def press_b_down(self, rec_time):
        """Handle B button pressed down"""
        if self.button_b_down:
            raise Exception('Button B is already down.')
        self.button_b_down = True
        self.output += (self.__get_experiment_time_string(rec_time) + " START " \
        + str(self.tasks.get_task_index()) + "\n")

    def press_b_up(self, rec_time):
        """Handle B button pressed up"""
        if not self.button_b_down:
            raise Exception('Button B is already up.')
        self.button_b_down = False
        self.output += self.__get_experiment_time_string(rec_time) + " END " \
        + str(self.tasks.get_task_index()) + "\n"
        self.tasks.next_task()

    def is_finished(self):
        """Returns the status of the experiment"""
        return self.tasks.is_finished()

    def get_output(self):
        """Returns the output of the experiment"""
        return self.output

    def __get_experiment_time_string(self, rec_time):
        """Returns the current experiment time as string"""
        return str(int(round(rec_time * 1000)) - self.start_time)
