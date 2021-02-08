import ADwin #ADwin python module
import pyvisa as visa #Virt. Instr. Soft. Arch. to control the Arduino
import time
from Pulseshaping.Hardware.AWG520 import AWG520 #import AWG520 Class

#Define variables
ARD_PORT = 'COM7' #Arduino COM Port
ADW_PROC = 'D:\PyCharmProjects\qcomp-qapps\ESRWorking\ESRWorkingProgram\CW_ESR\Hardware\AdWIN\Trigger_Count_test_1.TB1'
avg = 0 #Counter for Average Cycling
start_freq = 2870000000 #Start Frequency in Hz
stop_freq = 2880000000 #Stop Frequency in Hz
n_read = 600 #Number of Readings
n_avg = 20 #Number of Averages (Runs)
t_dwell = 10  #Dwell time in ms
t_trig = 0.2 #Trigger pulse time in s

#initialize AWG
awg = AWG520()
print("AWG Initialized!")

#initialize the Arduino
rm = visa.ResourceManager()
arduino = rm.open_resource(ARD_PORT)
print((arduino.read()))

#initialize the ADwin
adw = ADwin.ADwin()
adw.Boot(adw.ADwindir + 'ADwin11.btl')
adw.Load_Process(ADW_PROC)
adw.Set_Par(1, n_read)
print("Adwin Initialized!")

def initiate_trig_pulse(t):
    awg.sendcommand('SOUR2:MARK2:VOLT:LOW 2.0\n')
    time.sleep(t)
    awg.sendcommand('SOUR2:MARK2:VOLT:HIGH 0.0\n')

while avg < n_avg:
    adw.Start_Process(1) #Start Counter 1 of the ADWin

    # String sent to the Arduino (This string is controlled by the arduino sketch External_Trigger)
    arduino.write(str(start_freq) + '#' + str(stop_freq) + '#' + str(n_read) + '#' + str(t_dwell) + '#')

    t1 = time.perf_counter() #Elapsed time up to this point

    time.sleep(3) #Wait for the Arduino to Initialize Serial Comm.

    initiate_trig_pulse(t_trig) #Trigger Pulse from the AWG

    while adw.Process_Status(1) == 1: #While the ADwin is already running, delay the process
        time.sleep(0.0001)

    dataList = adw.GetData_Long(1, 1, n_read) # Get the data collected from the ADwin Counter 1
    t2 = time.perf_counter()  # Elapsed time up to this point

    #Print Data
    print((len(dataList), ' points done.'))
    print(("It takes: ", t2 - t1, 'for ', n_read, " steps"))
    print(list(dataList))

    avg += 1
    print("Average ", avg, " is done")
    time.sleep(2)

#close ADwin and Arduino
adw.Clear_Process(1)
arduino.close()
rm.close()
awg.cleanup()
