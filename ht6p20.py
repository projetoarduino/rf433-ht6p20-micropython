from machine import Pin, time_pulse_us


class Start:
    def __init__(self, pinNumber):
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
        self.data_return = ""
        self.pin = Pin(pinNumber, Pin.IN, pull=Pin.PULL_DOWN)

    def readRF(self):
        if self.startbit == False:
            # Check the PILOT CODE until START BIT;
            self.dur0 = time_pulse_us(self.pin, 0, 15000)

            # If time at "0" is between 9200 us (23 cycles of 400us) and 13800 us (23 cycles of 600 us).
            if self.dur0 > 9200 and self.dur0 < 13800 and self.startbit == False:
                # calculate wave length - lambda
                self.wave_lambda = self.dur0 / 23
                # Reset variables
                self.dur0 = 0
                self.buffer = 0
                self.counter = 0
                self.startbit = True

        if self.startbit == True and self.counter < 28:
            self.counter += 1
            self.dur1 = time_pulse_us(self.pin, 1, 1000)
            # If pulse width at "1" is between "0.5 and 1.5 lambda", means that pulse is only one lambda, so the data é "1".
            if self.dur1 > 0.5 * self.wave_lambda and self.dur1 < (1.5 * self.wave_lambda):
                self.buffer = (self.buffer << 1) + 1   # add "1" on data buffer
            # If pulse width at "1" is between "1.5 and 2.5 lambda", means that pulse is two lambdas, so the data é "0".
            elif self.dur1 > 1.5 * self.wave_lambda and self.dur1 < (2.5 * self.wave_lambda):
                self.buffer = (self.buffer << 1)  # add "0" on data buffer
            else:
                # Reset the loop
                self.startbit = False

        # Check if all 28 bits were received (22 of Address + 2 of Data + 4 of Anti-Code)
        if self.counter == 28:            
            data = '{0:b}'.format(self.buffer)
            # Check if Anti-Code is OK (last 4 bits of buffer equal "0101")
            # Estou compensan o 0b no inicio e acrescentei um verificação de tamanho da string para evitar o out of range 
            if len(data) == 28 and data[25] == "0" and data[26] == "1" and data[27] == "0":
                self.counter = 0
                self.startbit = False

                addr = self.buffer >> 6
                #print("->", data, addr, data[23], data[24]) #data binary, address, button 1, button 2    
                self.data_return = '{},{},{},{}'.format(addr, data[23], data[24], data)
                print(self.data_return)
            else:
                # Reset the loop
                self.startbit = False

    def read(self):
        return self.data_return
