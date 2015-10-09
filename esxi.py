import subprocess
import re

def profile():
     p = subprocess.Popen(["esxcli", "hardware", "platform", "get"], stdout=subprocess.PIPE).communicate()[0].split('\n')
     data_dict = {}
     for d in p[0:]:
         data_dict[d.split(':')[0].strip()] = d.split(':')[-1].strip()
     return data_dict

def ipaddress():
  p = subprocess.Popen(["esxcli","network","ip","interface","ipv4","get"], stdout=subprocess.PIPE)
  ip = p.communicate()
  pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  return pattern.findall(ip[0])[::3]

def private_ip():
  ips=[]
  p = subprocess.Popen(["esxcli","network","ip","interface","ipv4","get"], stdout=subprocess.PIPE)
  ip=p.communicate()
  pattern=re.compile(r'(192\.168\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0])[::3])
  pattern=re.compile(r'(10\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0])[::3])
  pattern=re.compile(r'(127\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  ips.extend(pattern.findall(ip[0])[::3])
  pattern=re.compile(r'(172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3})')
  for ip_data in pattern.findall(ip[0][::3]):
    ips.append(ip_data[0])
  return ips

def testip():
    p = subprocess.Popen(["esxcli","network","ip","interface","ipv4","get"], stdout=subprocess.PIPE)
    ip = p.communicate()
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    return ', '.join(pattern.findall(ip[0])[::3])

def ip():
  ips = list(set(ipaddress())-set(private_ip()))
  return ', '.join(ips)

def memory():
    p = subprocess.Popen(["esxcli","hardware","memory","get"], stdout=subprocess.PIPE)
    mem = int(p.communicate()[0].split()[2])/1024/1024/1024
    return str(mem) + "GB"

def processor_speed():
    p = subprocess.Popen(["vim-cmd","hostsvc/hosthardware"], stdout=subprocess.PIPE)
    cpu = p.communicate()
    pattern = re.compile(r'hz = (\d{10}),')
    return pattern.findall(cpu[0])[0]

def cpu_cores():
    p = subprocess.Popen(["vim-cmd","hostsvc/hosthardware"], stdout=subprocess.PIPE)
    cpu = p.communicate()
    pattern = re.compile(r'numCpuCores = (\d+)')
    return int(pattern.findall(cpu[0])[0])

def cpu():
    p = subprocess.Popen(["vim-cmd","hostsvc/hosthardware"], stdout=subprocess.PIPE)
    cpu = p.communicate()
    pattern = re.compile(r'description = "([^"]+)')
    return pattern.findall(cpu[0])[0]

def cpu_threads():
    p = subprocess.Popen(["vim-cmd","hostsvc/hosthardware"], stdout=subprocess.PIPE)
    cpu = p.communicate()
    pattern = re.compile(r'numCpuThreads = (\d+)')
    return int(pattern.findall(cpu[0])[0])


def serial_number():
     return profile()['Serial Number']

def model():
     return profile()['Product Name']

def os_name():
    p = subprocess.Popen(["esxcli", "system", "version", "get"], stdout=subprocess.PIPE).communicate()[0].split('\n')
    data_dict = {}
    for d in p[0:]:
        data_dict[d.split(':')[0].strip()] = d.split(':')[-1].strip()
    return data_dict['Product'] + ' ' + data_dict['Build'] + ' ' + data_dict['Version']

def disk():
    p = subprocess.Popen(["esxcli", "storage", "filesystem", "list"], stdout=subprocess.PIPE).communicate()[0].split('\n')
    data_dict = {}
    for mount in p[2:]:
        if len(mount) > 1:
            data_dict[mount.split()[0]] = mount.split()[5]
    return ', '.join('{0} {1}'.format(key, val) for key, val in sorted(data_dict.items()))

def child_ip():
    p=subprocess.Popen(['vim-cmd', 'vmsvc/getallvms'], stdout=subprocess.PIPE).communicate()
    data=p[0].split('\n')
    vm = {}
    try:
      for allvms in data[1:]:
          if len(allvms) > 1:
              allvms = allvms.split()
              vm[allvms[0]] = [allvms[1]]
    except:
        pass
    for vm_id in vm:
      p = subprocess.Popen(['vim-cmd', '/vmsvc/get.summary', vm_id], stdout=subprocess.PIPE).communicate()
      data = p[0].split()
      offset = data.index('ipAddress')
      val = data[offset+2][1:-2]
      if val == "169.254.80.80":
        p=subprocess.Popen(['vim-cmd', '/vmsvc/get.guest', vm_id], stdout=subprocess.PIPE).communicate()
        data1 = p[0].split()
        offset = [n for (n, e) in enumerate(data1) if e == 'ipAddress'][10]
        vm[vm_id].append(data1[offset+2][1:-2])
      elif val == 'unset':
        vm[vm_id].append(val)
      else:
        vm[vm_id].append(data[offset+2][1:-2])
    child_ip_os = ""
    for key, val in vm.items():
        child_ip_os = child_ip_os + ' '.join(val) + "<br>"
    return child_ip_os
