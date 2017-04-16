def start_events(events):
   log = [];
   localCounter = 0;
   received = False;
   for e in events:
      localCounter += 1;
      event_parts = e.split()

      if event_parts[0]=="call":
         call(event_parts[1], int(event_parts[2]), localCounter)
         print "call"

      elif event_parts[0]=="receive":
         while not received:
            if not call_queue.empty():
               remoteCounter = int(call_queue.get())
               print "recahed here"
               if remoteCounter>=0:
                  remoteCounter += 1
                  localCounter = max(localCounter, remoteCounter)
                  received = True
                  print "received"
            #print "not recived"

      log.append([e, localCounter])
   print log