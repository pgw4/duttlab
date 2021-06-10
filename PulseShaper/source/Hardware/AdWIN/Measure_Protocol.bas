'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 2
' Initial_Processdelay           = 3000
' Eventsource                    = External
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 6.3.0
' Optimize                       = Yes
' Optimize_Level                 = 1
' Stacksize                      = 1000
' Info_Last_Save                 = DUTTLAB8  Duttlab8\Duttlab
'<Header End>
' MeasureProtocol.bas
' Configured as Process 2, Priority High, External trigger.


#Include ADwinGoldII.inc
DIM s,r,i AS LONG
DIM count_time, reset_time as LONG


init:
  Cnt_Enable(0)
  Cnt_Mode(1,8)          ' Counter 1 set to increasing
  
  Cnt_Clear(1)           ' Clear counter 1
  i=0
  s=0
  r=0
  Par_10=0

  count_time = (Par_3  -10)/10 'added on 2/6/20 to allow passing parameter from Python
  reset_time = (Par_4 - 30)/10  'added on 2/6/20 to allow passing parameter from Python


event:
  Inc(i)
  Cnt_Enable(1)          ' enable counter 1
  CPU_Sleep(count_time)          ' count time 300 ns
  Cnt_Enable(0)          ' disable counter 1
  Cnt_Latch(1)           ' Latch counter 1
  CPU_Sleep(reset_time)         ' reset time 2000 ns
  Cnt_Enable(1)          ' enable counter 1
  CPU_Sleep(count_time)          ' count time 300 ns
  Cnt_Enable(0)          ' disable counter 1
  s=s+Cnt_Read_Latch(1)  ' accumulate sig
  r=r+Cnt_Read(1)        ' accumulate sig+ref
  Cnt_Clear(1)           ' Clear counter 1
  

  IF (i>=Par_5) THEN
    Par_1=s
    Par_2=r-s
    s=0
    r=0
    i=0
    Inc(Par_10)
  ENDIF


finish:
  Cnt_Enable(0)
