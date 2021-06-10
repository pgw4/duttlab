# Created on 2/1/20 by gurudev
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from source.Hardware.AWG520.Sequence import Sequence,SequenceList

#import pytest

print('Module name is: ',__name__)
def make_seq():
    wfmdir = Path('../../..') / 'arbpulseshape'
    #print(str(wfmdir.resolve()))
    # seq=[['Green', '0', '800'],['S2','900','1700'],['Wave','900','1400','Sech'],['Wave','1400','1800','Gauss'],
    #       ['Wave','1800','2200','Square'],['Wave','2200','2600','Lorentz'],['Wave','2600','3000','Load Wfm', \
    #         wfmdir / 'test4.txt']]
    seq = [['Wave','1000','1500','SquareI'],['Wave','1800','2100','SquareI']]
    #seq = [['Green', '0', '1000']]
    #seq = [['Wave', '900', '1400', 'Load Wfm',wfmdir/'test4.txt'],['Green', '1500', '2500']]
    # seq = [['Wave', '900+t', '1400+t', 'Gauss'], ['Green', '1500', '2500'],['S2','500','1500'],['S2','2000','2500'],
    #        ['Green', '3000', '3200'],['Measure','1500','1800']]
    # seq = [['S2', '1000', '1200'],['Green', '1100', '1700'],['S2','1800','2000']]
    newparams = {'amplitude': 100, 'pulsewidth': 50, 'SB freq': 0.00001, 'IQ scale factor': 1.0, 'phase': 0.0,
                 'skew phase':0.0, 'num pulses': 1}
    s = Sequence(seq,pulseparams=newparams,timeres=1)
    s.create_sequence(dt=10)
    tt = np.linspace(0,s.maxend,len(s.c1markerdata))
    # plt.plot(tt,s.c1m1,'r-',tt,s.c1m2,'g-')
    # plt.plot(tt,s.wavedata[0,:],'r-',tt,s.wavedata[1,:],'b-',tt,s.c1markerdata,'g--',tt,s.c2markerdata,'y-')
    plt.plot(tt,s.wavedata[0,:],'r--',tt,s.wavedata[1,:],'b--')
    #plt.plot(tt,s.wavedata[1,:])
    plt.show()
    #raise RuntimeError('test the runtime handling')

def make_seq_list():
    wfmdir = Path('../../..') / 'arbpulseshape'
    # print(str(wfmdir.resolve()))
    # notice the sequence below scans time by setting all times after the pulse that is being scanned are also moved
    # seq = [['Green', '1600', '2500'],['Wave', '1000+t', '1500+t', 'Sech'],['Measure','1500+t','1800+t']]
    seq = [['S2', '1000', '1025'],['S2', '1030+t', '1050+t'],['Green','1050+t','4025+t'],['Measure','1025+t','1125+t']]
    # seq = [['Green', '0', '1000']]
    newparams = {'amplitude': 100, 'pulsewidth': 50, 'SB freq': 0.01, 'IQ scale factor': 1.0, 'phase': 0.0,
                 'skew phase': 0.0, 'num pulses': 1}
    newscanparams = {'type':'time','start': 0, 'stepsize': 100, 'steps': 3}
    s = SequenceList(seq, pulseparams=newparams, timeres=1,scanparams = newscanparams)
    s.create_sequence_list()
    for nn in list(range(len(s.sequencelist))):
        xstop = s.sequencelist[nn].maxend
        points = len(s.sequencelist[nn].c1markerdata)
        ydat = s.sequencelist[nn].wavedata
        c1dat = s.sequencelist[nn].c1markerdata
        c2dat = s.sequencelist[nn].c2markerdata
        tt = np.linspace(0, xstop, points)
        plt.plot(tt, ydat[0, :], 'r-', tt, ydat[1, :], 'b-', tt, c1dat, 'g--',tt,c2dat,'+')
        plt.show()
    # plt.plot(tt,s.wavedata[1,:])

    # raise RuntimeError('test the runtime handling')

def make_long_seq():
    seq = [['S2','1000','1050'],['Green','100000','102000'],['Measure','100100','100400']]
    newparams = {'amplitude': 100, 'pulsewidth': 50, 'SB freq': 0.01, 'IQ scale factor': 1.0, 'phase': 0.0,
                 'skew phase': 0.0, 'num pulses': 1}
    s = Sequence(seq, pulseparams=newparams, timeres=1)
    s.create_sequence(dt=0)
    tt = np.linspace(0, s.maxend, len(s.c1markerdata))
    plt.plot(tt, s.wavedata[0, :], 'r-', tt, s.wavedata[1, :], 'b-', tt, s.c1markerdata, 'g--', tt, s.c2markerdata,
             'y-')
    # plt.plot(tt,s.wavedata[1,:])
    plt.show()
    # raise RuntimeError('test the runtime handling')

def test_sequence():
    make_seq()

def test_seq_list():
    make_seq_list()

if __name__ == '__main__':
    test_sequence()
    # test_seq_list()
    #make_long_seq()