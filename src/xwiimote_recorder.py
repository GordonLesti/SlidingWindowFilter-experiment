"""A simple script that connects with a wii controller and starts experiment"""

import errno
import time
from select import poll, POLLIN
from src.experiment import Experiment
from src.tasks_gui import TasksGui
try:
    XWIIMOTE = __import__("xwiimote")
except ImportError:
    print "No xwiimote found"
    exit(1)
else:
    # display a constant
    print "=== " + XWIIMOTE.NAME_CORE + " ==="

    # list wiimotes and remember the first one
    try:
        MON = XWIIMOTE.monitor(True, True)
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
        DEV = XWIIMOTE.iface(FIRST_WIIMOTE)
    except IOError as ex:
        print "ooops,", ex
        exit(1)

    # display some information and open the iface
    try:
        print "syspath:" + DEV.get_syspath()
        FD = DEV.get_fd()
        print "fd:", FD
        print "opened mask:", DEV.opened()
        DEV.open(DEV.available() | XWIIMOTE.IFACE_WRITABLE)
        print "opened mask:", DEV.opened()
        print "capacity:", DEV.get_battery(), "%"
    except SystemError as ex:
        print "ooops", ex
        exit(1)

    # read some values
    POLL = poll()
    POLL.register(FD, POLLIN)
    EVT = XWIIMOTE.event()
    CONST_N = 0
    OUTPUT = ""
    OUTPUT_FILE = None
    EXPERIMENT = Experiment(TasksGui())
    START_TIME = 0
    while CONST_N < 2:
        POLL.poll()
        try:
            DEV.dispatch(EVT)
            if EVT.type == XWIIMOTE.EVENT_KEY:
                KEY, STATE = EVT.get_key()
                if KEY == XWIIMOTE.KEY_B:
                    if STATE == 1:
                        EXPERIMENT.press_b_down()
                    elif STATE == 0:
                        EXPERIMENT.press_b_up()
                        if EXPERIMENT.is_finished():
                            OUTPUT_FILE = open(
                                "data/record-"+str(time.time())+".txt", "w"
                            )
                            OUTPUT_FILE.write(EXPERIMENT.get_output())
                            OUTPUT_FILE.close()
                            CONST_N = 2
            elif EVT.type == XWIIMOTE.EVENT_ACCEL:
                X_VALUE, Y_VALUE, Z_VALUE = EVT.get_abs(0)
                EXPERIMENT.accel(X_VALUE, Y_VALUE, Z_VALUE)
            elif EVT.type == XWIIMOTE.EVENT_GONE:
                print "Gone"
                CONST_N = 2
        except IOError as ex:
            if ex.errno != errno.EAGAIN:
                print "Bad"
                exit(0)

exit(0)
