#!/usr/bin/env python

"""
TorTP is a simple way to implement Tor Transparent Proxy in your GNU/Linux Box
TorTP use Tor stem library for setup Transparen Proxy and DNS server capabilities on Tor
"""

import subprocess
import os
import stem
from stem.control import Controller
from stem.version import get_system_tor_version
from stem.util import system
import stem.process
from shutil import copy2
import sys
import urllib
import re
from pwd import getpwnam, getpwuid

TOR_USER = os.environ.get('TOR_USER', 'debian-tor')

def notify(title, message):
    """
    Notification system
    """
    print("[%s]: %s" % (title, message))
    return

def check_user():
   """
   Only root can do that!
   """
   uid = os.getuid()
   if uid == 0:
      return os.environ.get('SUDO_UID', 0)
   else:
      notify("TorTP", "[!] Only root can do that!")
      sys.exit(1)

def get_home(user):
   """
   Get user home path
   """
   return getpwuid(int(user))[5]

def tortp_dir(home):
   """
   Create directory /home/$user/.tortp
   """
   tortpdir = "%s/.tortp" % home
   if not os.path.exists(tortpdir):
      os.makedirs(tortpdir)
      notify("TorTP", "[+] Directory %s created" % tortpdir)
   return tortpdir

def check_sys_dependencies():
   """
   Check if all dependencies are installed
   """
   devnull = open(os.devnull,"w")
   tor = subprocess.call(["which","tor"],stdout=devnull,stderr=subprocess.STDOUT)
   if tor != 0:
      notify("TorTP", "[!] Tor is not installed")
      sys.exit(1)
   devnull.close()


def iptables_clean():
   """
   This function remove all iptables rules
   """
   subprocess.call(['iptables', '-F'])
   subprocess.call(['iptables', '-X'])
   subprocess.call(['iptables', '-t', 'nat', '-F'])
   subprocess.call(['iptables', '-t', 'nat', '-X'])

def iptables_up(tortpdir, toruser):
   """
   This function make configuration backups and add iptables rules in order to redirect all network traffic through TorTP.
   Only except for Tor user.
   """
   ipt = open("%s/iptables.txt" % tortpdir, "w")
   subprocess.call(['iptables-save'], stdout=ipt)
   ipt.close()
   # Redirect DNSTor port (9053)
   subprocess.call(['iptables', '-t', 'nat', '-A', 'OUTPUT', '-p', 'udp', '-m', 'udp', '--dport', '53', '-j', 'REDIRECT', '--to-ports', '9053'])
   # Redirect to Transparent Proxy Tor (9040)
   subprocess.call(['iptables', '-t', 'nat', '-A', 'OUTPUT', '!', '-o', 'lo', '-p', 'tcp', '-m', 'owner', '!', '--uid-owner', '%s' % toruser, '-m', 'tcp', '-j', 'REDIRECT', '--to-ports', '9040'])
   subprocess.call(['iptables', '-t', 'filter', '-A', 'OUTPUT', '-p', 'tcp', '-m', 'owner', '!', '--uid-owner', '%s' % toruser, '-m', 'tcp', '--dport', '9040', '-j', 'ACCEPT'])
   subprocess.call(['iptables', '-t', 'filter', '-A', 'OUTPUT', '!', '-o', 'lo', '-m', 'owner', '!', '--uid-owner', '%s' % toruser, '-j', 'DROP'])
   subprocess.call(['iptables', '-t', 'nat', '-A', 'OUTPUT', '-p', 'tcp', '-m', 'owner', '!', '--uid-owner', '%s' % toruser, '-m', 'tcp', '--syn', '-d', '127.0.0.1', '--dport', '6969', '-j', 'ACCEPT'])

def iptables_down(tortpdir):
   """
   Restore original iptables rules
   """
   try:
      subprocess.call('iptables-restore < %s/iptables.txt' % tortpdir, shell=True)
      os.remove("%s/iptables.txt" % tortpdir)
   except IOError as e:
      iptables_clean()
      print e

def resolvconf(tortpdir):
   """
   Backup and modify resolv configuration file
   """
   try:
      copy2("/etc/resolv.conf",tortpdir)
   except IOError as e:
      print e
   resolv = open('/etc/resolv.conf', 'w')
   resolv.write('nameserver 127.0.0.1\n')
   resolv.close()


def myip():
   """
   Get my IP from check.torproject.org
   """
   url = "http://check.torproject.org"
   request = urllib.urlopen(url).read()
   myip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)
   return myip[0]

