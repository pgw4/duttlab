from PyQt5 import QtCore
from source.Hardware.AWG520 import AWG520
from source.Hardware.AWG520.AWG520 import AWGFile
from source.Hardware.AWG520.Sequence import Sequence,SequenceList
from source.Hardware.PTS3200.PTS import PTS
from source.Hardware.MCL.NanoDrive import MCL_NanoDrive
from source.common.utils import log_with, create_logger,get_project_root
import time,sys,multiprocessing
import logging
import ADwin,os
from pathlib import Path

_PTS_PORT = 'COM3'
sourcedir = get_project_root()
dirPath = Path(sourcedir / 'Hardware/AWG520/sequencefiles/')
awgPath = Path('./pulsed_esr')

_GHZ = 1000000000
_MHZ = 1000000

class UploadThread(QtCore.QThread):
    """this is the upload thread to send all the files to the AWG. it has following variables:
    1. seq = the sequence list of strings
    2. scan = scan parameters dictionary
    3. params = misc. params list such as count time etc
    4. awgparams = awg params dict
    5. pulseparams = pulseparams dict
    6. mwparams = mw params dict
    7. timeRes = awg clock rate in ns

    This class emits one Pyqtsignal which is emitted once the upload is finished
    1. done  - when the upload is finished
    """

    done = QtCore.pyqtSignal()
    def __init__(self, parent=None, dirPath=dirPath, awgPath=awgPath):
        #super().__init__(self)
        QtCore.QThread.__init__(self, parent)

        self.dirPath = dirPath
        self.awgPath =awgPath

    def run(self):
        samples = self.parameters[0]
        delay = self.parameters[-2:]

        self.sequences = SequenceList(sequence=self.seq, delay=delay, pulseparams = self.pulseparams, scanparams = self.scan, timeres=self.timeRes)
        self.awgfile = AWGFile(ftype='SEQ', timeres = self.timeRes)
        self.awgfile.write_sequence(sequences=self.sequences, seqfilename="scan.seq", repeat= samples)

        try:
            if self.awgparams['awg device'] == 'awg520':
                self.awgcomm = AWG520()
                t = time.process_time()
                for filename in os.listdir(self.dirPath):
                    self.awgcomm.sendfile(self.awgPath / filename, self.dirPath / filename)
                transfer_time = time.process_time() - t
                time.sleep(1)
                self.logger.info('time elapsed for all files to be transferred is:{0:.3f} seconds'.format(transfer_time))
                self.awgcomm.cleanup()
                self.done.emit()
            else:
                raise ValueError('AWG520 is the only AWG supported')
        except ValueError as err:
            self.logger.error('Value Error {0}'.format(err))
        except RuntimeError as err:
            self.logger.error('Run time error {0}'.format(err))


class ScanThread(QtCore.QThread):
    """this is the Scan thread. it has following variables:
        1. seq = the sequence list of strings
        2. scan = scan parameters dictionary
        3. params = misc. params list such as count time etc
        4. awgparams = awg params dict
        5. pulseparams = pulseparams dict
        6. mwparams = mw params dict
        7. timeRes = awg clock rate in ns
        8. maxcounts = observed max. counts

        This has 2 pyqtsignals
        1. data = a tuple of 2 integers which contain sig and ref counts
        2. tracking - integer with tracking counts
        """

    data = QtCore.pyqtSignal(int, int)
    tracking = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, timeRes = 1, maxcounts=100):
        #QtCore.QThread.__init__(self,parent)
        super().__init__(parent)

        self.timeRes = timeRes
        self.maxcounts = maxcounts
  
    def run(self):
        self.scanning = True
        self.proc_running = True

        self.p_conn, self.c_conn = multiprocessing.Pipe() # create parent and child connectors
     
        self.proc = ScanProcess()
        self.proc.get_conn(self.c_conn)

        # pass the variables to ScanProcess()
        self.proc.parameters = self.parameters
        self.proc.mw = self.mw
        self.proc.scan = self.scan
        self.proc.awgparams = self.awgparams
        self.proc.maxcounts = self.maxcounts
        self.proc.start()

        while self.scanning:
            threshold = self.parameters[4]
            if self.p_conn.poll(1): # check if there is data
                reply = self.p_conn.recv() # get the data
                self.p_conn.send((threshold, self.scanning))
                # self.p_conn.send((threshold,self.proc_running))

                print(f"Scan thread is sending threshold {threshold} and scanning status {self.scanning}")

                if reply == 'Abort!':
                    self.scanning = False
                    break
                elif type(reply) is int: # if the reply is tracking counts, send that signal to main app
                    self.tracking.emit(reply)
                elif len(reply) == 2: # if the reply is a tuple with signal and ref,send that signal to main app
                    self.data.emit(reply[0], reply[1]) 

