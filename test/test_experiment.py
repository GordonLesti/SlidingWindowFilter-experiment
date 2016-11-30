"""This script contains tests for the Experiment class"""

import unittest
from src.experiment import Experiment

class TasksMock(object):
    """A small test class that mocks the task GUI"""

    def __init__(self):
        self.image_count = 19
        self.task_index = 0

    def next_task(self):
        """Continues with the next task"""
        self.task_index = self.task_index + 1

    def is_finished(self):
        """Returns the status of the test tasks"""
        if self.task_index + 1 >= self.image_count:
            return True
        return False

    def get_task_index(self):
        """Returns the tesk index"""
        return self.task_index


# pylint: disable=R0904
class TestExperiment(unittest.TestCase):
    """A class that tests the class Experiment"""
    def test_accel(self):
        """Tests the method accel"""
        experiment = Experiment(TasksMock())
        experiment.accel(80, 48, 97)
        experiment.accel(3, 42, 79)
        self.assertRegexpMatches(
            experiment.get_output(),
            '^[0-9]* 80 48 97\n[0-9]* 3 42 79\n$'
        )

    def test_press_b_success(self):
        """Tests the method press_b_down"""
        experiment = Experiment(TasksMock())
        experiment.accel(80, 48, 97)
        experiment.press_b_down()
        experiment.accel(3, 42, 79)
        experiment.press_b_up()
        experiment.accel(56, 21, 43)
        experiment.press_b_down()
        experiment.accel(62, 32, 28)
        experiment.press_b_up()
        self.assertRegexpMatches(
            experiment.get_output(),
            '^[0-9]* 80 48 97\n[0-9]* START 0\n[0-9]* 3 42 79\n[0-9]* END 0' \
            '\n[0-9]* 56 21 43\n[0-9]* START 1\n[0-9]* 62 32 28\n[0-9]* END ' \
            '1\n$'
        )

    def test_is_finished(self):
        """Tests the method is_finished"""
        experiment = Experiment(TasksMock())
        self.assertEquals(False, experiment.is_finished())
        for _ in range(0, 17):
            experiment.press_b_down()
            self.assertEquals(False, experiment.is_finished())
            experiment.press_b_up()
            self.assertEquals(False, experiment.is_finished())
        experiment.press_b_down()
        self.assertEquals(False, experiment.is_finished())
        experiment.press_b_up()
        self.assertEquals(True, experiment.is_finished())

if __name__ == "__main__":
    unittest.main()
