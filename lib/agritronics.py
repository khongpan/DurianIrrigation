import requests
import xml.etree.ElementTree as etree
from datetime import datetime


def test():
    print('Agritronics...')

    
def GetLastData(network_id,node_id,io_number):
  script_path = '/ws/get.php?' 
  time=''
  url = 'http://'+server+script_path+'appkey='+appkey+'&p='\
                 + network_id+','+node_id+','+io_number
  print(url)
  page = requests.get(url)
  root = etree.fromstring(page.content)
  io=root.find('IO')
  if io is None :
    return time

  time=io.find('LastIODateTime').text    
  value=io.find('LastValue').text
  
  return time,value

def GetDailyData(network_id,node_id,io_number,date):
  server = 'agritronics.nstda.or.th'
  appkey = '0c5a295bd8c07a080d5306'
  script_path = '/ws/get.php?'
  times=[]
  values=[]
  url = 'http://'+server+script_path+'appkey='+appkey+'&p='\
                 + network_id+','+node_id+','+io_number+','+date
  print(url)
  page = requests.get(url)
  root = etree.fromstring(page.content)
  io=root.find('IO')
  if io is None :
    return times,values
  for d in io.findall('Data'):
     t=d.find('IODateTime').text
     v=float(d.find('Value').text)
     times.append(t)
     values.append(v)
  return times,values

  #4010,A,20/12/04,14:05:00,7,100,0.0
def PrepareDataForUpload(time_s,value_s) :
  node_id='4010'
  log_type='A'
  io_number='100'
  data_str=''
  i=0
  for ts_str in time_s :
    ts_dt = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
    date_str=ts_dt.strftime('%y/%m/%d')
    time_str=ts_dt.strftime('%H:%M:%S')
    line_str = F"{node_id},{log_type},{date_str},{time_str},7,{io_number},{value_s[i]}\n" 
    #print(line_str)
    data_str=F"{data_str}{line_str}"
    i=i+1

  return data_str



def PrepareDataForUpload(node_id,io_number,time_s,*n) :
  log_type='A'
  data_str=''
  i=0
  for ts_str in time_s :
    ts_dt = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
    date_str=ts_dt.strftime('%y/%m/%d')
    time_str=ts_dt.strftime('%H:%M:%S')
    line_str = F"{node_id},{log_type},{date_str},{time_str},7,{io_number}"
    for value_s in n :
      line_str+=F",{value_s[i]}" 
    line_str+="\n"
    #print(line_str)
    data_str=F"{data_str}{line_str}"
    i=i+1

  return data_str



#curl -F uploadedfile=@data.txt -F network=DURIAN-01 http://agritronics.nstda.or.th/webpost0606/log_webpost.php
def UploadData(network_id,data_str):
  url= 'http://agritronics.nstda.or.th/webpost0606/log_webpost.php'

  files={
        'uploadedfile': ('data.txt', data_str),
  }
  data={
        'network' : (network_id)
  }
   
  res = requests.post(url,files=files,data=data)
  #print(res.request.headers)
  #print(res.request.body)
  print(res.text)
  return

def UploadPicture(network_id,node_id,io_number,time_stamp,file) :
  url='http://agritronics.nstda.or.th/webpost0606/log_imgcap.php'
  
  ts_str=time_stamp.strftime('%Y%m%d%H%M%S')
  
  file_name = F"{ts_str}__{network_id}__{node_id}__{io_number}.jpg"
  print(file_name)
  files={
      'uploadedfile':(file_name, file)
  }
  data={
      'network' : (network_id),
      'filedatetime' : (ts_str)
  }
  
  #res = requests.post(url,files=files,data=data)
  #print(res.request.headers)
  #print(res.request.body)
  #print(res.text)

  return
