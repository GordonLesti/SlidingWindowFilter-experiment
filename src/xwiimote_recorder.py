"""A simple script that connects with a wii controller and starts experiment"""

import errno
import time
from select import poll, POLLIN
from src.experiment import Experiment
from src.tasks_gui import TasksGui
import threading
import Queue

class App(threading.Thread):
    def __init__(self):
        try:
            self.XWIIMOTE = __import__("xwiimote")
        except ImportError:
            print "No xwiimote found"
            exit(1)
        else:
            # display a constant
            print "=== " + self.XWIIMOTE.NAME_CORE + " ==="

            # list wiimotes and remember the first one
            try:
                MON = self.XWIIMOTE.monitor(True, True)
                print "mon fd", MON.get_fd(False)
                ENT = MON.poll()
                FIRST_WIIMOTE = ENT
                while ENT is not None:
                    print "Found device: " + ENT
                    ENT = MON.poll()
            except SystemError as ex:
                print "ooops, cannot create monitor (", ex, ")"

            # continue only if there is a wiimote
            if FIRST_WIIMOTE is None:
                print "No wiimote to read"
                exit(0)

            # create a new iface
            try:
                self.DEV = self.XWIIMOTE.iface(FIRST_WIIMOTE)
            except IOError as ex:
                print "ooops,", ex
                exit(1)

            # display some information and open the iface
            try:
                print "syspath:" + self.DEV.get_syspath()
                FD = self.DEV.get_fd()
                print "fd:", FD
                print "opened mask:", self.DEV.opened()
                self.DEV.open(self.DEV.available() | self.XWIIMOTE.IFACE_WRITABLE)
                print "opened mask:", self.DEV.opened()
                print "capacity:", self.DEV.get_battery(), "%"
            except SystemError as ex:
                print "ooops", ex
                exit(1)

            self.queue = Queue.Queue()
            self.POLL = poll()
            self.POLL.register(FD, POLLIN)
            self.loop_active = True
            gui = TasksGui()
            EXPERIMENT = Experiment(gui)
            threading.Thread.__init__(self)
            self.start()
            OUTPUT = ""
            OUTPUT_FILE = None
            while self.loop_active:
                evt = self.queue.get()
                if evt[0] == 1:
                    EXPERIMENT.press_b_down(evt[1])
                elif evt[0] == 2:
                    EXPERIMENT.press_b_up(evt[1])
                    if EXPERIMENT.is_finished():
                        OUTPUT_FILE = open("data/record-"+str(time.time())+".txt", "w")
                        OUTPUT_FILE.write(EXPERIMENT.get_output())
                        OUTPUT_FILE.close()
                        self.loop_active = False
                elif evt[0] == 3:
                    EXPERIMENT.accel(evt[1], evt[2], evt[3], evt[4])
                elif evt[0] == 4:
                    self.loop_active = False
            gui.quit()

    def run(self):
        # read some values
        evt = self.XWIIMOTE.event()
        CONST_N = 0
        while CONST_N < 2 and self.loop_active:
            self.POLL.poll()
            try:
                self.DEV.dispatch(evt)
                if evt.type == self.XWIIMOTE.EVENT_KEY:
                    KEY, STATE = evt.get_key()
                    if KEY == self.XWIIMOTE.KEY_B:
                        if STATE == 1:
                            self.queue.put([1, time.time()])
                        elif STATE == 0:
                            self.queue.put([2, time.time()])
                elif evt.type == self.XWIIMOTE.EVENT_ACCEL:
                    X_VALUE, Y_VALUE, Z_VALUE = evt.get_abs(0)
                    self.queue.put([3, X_VALUE, Y_VALUE, Z_VALUE, time.time()])
                if evt.type == self.XWIIMOTE.EVENT_GONE:
                    self.queue.put([4])
                    CONST_N = 2
            except IOError as ex:
                if ex.errno != errno.EAGAIN:
                    print "Bad"
                    exit(0)

App()
exit(0)
