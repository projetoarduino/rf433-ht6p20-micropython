import ht6p20
import time
from power import Power #coment if you not use m5stack core2
import _thread
Power()

count = 0
# not work correct in a tread
def readSensorsRF():
    rf433 = ht6p20.Start(36)
    while True:
        rf433.readRF()
        time.sleep_us(1)


_thread.start_new_thread(readSensorsRF, ())

while True:
    count = count + 1
    print("Running", count)
    time.sleep_ms(10)

#correct way but not usefull
# rf433 = ht6p20.Start(36)
# while True:    
#     rf433.readRF()