def check_tortp(myip, exit):
   """
   Check if my IP is a Tor exit node
   """
   if myip in exit['ipaddress']:
      notify("TorTP", "[+] Congratulations. TorTP is working: %s" % myip)
   else:
      notify("TorTP", "[-] Sorry. TorTP is not working: %s" % myip)
      sys.exit(1)
   return myip

def get_exit(is_running):
   """
   Get list of exit node from stem
   """
   if is_running:
      try:
         with Controller.from_port(port = 6969) as controller:
            controller.authenticate()
            exit = {'count': [], 'fingerprint': [], 'nickname': [], 'ipaddress': []}
            count = -1
            for circ in controller.get_circuits():
               if circ.status != stem.CircStatus.BUILT:
                  continue
               exit_fp, exit_nickname = circ.path[-1]
               exit_desc = controller.get_network_status(exit_fp, None)
               exit_address = exit_desc.address if exit_desc else 'unknown'
               count += 1
               exit['count'].append(count)
               exit['fingerprint'].append(exit_fp)
               exit['nickname'].append(exit_nickname)
               exit['ipaddress'].append(exit_address)
         return exit
      except stem.SocketError as exc:
         notify("TorTP", "[!] Unable to connect to port 6969 (%s)" % exc)
         sys.exit(1)
   else:
      notify("TorTP", "[!] Tor is not running")
      sys.exit(0)


def exit_info(exit):
   """
   Print info about my exit node
   """
   torversion = get_system_tor_version()
   print "Tor version: %s\n" % torversion
   for i in exit['count']:
      print "  nickname: %s" % exit['nickname'][i]
      print "  address: %s" % exit['ipaddress'][i]
      print "  fingerprint: %s\n" % exit['fingerprint'][i]

def tor_new():
   """
   Create a new tor circuit
   """
   try:
      stem.socket.ControlPort(port = 6969)
   except stem.SocketError as exc:
      notify("TorTP", "[!] Unable to connect to port 6969 (%s)" % exc)
      sys.exit(1)
   with Controller.from_port(port = 6969) as controller:
      controller.authenticate()
      controller.signal(stem.Signal.NEWNYM)
      notify("TorTP", "[+] New Tor circuit created")

def tor_new_process():
    """
    Drops privileges to TOR_USER user and start a new Tor process
    """
    debian_tor_uid = getpwnam(TOR_USER).pw_uid
    debian_tor_gid = getpwnam(TOR_USER).pw_gid
    os.setgid(debian_tor_gid)
    os.setuid(debian_tor_uid)
    os.setegid(debian_tor_gid)
    os.seteuid(debian_tor_uid)
    os.environ['HOME'] = "/var/lib/tor"

    tor_process = stem.process.launch_tor_with_config(
      config = {
        'SocksPort': '6666',
        'ControlPort': '6969',
        'DNSPort': '9053',
        'DNSListenAddress': '127.0.0.1',
        'AutomapHostsOnResolve': '1',
        'AutomapHostsSuffixes': '.exit,.onion',
        'VirtualAddrNetwork': '10.192.0.0/10',
        'TransPort': '9040',
        'TransListenAddress': '127.0.0.1',
        'AvoidDiskWrites': '1',
        'WarnUnsafeSocks': '1',
      })


def start(tortpdir):
    """
    Start TorTP
    """
    if os.path.exists("%s/resolv.conf" % tortpdir) and os.path.exists("%s/iptables.txt" % tortpdir):
        notify("TorTP", "[!] TorTP is already running")
        sys.exit(2)
    else:
        check_sys_dependencies()
        iptables_clean()
        iptables_up(tortpdir, TOR_USER)
        resolvconf(tortpdir)
        tor_new_process()
        notify("TorTP", "[+] Tor Transparent Proxy enabled")

def stop(tortpdir):
   """
   Stop TorTP and restore original network configuration
   """
   try:
      copy2("%s/resolv.conf" % tortpdir, "/etc")
      os.remove("%s/resolv.conf" % tortpdir)
   except IOError:
      notify("TorTP", "[!] TorTP seems already disabled")
      sys.exit(1)
   iptables_down(tortpdir)
   os.kill(system.get_pid_by_port(6969), 2)
   notify("TorTP", "[+] Tor Transparent Proxy disabled")

def is_running():
   """
   check if TorTP is running
   """
   path = tortp_dir(get_home(check_user()))
   file_path = os.path.join(path, "resolv.conf")
   return os.path.exists(file_path)

def do_start():
   start(tortp_dir(get_home(check_user())))

def do_stop():
   stop(tortp_dir(get_home(check_user())))

def do_check():
   return check_tortp(myip(), get_exit(is_running()))
