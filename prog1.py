#!/usr/bin/python

import Queue
import threading
import argparse
import socket, struct
import errno
import time

call_queue = Queue.Queue()

def DoesServiceExist(host, port):
    captive_dns_addr = ""
    host_addr = ""

    try:
        captive_dns_addr = socket.gethostbyname("BlahThisDomaynDontExist22.com")
    except:
        pass

    try:
        host_addr = socket.gethostbyname(host)

        if (captive_dns_addr == host_addr):
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
    except:
        return False

    return True

def call(host, port, localCounter):
   s = socket.socket()
   #print "Calling: " + host + ", " + str(port) + ", " + str(localCounter)
   #while not DoesServiceExist(host, port):
   #   pass
   time.sleep(5)
   s.connect((host, port))

   #print s.recv(1024)
   s.send(str(localCounter))
   s.close()
   

def start_events(events):
   log = [];
   localCounter = 0;
   received = False;
   for e in events:
      localCounter += 1;
      event_parts = e.split()

      if event_parts[0]=="call":
         call(event_parts[1], int(event_parts[2]), localCounter)

      elif event_parts[0]=="receive":
         while call_queue.empty():
            #do nothing
            pass
         remoteCounter = int(call_queue.get())
         if remoteCounter>=0:
            remoteCounter += 1
            localCounter = max(localCounter, remoteCounter)
            received = True
            #print "received"
            #print "not recived"

      #log.append([e, localCounter])
      log.append(localCounter)
   print(*log)

def start_listening(port):
   s = socket.socket()
   host = socket.gethostname()
   #print "REeceive: " + host + ", " + str(port)
   s.bind(('',port))
   s.listen(5)
   while True:
      c, addr = s.accept()
      call_queue.put(c.recv(1026))
      c.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('port', type=int)
    res = parser.parse_args()
    inputfile = res.file
    port = res.port
    
    with open(inputfile) as f:
      inputRaw = f.readlines()
    events = [x.strip() for x in inputRaw]


    #start events thread
    events_thread = threading.Thread(target=start_events, args = (events,))
    events_thread.daemon = True
    events_thread.start()

    #start listening thread
    listening_thread = threading.Thread(target=start_listening, args = (port,))
    listening_thread.daemon = True
    listening_thread.start()

    events_thread.join()
    listening_thread.join()

    print port