"""A simple script that connects with a wii controller and starts experiment"""

import errno
import time
from select import poll, POLLIN
import threading
import Queue
from src.experiment import Experiment
from src.tasks_gui import TasksGui

class App(threading.Thread):
    """A application class puts accel data into a queue"""

    def __init__(self):
        try:
            self.xwiimote = __import__("xwiimote")
        except ImportError:
            print "No xwiimote found"
            exit(1)
        else:
            self.fd_value = None
            self.dev = None
            self.ini_xwii()
            self.queue = Queue.Queue()
            self.poll = poll()
            self.poll.register(self.fd_value, POLLIN)
            self.loop_active = True
            gui = TasksGui()
            experiment = Experiment(gui)
            threading.Thread.__init__(self)
            self.start()
            output_file = None
            while self.loop_active:
                evt = self.queue.get()
                if evt[0] == 1:
                    experiment.press_b_down(evt[1])
                elif evt[0] == 2:
                    experiment.press_b_up(evt[1])
                    if experiment.is_finished():
                        output_file = open(
                            "data/record-"+str(time.time())+".txt", "w"
                        )
                        output_file.write(experiment.get_output())
                        output_file.close()
                        self.loop_active = False
                elif evt[0] == 3:
                    experiment.accel(evt[1], evt[2], evt[3], evt[4])
                elif evt[0] == 4:
                    self.loop_active = False
            gui.quit()

    def ini_xwii(self):
        """Find the WiiController"""

        # display a constant
        print "=== " + self.xwiimote.NAME_CORE + " ==="

        # list wiimotes and remember the first one
        try:
            mon = self.xwiimote.monitor(True, True)
            print "mon fd", mon.get_fd(False)
            ent = mon.poll()
            first_wiimote = ent
            while ent is not None:
                print "Found device: " + ent
                ent = mon.poll()
        except SystemError as ex:
            print "ooops, cannot create monitor (", ex, ")"

        # continue only if there is a wiimote
        if first_wiimote is None:
            print "No wiimote to read"
            exit(0)

        # create a new iface
        try:
            self.dev = self.xwiimote.iface(first_wiimote)
        except IOError as ex:
            print "ooops,", ex
            exit(1)

        # display some information and open the iface
        try:
            print "syspath:" + self.dev.get_syspath()
            self.fd_value = self.dev.get_fd()
            print "fd:", self.fd_value
            print "opened mask:", self.dev.opened()
            self.dev.open(
                self.dev.available() | self.xwiimote.IFACE_WRITABLE
            )
            print "opened mask:", self.dev.opened()
            print "capacity:", self.dev.get_battery(), "%"
        except SystemError as ex:
            print "ooops", ex
            exit(1)

    def run(self):
        # read some values
        evt = self.xwiimote.event()
        local_loop_active = True
        while local_loop_active and self.loop_active:
            self.poll.poll()
            try:
                self.dev.dispatch(evt)
                if evt.type == self.xwiimote.EVENT_KEY:
                    key, state = evt.get_key()
                    if key == self.xwiimote.KEY_B:
                        if state == 1:
                            self.queue.put([1, time.time()])
                        elif state == 0:
                            self.queue.put([2, time.time()])
                elif evt.type == self.xwiimote.EVENT_ACCEL:
                    x_value, y_value, z_value = evt.get_abs(0)
                    self.queue.put([3, x_value, y_value, z_value, time.time()])
                if evt.type == self.xwiimote.EVENT_GONE:
                    self.queue.put([4])
                    local_loop_active = False
            except IOError as ex:
                if ex.errno != errno.EAGAIN:
                    print "Bad"
                    exit(0)

App()
exit(0)
