#!/usr/bin/python

import Queue
import threading
import argparse
import socket

call_queue = Queue.Queue()

def receive_call(host, port):
   s = socket.socket()
   s.connect((host, port))
   print s.recv(1024)
   inpt = raw_input('type anything and click enter... ')
   s.send(inpt)
   print "the message has been sent"
   return 1
   

def start_events(events):
   log = [];
   localCounter = 0;
   for e in events:
      localCounter += 1;
      event_parts = e.split()
      if event_parts[0]=="call":
         remoteCounter = receive_call(event_parts[1], event_parts[2])
         localCounter = max(localCounter, remoteCounter)
      log.append([e, localCounter])
   print log

def start_listening(port):
   s = socket.socket()
   host = socket.gethostname()
   port = 1247
   s.bind((host,port))
   s.listen(5)
   while True:
      c, addr = s.accept()
      print("Connection accepted from " + repr(addr[1]))
      c.send("Server approved connection\n")
      print repr(addr[1]) + ": " + c.recv(1026)
      c.close()

   #q.put(urllib2.urlopen(url).read())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('port', type=int)
    res = parser.parse_args()
    inputfile = res.file
    port = res.port
    
    with open(inputfile) as f:
      inputRaw = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    events = [x.strip() for x in inputRaw]


    #start events thread
    events_thread = threading.Thread(target=start_events, args = (events,))
    events_thread.daemon = True
    events_thread.start()

    #start listening thread
    listening_thread = threading.Thread(target=start_listening, args = (port,))
    listening_thread.daemon = True
    listening_thread.start()

    print port