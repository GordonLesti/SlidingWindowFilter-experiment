"""A simple script that connects with a wii controller and starts experiment"""

import errno
import time
from select import poll, POLLIN
import xwiimote

# display a constant
print "=== " + xwiimote.NAME_CORE + " ==="

# list wiimotes and remember the first one
try:
    MON = xwiimote.monitor(True, True)
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
    DEV = xwiimote.iface(FIRST_WIIMOTE)
except IOError as ex:
    print "ooops,", ex
    exit(1)

# display some information and open the iface
try:
    print "syspath:" + DEV.get_syspath()
    FD = DEV.get_fd()
    print "fd:", FD
    print "opened mask:", DEV.opened()
    DEV.open(DEV.available() | xwiimote.IFACE_WRITABLE)
    print "opened mask:", DEV.opened()
    print "capacity:", DEV.get_battery(), "%"
except SystemError as ex:
    print "ooops", ex
    exit(1)

# read some values
POLL = poll()
POLL.register(FD, POLLIN)
EVT = xwiimote.event()
CONST_N = 0
RECORD = False
OUTPUT = ""
OUTPUT_FILE = None
START_TIME = 0
while CONST_N < 2:
    POLL.poll()
    try:
        DEV.dispatch(EVT)
        if EVT.type == xwiimote.EVENT_KEY:
            KEY, STATE = EVT.get_key()
            if KEY == xwiimote.KEY_A and STATE == 1:
                if not RECORD:
                    print "RECORD"
                    RECORD = True
                    OUTPUT = ""
                    START_TIME = int(round(time.time() * 1000))
                else:
                    print "STOP RECORD"
                    RECORD = False
                    OUTPUT_FILE = open(
                        "../data/record-"+str(time.time())+".txt", "w"
                    )
                    OUTPUT_FILE.write(OUTPUT)
                    OUTPUT_FILE.close()
                    CONST_N = 2
            elif RECORD and KEY == xwiimote.KEY_B:
                if STATE == 1:
                    print "START"
                    OUTPUT += str(int(round(time.time() * 1000)) - START_TIME) \
                    + " START\n"
                elif STATE == 0:
                    print "END"
                    OUTPUT += str(int(round(time.time() * 1000)) - START_TIME) \
                    + " END\n"
        elif EVT.type == xwiimote.EVENT_ACCEL:
            X_VALUE, Y_VALUE, Z_VALUE = EVT.get_abs(0)
            OUTPUT += str(int(round(time.time() * 1000)) - START_TIME) + " " \
            + str(X_VALUE) + " " + str(Y_VALUE) + " " + str(Z_VALUE) + "\n"
        elif EVT.type == xwiimote.EVENT_GONE:
            print "Gone"
            CONST_N = 2
    except IOError as ex:
        if ex.errno != errno.EAGAIN:
            print "Bad"
            exit(0)

exit(0)
