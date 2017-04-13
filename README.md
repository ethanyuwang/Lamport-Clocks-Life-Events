# Lamport-Clocks-Life-Events

Implementation of Lamport Clocks to Order Life Events
04/05/2017
This assignment aims to help students understand Lamport clocks [1] and sockets programming.
1 Introduction
Lamport logical clocks [1] are used to order events capturing causality or happens before relationship
between events. An event e happens before another event f (denoted by e → f) iff:
• the same process executes e and f and e is executed before f,
• e is the send event of a message m (send(m)) and f is the corresponding receive of a message
m (receive(m)), or
• ∃h | e → h ∧ h → f
In this assignment, you are required to write a program that assigns Lamport clocks to events
happening on different processes. These processes communicate with each other using sockets.
There is no shared memory between the running processes.
2 Implementation
The events that need to be ordered are life events of different people. Each person is represented
by a process and has two types of life events:
• local events like sleep, eat, shower, wake up, etc, and
• communication between 2 persons via phone calls.
Each process reads its life events from a file. There is one input file per process and each input
file has one event per line. Communication between processes is implemented using TCP sockets.
Communication between two process is represented by a call event (in the sender process) and a
receive event (in the receiver process). Each process has a counter initialized by zero. For each
local event, a process increments its local counter and assigns the counter value to this event. A
call event must have a destination represented by an IP address and a port number. A call event
piggybacks the local counter value in the call request. A process has to block on receive events
until receiving a message on the TCP socket. Upon receiving a message, a process has to compare
the local counter value to the received value and decides a value assignment to the receive event
and updates the local counter accordingly.
Each process is implemented using two threads as shown in Figure 1. A communication thread
listens on a TCP socket for any messages sent to this process. Upon receiving a message, the
communication thread puts the message in a shared producer/consumer queue and blocks waiting
on receiving more messages. A processing thread processes the events one by one until having a
receive event. For a receive event, a processing thread pops a message from the producer/consumer
queue, if any exists, or block until a message is inserted in the queue. This ways prevents a potential
race condition between the send and receive events.
The processing thread should output the assigned clock values to its events space separated.
Section 3 gives a sample input and the corresponding output.
1
Figure 1: An implementation of a process using 2 threads: a communication thread and a processing
thread.
P1 P2 P3
wakeup wakeup wakeup
eat call 127.0.0.1 5001 shower
receive call jog eat
shower
study
call 127.0.0.1 5002
receive call
call 127.0.0.1 5003
receive call
Table 1: A sample input of 3 processes.
3 Sample input and output
A sample input of 3 processes and their corresponding output are shown in Tables 1 and 2
respectively. Your program should take the port number to bind a socket at (first argument) and
the input file path (second argument) as its arguments (e.g. /asg1 5001 p1.txt). Input events are
represented in the input file one at each line. The program should output the assigned counter
values space separated to the standard output.
4 Submission policy and deadline
You should work on this assignment individually. There is no restriction on the programming
language but you have to use a platform that can run on any of the Linux CSIL machines. You
should submit one tar file on Gaucho space that has the source files and an executable file that
can run directly on a Linux CSIL machine by April 14th 11:59pm. Please make sure to name your
executable asg1. We will run this executable file over some test cases and give you credit based
on your program responses. There is no partial credit on submitting non functioning code so it is
better to start NOW.
P1 P2 P3
1 2 3 4 5 6 1 2 3 7 8 1 2 3 9
Table 2: The output corresponding to the sample input shown in Table 1.
2
References
[1] L. Lamport. Time, clocks, and the ordering of events in a distributed system. Communications
of the ACM, 21(7):558–565, 1978.
3