class ScanProcess(multiprocessing.Process):
    """This is where the scanning actually happens. It inherits nearly all the same params as the ScanThread, except for
    one more parameter: conn which is the child connector of the Pipe used to communicate to ScanThread."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def get_conn(self, conn):
        self.conn = conn
        self.scanning = False

    def initialize(self):
        count_time = self.parameters[1]
        reset_time = self.parameters[2]
        samples = self.parameters[0]

        use_pts = self.mw['PTS'][0]
        current_freq = float(self.mw['PTS'][1])
        do_enable_iq = self.awgparams['enable IQ']

        # ADWIN
        self.adw = ADwin.ADwin()
        try:
            self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')

            measure_proc = os.path.join(os.path.dirname(__file__), 'AdWIN', 'Measure_Protocol.TB2')
            self.adw.Load_Process(measure_proc)

            count_proc = os.path.join(os.path.dirname(__file__), 'ADWIN', 'TrialCounter.TB1')
            self.adw.Load_Process(count_proc)

            self.adw.Set_Par(3, count_time)
            self.adw.Set_Par(4, reset_time)
            self.adw.Set_Par(5, samples)

            # start the Measure protocol
            self.adw.Start_Process(2)

        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            self.conn.send('Abort!')
            self.scanning = False


        # PTS
        if use_pts:
            self.pts = PTS(_PTS_PORT)
            self.pts.write(int(current_freq * _MHZ))
        else:
            print('MW is off.')

        # AWG
        self.awgcomm = AWG520()
        self.awgcomm.setup(enable_iq=do_enable_iq, seqfilename="./pulsed_esr/scan.seq")
        time.sleep(0.2)
        self.awgcomm.run()
        time.sleep(0.2)

    def run(self):
        self.scanning = True
        self.initialize() # why is initialize called in run? it would seem best to initialize hardware first

        numavgs = self.parameters[3]
        start = float(self.scan['start'])
        step = float(self.scan['stepsize'])
        numsteps = int(self.scan['steps'])

        use_pts = self.mw['PTS'][0]
        scan_carrier_freq = (self.scan['type'] == 'Carrier frequency')
        current_freq = float(self.mw['PTS'][1])

        try:
            for _ in list(range(numavgs)): # we will keep scanning for this many averages
                self.awgcomm.trigger() # trigger the awg for the arm sequence which turns on the laser.
                time.sleep(0.2)

                for x in list(range(numsteps)):
                    if not self.scanning:
                        raise Abort()

                    if use_pts and scan_carrier_freq: # this part implements frequency scanning
                        freq = int((start + step*x)*_MHZ)
                        temp=1
                        # try to communicate with PTS and make sure it has put out the right frequency
                        while not (self.pts.write(freq)):
                            time.sleep(temp)
                            temp *= 2
                            if temp>10:
                                self.pts.__init__()
                                temp=1

                    # get the signal and reference data
                    sig, ref = self.getData(x)
                    
                    threshold = self.parameters[4]
                    while ref < threshold:
                        threshold = self.parameters[4]
                        print(f"THRESHOLD IS: {threshold}")
                        if not self.scanning:
                            raise Abort()
                        if ref < 0: # this condition arises if the adwin did not update correctly
                            self.logger.debug('the ref is less than 0, probably adwin did not update')
                            raise Abort()
                        else:
                            # turning on the microwave for finetrack
                            self.awgcomm.sendcommand('SOUR1:MARK1:VOLT:LOW 2.0\n')
                            self.pts.write(int(2700 * _MHZ))
                            self.finetrack()
                            self.awgcomm.sendcommand('SOUR1:MARK1:VOLT:LOW 0\n')
                            time.sleep(0.1)
                            self.awgcomm.sendcommand('SOUR1:MARK1:VOLT:HIGH 2.0\n')
                            time.sleep(0.1)
                            self.pts.write(int(current_freq * _MHZ))

                            sig, ref = self.getData(x, 'jump') # we have to execute the sequence again.

                            if sig == 0:
                                sig, ref = self.getData(x,'jump')

                    self.conn.send([sig,ref])
                    # self.logger.info('signal {0:d} and reference {1:d} sent from ScanProc to ScanThread'.format(sig,ref))
                    self.conn.poll(None)
                    self.parameters[4], self.scanning = self.conn.recv() # receive the threshold and scanning status
        except Abort:
            self.conn.send('Abort!')
        self.cleanup()

    def getData(self, x, *args):
        '''This is the main function that gets the data from the Adwin.
        to understand the code, it helps to know that the AWGFile class that was used to upload the sequences first
        creates an arm_sequence which is the 1st line in the scan.seq file. The 2md line of the scan.seq file will
        therefore be the 1st point in the scan list and so on. The arm_sequence is executed during the
        finetrack function when the counts from NV are low. There are 3 possible ways getData function is called:
            getData(0) = 1st time getData is called it will jump to the 2nd line of the scan.seq file which
            corresponds to the first actual point in the scan. it will then trigger to output that wfm on the AWG
            getData(x) = not the 1st time, will direct trigger to output the current line of the scan.seq file and
            move to the next
            getData(x,'jump') = including the case x = 0, this is called when we finished tracking and maximizing
            counts using fine_track func. If we have taken x points of data and now want to move to the (x+1)th
            point, then the scan index is x (because python indexing starts at 0 for lists). So again when we come
            back from finetrack, we need to jump the (x+2) line of the scan.seq function and output that wfm by
            triggering. For some reason the trigger has to be done twice here according to Kai Zhang.
            Thus the params to be sent are:
            1. x : data point number
            2. args : only one arg 'jump' is supported at this time
        '''
        flag = self.adw.Get_Par(10)
        
        if x==0 or args!=(): # if this is the first point we need to jump over the arm_sequence to the 2nd line of
            # scan.seq. If not first point, we still need to add 2 again to get to the right line number
            self.awgcomm.jump(x+2)
            time.sleep(0.005)  # This delay is necessary. Otherwise neither jump nor trigger would be recognized by awg.

        self.awgcomm.trigger() # now we output the line number in the scan.seq file
        time.sleep(0.2)
        if args!=():
            time.sleep(0.1)
            self.awgcomm.trigger() # if the arg is 'jump' we have to trigger again for some reason.
        self.logger.info(f'Adwin Par_10 just before while is {self.adw.Get_Par(10):d}')
        # wait until data updates
        while flag==self.adw.Get_Par(10):
            time.sleep(0.1)
            self.logger.info(f'Adwin Par_10 within while is {self.adw.Get_Par(10):d}')

        sig = self.adw.Get_Par(1)
        ref = self.adw.Get_Par(2)

        return sig, ref

    def track(self):
        self.axis = 'z'
        position = self.nd.SingleReadN(self.axis, self.handle)
    
    def finetrack(self):
        modlogger.info('entering tracking from ScanProc')
        self.adw.Stop_Process(2)  # Stop the ADWin measure process
        
        self.awgcomm.jump(1)  # Jumping to line 1 which turns the green light on (arm sequence)
        time.sleep(0.005)  # This delay is necessary. Otherwise neither jump nor trigger would be recognized by awg.
        self.awgcomm.trigger()
        try:
            self.nd = MCL_NanoDrive()
            self.handle = self.nd.InitHandles().get('L')
        except IOError as err:
            self.logger.error("Error initializing NanoDrive {0}".format(err))
            raise
        self.accuracy = 0.025
        self.axis = 'x'
        self.scan_track()  # Readjust the x axis
        self.axis = 'y'
        self.scan_track()  # Readjust the y axis
        self.axis = 'z'
        self.scan_track(ran=0.5)  # Increase range for z
        self.nd.ReleaseAllHandles()
        
        self.adw.Start_Process(2)  # Restart the ADWin measure process
        time.sleep(0.3)
        
    def go(self, command):
        # we need to check if the position has really gone to the command position
        position = self.nd.SingleReadN(self.axis, self.handle)
        i = 0
        while abs(position - command) > self.accuracy:
            print(f'{self.axis} moving to {command} from {position}')
            position=self.nd.MonitorN(command, self.axis, self.handle)
            time.sleep(0.1)
            i += 1
            if i == 20:
                break

    def count(self):
        # this function uses the Adwin process 1 to simply record the counts
        self.adw.Start_Process(1)
        time.sleep(1.01) # feels like an excessive delay, check by decreasing if it can be made smaller
        counts=self.adw.Get_Par(1)
        print(f'counts collected from the count method is {counts}')
        self.adw.Stop_Process(1)
        return counts
    
    def scan_track(self, ran=0.25, step=0.05):
        '''This is the function that maximizes the counts by scanning a small range around the current position.
        Params are
         1. ran : range to scan in microns ie 250 nm is default
         2. step = step size in microns, 50 nm is default'''

        positionList = []
        position = self.nd.SingleReadN(self.axis, self.handle)
        counts_data = []
        p = position-ran/2
        while p <= position + ran/2:
            positionList.append(p)
            p += step
        for each_position in positionList:
            self.go(each_position)
            data = self.count()
            self.conn.send(data)
            print(f'data collected from the scan_track method is {data}')
            self.conn.poll(None)
            r = self.conn.recv()
            self.parameters[4] = r[0]
            counts_data.append(data)
        
        self.go(positionList[counts_data.index(max(counts_data))])
        
    def cleanup(self):
        self.awgcomm.stop()
        self.awgcomm.cleanup()
        self.adw.Stop_Process(2)
        #self.amp.switch(False)
        self.pts.cleanup()


class KeepThread(QtCore.QThread):
    """This thread should be run automatically after the scan thread is done, so as to keep the NV in focus even when the user
    is not scanning. It works on a very similar basis as the scan thread. It has one signal:
        1. status = string which updates the main app with the counts"""

    status=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.running=False
        self.logger = logging.getLogger('threadlogger.KeepThread')


    def run(self):
        self.running=True
        # create the keep process in a separate process and pass it a child connector
        self.p_conn,self.c_conn=multiprocessing.Pipe()
        self.proc = KeepProcess()
        self.proc.get_conn(self.c_conn)
        self.proc.start() # start the keep process
        while self.running:
            self.logger.info('keep process still running')
            if self.p_conn.poll(1):
                reply=self.p_conn.recv()
                if reply=='t': # if the reply from Keep process is t, then it is tracking
                    self.status.emit('Tracking...')
                    self.logger.debug('signal emitted by KeepThread is Tracking..')
                elif reply[0]=='c': # if the reply starts with c, then we can get the counts
                    self.status.emit('Monitoring counts...'+reply[1:])
                    self.logger.debug('signal emitted by KeepThread is Monitoring counts...{0}'.format(reply[1:]))
        #self.logger.info('keep thread stopping')
        self.p_conn.send(False)
        while self.proc.is_alive():
            self.logger.info('keep proc still alive {0}'.format(id(self.proc.running)))
            time.sleep(1)
        self.status.emit('Ready!') # we finished the keep process and can now go back to main program
        
class KeepProcess(multiprocessing.Process):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger('threadlogger.keepproc')

        self.accuracy = 0.025 # accuracy for moves of nanostage is 25 nm
        self.count_threshold_percent = 0.7
        self.running = False

    def get_conn(self, conn):
        self.conn = conn


    # def __init__(self,parent=None,conn=None):
    #     super().__init__(parent)
    #     self.conn = conn
    #     self.running = False
    #     self.logger = logging.getLogger('threadlogger.KeepThread.keepproc')
    #     self.initialize()
    #     self.accuracy = 0.025 # accuracy for moves of nanostage is 25 nm
    #     self.count_threshold_percent = 0.7

    def run(self):
        self.logger.info('keep process starts')
        self.initialize()
        self.running=True
        time.sleep(5) # wait 5 seconds before counting again
        
        maxcount=self.count()
        self.conn.send('c'+str(maxcount))
        time.sleep(5) # wait 5 seconds before counting again
        
        
        while not self.conn.poll(0.01):
            # self.logger.info('keep process did not receive anything.')
            c=self.count()
            if float(c)/maxcount<self.count_threshold_percent: # if the counts fall below threshold
                self.conn.send('t') # tell Keep thread that we are now tracking
                self.track()
                maxcount=self.count()
                self.conn.send('c'+str(maxcount))
            time.sleep(5)
        
        self.cleanup()
        
    def initialize(self):
        self.nd=MCL_NanoDrive()
        self.adw=ADwin.ADwin()
        self.awgcomm = AWG520()

        # try:
        #     self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')
        #     count_proc = os.path.join(os.path.dirname(__file__),'ADWIN\\TrialCounter.TB1') # TrialCounter is configured as process 1
        #     self.adw.Load_Process(count_proc)
        # except ADwin.ADwinError as e:
        #     sys.stderr.write(e.errorText)
        #     self.conn.send('Abort!')
        #     self.running=False

        try:
            # boot the adwin with the bootloader
            self.adw.Boot(self.adw.ADwindir + 'ADwin11.btl')
            # Measurement protocol is configured as process 2, external triggered
            count_proc = os.path.join(os.path.dirname(__file__),'ADWIN\\TrialCounter.TB1') # TrialCounter is configured as process 1
            self.adw.Load_Process(count_proc)

        except ADwin.ADwinError as e:
            sys.stderr.write(e.errorText)
            self.conn.send('Abort!')
            self.scanning = False
            
    def track(self):
        self.logger.info('entered track function')
        
        self.handle=self.nd.InitHandles().get('L')
        # track each axis one by one
        self.axis='x'
        self.scan_track()
        self.axis='y'
        self.scan_track()
        self.axis='z'
        self.scan_track()
        
        
    def go(self,command):
        ''' this function moves nanostage to the position given by param:
        1. command'''
        position = self.nd.SingleReadN(self.axis, self.handle)
        while abs(position-command)>self.accuracy:
            #print 'moving to',command,'from',position
            position=self.nd.MonitorN(command, self.axis, self.handle)
            time.sleep(0.1)

    def count(self):
        '''this function uses the Adwin process 1 to simply record the counts '''
        self.awgcomm.green_on()
        self.adw.Start_Process(1)
        time.sleep(1.01) # very long delay, check if truly needed
        counts=self.adw.Get_Par(1)
        self.adw.Stop_Process(1)
        self.awgcomm.green_off()
        return counts
    
    def scan_track(self,ran=0.5,step=0.05):
        '''This is the function that maximizes the counts by scanning a small range around the current position.
        Params are
         1. ran : range to scan in microns ie 500 nm is default
         2. step = step size in microns, 50 nm is default'''
        positionList=[]
        position = self.nd.SingleReadN(self.axis, self.handle)
        counts_data=[]
        p=position-ran/2
        while p<=position+ran/2:
            positionList.append(p)
            p+=step
        for each_position in positionList:
            self.go(each_position)
            data=self.count()
            
            counts_data.append(data)
        
        self.go(positionList[counts_data.index(max(counts_data))])
        
    def cleanup(self):
        self.nd.ReleaseAllHandles()
        self.awgcomm.cleanup()

class Abort(Exception):
    pass

