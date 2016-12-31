import io
import pycurl
import os
import sys
import random
from stem.control import Controller
from stem.util import system

import stem.process
from stem.util import term
import time

import mongodb_client


SOCKS_PORT = 7000
CONTROL_PORT = 6969

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

USER_AGENTS_FILE = '../common/user_agents.txt'
USER_AGENTS = []


"""Uses pycurl to fetch a site using the proxy on the SOCKS_PORT"""
def query(url):

  output = io.BytesIO()

  query = pycurl.Curl()
  query.setopt(pycurl.URL, url)
  query.setopt(pycurl.HTTPHEADER, getHeaders())
  query.setopt(pycurl.PROXY, 'localhost')
  query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
  query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
  query.setopt(pycurl.WRITEFUNCTION, output.write)

  through = False
  while not through:
    try:
      query.perform()
      http_code = query.getinfo(pycurl.HTTP_CODE)
      if http_code == 200:
        through = True
      else:
        # renew tor to retry
        print 'error httpcode:' +str(http_code)
        renew_tor()
        # time.sleep(3)
    except pycurl.error as exc:
      print "pycurl error in tor.py %s" % exc
      # return "Unable to reach %s (%s)" % (url, exc)



  return output.getvalue()


"""print tor bootstrap info"""
def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))


"""get user-agent and httpheader string list"""
def getHeaders():
  ua = random.choice(USER_AGENTS)  # select a random user agent
  headers = [
    "Connection: close",
    "User-Agent: %s"%ua
  ]
  # print headers
  return headers


"""start tor process"""
def start_tor():
  tor_process = system.pid_by_port(SOCKS_PORT)
  if  tor_process is None:
    tor_process = system.pid_by_name('tor')
  if  tor_process is None:
    tor_process = stem.process.launch_tor_with_config(
      config={
        'SocksPort': str(SOCKS_PORT),
        'ControlPort': str(CONTROL_PORT),
        'ExitNodes': '{ru}',
      },
      init_msg_handler=print_bootstrap_lines,
    )
  else:
    print "tor already running, no need to start"


"""renew tor circuit"""
def renew_tor():
   """
   Create a new tor circuit
   """
   try:
      stem.socket.ControlPort(port = CONTROL_PORT)
   except stem.SocketError as exc:
      print ("Tor", "[!] Unable to connect to port %s (%s)" %(CONTROL_PORT , exc))
   with Controller.from_port(port = CONTROL_PORT) as controller:
      controller.authenticate()
      controller.signal(stem.Signal.NEWNYM)
      print ("TorTP", "[+] New Tor circuit created")
      print 'renewed:' + query("http://icanhazip.com")


"""stop tor process"""
def stop_process_on_name():
  process =  system.pid_by_name('tor')
  if  process is not None:
    os.kill(process, 2)

"""read user-agent"""
with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip())
random.shuffle(USER_AGENTS)


"""start tor instance when called this module"""
start_tor()

query("www.zillow.com")

db = None
db = mongodb_client.getDB()
if  db is None:
  print "fail"
else:
  print "succeed"

