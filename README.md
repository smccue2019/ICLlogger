A simple logger and control for DSL Inductively Coupled Link temperature probes,
developed initially for ROV Jason ops. Communication with the probe system is serial,
but comms by network fits better in the Jason control vans. This util expects a Moxa-
like appliance to negotiate serial to network comms. Further, this util expects the
appliance to be operating as a TCP server.
Report of a measurement is triggered by a query sequence from this util, to which the
probe will report a single measurement. The measurement is parsed and temperatures
are displayed in the GUI. The unparsed measurement record is also saved as ASCII to
log file. Log files are timestamped according to when the user clicks a "start logging"
button, and the file is closed upon a "stop logging" or "quit" command.
Built using PyQt5.
