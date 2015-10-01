import re
import subprocess
import socket

def ipaddress():
  p=subprocess.Popen(["/sbin/ifconfig"],stdout=subprocess.PIPE)
  ip=p.communicate()
  pattern=re.compile(r'inet\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  return pattern.findall(ip[0])

def private_ip():
  ips=[]
  p=subprocess.Popen(["/sbin/ifconfig"],stdout=subprocess.PIPE)
  ip=p.communicate()
  pattern=re.compile(r'inet\s*(192\.168\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0]))
  pattern=re.compile(r'inet\s*(10\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0]))
  pattern=re.compile(r'inet\s*(127\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0]))
  pattern=re.compile(r'inet\s*(172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3})')
  for ip_data in pattern.findall(ip[0]):
    ips.append(ip_data[0])
  return ips

def ip():
  ips = list(set(ipaddress())-set(private_ip()))
  return ', '.join(ips)

def profiler_hardware_datatype():
  data = filter(None, subprocess.Popen(["/usr/sbin/system_profiler","SPHardwareDataType"], stdout=subprocess.PIPE).communicate()[0].split('\n'))
  data_dict = {}
  for d in data[2:]:
    data_dict[ d.split(':')[0].strip() ] = d.split(':')[1].strip()
  return data_dict

def memory():
  return profiler_hardware_datatype()['Memory']

def os_name():
  return subprocess.Popen(["sw_vers"], stdout=subprocess.PIPE).communicate()[0].split('\n')[0].split('\t')[1]

def cpu():
  return profiler_hardware_datatype()['Processor Name']

def cpu_cores():
  try:
    return profiler_hardware_datatype()['Total Number of Cores']
  except:
    return profiler_hardware_datatype()['Total Number Of Cores']

def serial_number():
  return profiler_hardware_datatype()['Serial Number (system)']

def disk():
    p = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE).communicate()[0].split('\n')
    data_dict = {}
    for mount in p[1:]:
        if len(mount) > 1:
            if mount.split()[0] == "map":
                data_dict[mount.split()[-1]] = mount.split()[2]
            else:
                data_dict[mount.split()[-1]] = mount.split()[1]
    return ', '.join('{0} {1}'.format(key, val) for key, val in sorted(data_dict.items()))

def model():
    return profiler_hardware_datatype()['Model Name']

def child_ip():
    return "N/A"

def fqdn():
  return socket.gethostname()

def processor_speed():
  return profiler_hardware_datatype()['Processor Speed']

def cpu_type():
  return profiler_hardware_datatype()['Processor Name']
