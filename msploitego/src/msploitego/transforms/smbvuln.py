#!/usr/bin/env python

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from pprint import pprint

from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'
# nmap -vv -p 139,445 --script=$(ls /usr/share/nmap/scripts/smb-vuln* | cut -d"/" -f6 | tr '\n' ',' | sed 's/.$//') --script-args=unsafe=1

scripts = "smb-vuln-conficker,smb-vuln-cve-2017-7494,smb-vuln-cve2009-3103,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067,smb-vuln-ms10-054,smb-vuln-ms10-061,smb-vuln-ms17-010,smb-vuln-regsvc-dos,smb2-vuln-uptime"

def mycallback(nmaptask):
    nmaptask = nmap_proc.current_task
    if nmaptask:
        print "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                              nmaptask.status,
                                                              nmaptask.etc,
                                                              nmaptask.progress)

args = ['smbvuln.py',
 'netbios-ns/137:253',
 'properties.metasploitservice=netbios-ns/137:253#name=netbios-ns#proto=tcp#hostid=253#service.name=80/Apache 9#port=137#banner=Apache 9#properties.service= #ip=10.10.10.80#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#state=filtered']

mt = MaltegoTransform()
# mt.debug(pprint(sys.argv))
mt.parseArguments(args)
# mt.parseArguments(sys.argv)
ip = mt.getVar("ip")
port = mt.getVar("port.number")
# options="-vvvv -p {} -sS --script {}".format(port,scripts),
nmap_proc = NmapProcess(targets=ip,
                         options="-vvvvv --script=smb-vuln-conficker",
                         event_callback=mycallback,
                        safe_mode=False)
nmap_proc.run()
rep = NmapParser.parse(nmap_proc.stdout)
for host in rep.hosts:
    pprint(host)
print "running"