import re
import subprocess
import socket

def ipaddress():
  p = subprocess.Popen(["/sbin/ip","addr","show"], stdout=subprocess.PIPE)
  ip=p.communicate()
  pattern = re.compile(r'inet\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  return pattern.findall(ip[0])

def private_ip():
  ips=[]
  p=subprocess.Popen(["/sbin/ip","addr","show"],stdout=subprocess.PIPE)
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
  if len(ips) > 0:
      return ', '.join(ips)
  else:
     p=subprocess.Popen(["curl","http://169.254.169.254/latest/meta-data/public-ipv4"],stdout=subprocess.PIPE).communicate()[0]
     if p != "not found":
         return p
     else:
         return ""

def os_name():
  return subprocess.Popen(["uname"], stdout=subprocess.PIPE).communicate()[0]

def memory():
  mem = int(subprocess.Popen(["grep","MemTotal","/proc/meminfo"], stdout=subprocess.PIPE).communicate()[0].split()[1:2][0])/1024
  return str(mem) + "MB"

def cpu():
  return subprocess.Popen(["grep","-m1", "name","/proc/cpuinfo"], stdout=subprocess.PIPE).communicate()[0].split(':')[-1]

def serial_number():
    try:
        sys_info = subprocess.Popen('dmidecode -t system'.split(), stdout=subprocess.PIPE)
        uid = subprocess.Popen('grep UUID'.split(), stdin=sys_info.stdout, stdout=subprocess.PIPE)
        return uid.communicate()[0].split(':')[-1].strip().strip('\n')
    except:
        return "Uid_Not_Avail"

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
    try:
        sys_info = subprocess.Popen('dmidecode -t system'.split(), stdout=subprocess.PIPE)
        model = subprocess.Popen('grep Product'.split(), stdin=sys_info.stdout, stdout=subprocess.PIPE)
        return  model.communicate()[0].split(':')[-1].strip().strip('\n')
    except:
        return "N/A"

def child_ip():
    return "N/A"

def fqdn():
  return socket.gethostname()

def swap():
  return subprocess.Popen(["grep","SwapTotal","/proc/meminfo"], stdout=subprocess.PIPE).communicate()[0].split()[1:]

def cpu_cores():
  return subprocess.Popen(["grep","-m1","cores","/proc/cpuinfo"], stdout=subprocess.PIPE).communicate()[0].split()[-1]

def cpu_threads():
  return subprocess.Popen(["grep","-c","processor","/proc/cpuinfo"], stdout=subprocess.PIPE).communicate()[0].split()[-1]
