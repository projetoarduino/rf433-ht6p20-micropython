# based on https://acturcato.wordpress.com/2013/12/20/decodificador-para-o-encoder-ht6p20b-em-arduino/
# and direct converted from arduino code

from machine import Pin
import time

class In:
    def __init__(self, pin1):
        self.result = None
        self.start_dur0 = 0
        self.dur0 = 0
        self.start_dur1 = 0
        self.dur1 = 0
        self.wave_lambda = 0
        self.buffer = 0
        self.counter = 0
        self.startbit = False
        self.addr = 0
        if pin1 is not None:
            self.pin = Pin(pin1, Pin.IN, pull = Pin.PULL_DOWN) #before Pin.PULL_DOWN
            #self.pin.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.trig)
            self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.trig)

    def trig(self, pin):
        if self.pin.value() == 0:
            self.start_dur0 = time.ticks_us()
        elif self.start_dur0 is not 0:
            #self.dur0 = time.ticks_diff(time.ticks_us(), self.start_dur0)
            self.dur0 = abs(self.start_dur0 - time.ticks_us())
            self.start_dur0 = 0

        if self.pin.value() == 1:
            self.start_dur1 = time.ticks_us()
        elif self.start_dur1 is not 0:
            #self.dur1 = time.ticks_diff(time.ticks_us(), self.start_dur1
            self.dur1 = abs(self.start_dur1 - time.ticks_us())
            self.start_dur1 = 0
                
        #If time at "0" is between 9200 us (23 cycles of 400us) and 13800 us (23 cycles of 600 us).
        if self.dur0 > 9200 and self.dur0 < 13800 and self.startbit == False:
            #print(self.dur0, self.dur1)
            #calculate wave length - lambda
            self.wave_lambda = self.dur0 / 23
      
            #Reset variables
            self.dur0 = 0
            self.buffer = 0
            self.counter = 0      
            self.startbit = True

        if self.startbit == True and self.counter < 28:
            self.counter += 1
    
            if self.dur1 > 0.5 * self.wave_lambda and self.dur1 < 1.5 * self.wave_lambda:  #If pulse width at "1" is between "0.5 and 1.5 lambda", means that pulse is only one lambda, so the data é "1".
                self.buffer = (self.buffer << 1) + 1   # add "1" on data buffer    
            elif self.dur1 > 1.5 * self.wave_lambda and self.dur1 < 2.5 * self.wave_lambda:  #If pulse width at "1" is between "1.5 and 2.5 lambda", means that pulse is two lambdas, so the data é "0".
                self.buffer = (self.buffer << 1) + 0    #add "0" on data buffer
            else:
                #Reset the loop
                self.startbit = False

        #Check if all 28 bits were received (22 of Address + 2 of Data + 4 of Anti-Code)
        if self.counter == 28:
            print("->", self.buffer, self.buffer >> 6, )
            print("->", bin(self.buffer))
            print("->", bin(self.buffer >> 6))
            self.counter = 0
            self.startbit = False
            
            # #I can't extract the Anti-Code or the data
            # #Check if Anti-Code is OK (last 4 bits of buffer equal "0101")
            # if bin(self.buffer)[2] == "1" and bin(self.buffer)[3] == "0" and bin(self.buffer)[4] == "1" and bin(self.buffer)[5] == "0":     
            #     self.counter = 0
            #     self.startbit = False
      
            #     #Get ADDRESS CODE from Buffer
            #     self.addr = self.buffer >> 6
            # else:    
            #     #Reset the loop
            
    
    def read(self):
        return self.buffer