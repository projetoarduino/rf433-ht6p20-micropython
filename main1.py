import ht6p20
import time

rf433 = ht6p20.In(36) #interrupt pin

while True:
    code = rf433.read()
    #print(code)
    time.sleep_ms(100)

    