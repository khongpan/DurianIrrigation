import datetime as dt
import numpy as np
from scipy import interpolate


def m_avg(a,n) :
  pad_size = n//2
  a_len = len(a)
  a = np.pad(a,pad_size,mode='linear_ramp',end_values=(a[0],a[-1]))
  a = np.insert(a,0,0)
  cumsum = np.cumsum(a)
  m_a = (cumsum[n:n+a_len]-cumsum[0:a_len])/float(n)
  return m_a

def Time2Sampling(time_str) :
    s_time_dt = dt.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    sampling_number = s_time_dt.hour*12+int(s_time_dt.minute/5)
    return sampling_number

def TimeStrToSecOfDay(time_str, mode='') :
  time_dt = dt.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
  s_of_day = time_dt.hour*60*60+time_dt.minute*60
  return s_of_day

def ReSamplingDailyData(time_str_s, value_s, period_in_sec) :
  point_num = len(value_s)
  if point_num==(24*60*60/period_in_sec) :
    return value_s
  if (point_num<=2) :
    print("data less than 2 points")
  
  x_s = [TimeStrToSecOfDay(time_str) for time_str in time_str_s]
  y_s = value_s
  f = interpolate.interp1d(x_s, y_s,fill_value= 'extrapolate')
  xnew_s = np.arange(0,24*60*60, period_in_sec)
  ynew_np = f(xnew_s)

  return ynew_np.tolist()
