import numpy as np

def CalcSatVapourPressureSlope(t) :
  k=t+237.3
  delta= 4096*(0.61078*np.exp(17.27*t/k))/k**2
  return delta

def CalcSatVapourPressure(t) :
  svp=0.61078*np.exp(t/(t+238.3)*17.2694)
  return svp

def CalcActualVapourPressure(svp,h) :
  avp= svp*h/100
  return avp

def CalcVPD(t,rh):
  svp=0.61078*np.exp(t/(t+238.3)*17.2694)
  vpd = svp * (1-rh/100)
  return vpd
 
def CalcWind2m(w) :
  w2m = w*1000./3600.
  #print(w2m)
  return w2m

def CalcNetRadiation(i) :
  return i*5.*60./1000000.

def CalcPsychrometricConstant(p) :
  gamma=p*0.665*10**-3
  #print(gamma)
  return gamma

def CalcETo(t,rh,p,i,w) :
  svp_slope= CalcSatVapourPressureSlope(t)
  net_rad = CalcNetRadiation(i)
  wind_speed = CalcWind2m(w)
  psy_const = CalcPsychrometricConstant(p)
  vpd = CalcVPD(t,rh)
  eto=(0.408*svp_slope*net_rad+psy_const*(900.0/(288)/(t+273))*wind_speed*vpd)/(svp_slope+psy_const*(1+0.34*wind_speed))
  return eto
