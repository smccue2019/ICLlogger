# ICLlogger
A simple logger and control for DSL Inductively Coupled Link temperature probes.
Built using PyQt5. First version uses low level UDP comms to and from a Moxa serial
to UDP device. Direct serial comms would be a useful addition.
The GUI displays the most recent measurement. The measurement is appended to a log file,
which is named according to start of log timestamp.

