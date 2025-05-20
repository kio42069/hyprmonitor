# Hyprmonitor
A simple tool to track application usage time, with visualisation support

# Description
Hyprmonitor is a python based application, currently in its CLI/TUI stage. 
Users can view their app wise usage data, tab wise usage data, and also look up the logs of a certain date for both the supported tabs
Logs are available on a per-day basis, stored as serialised dictionary objects in a logs directory
It logs the system data as a python dictionary object, the next version will be ported to a JSON logfile based system. That way, users can export the raw data and do their own personal analysis 

Future updates will include a user interface, both web-based and a standable native QT application, with graphs for visualisation, and filters for date, time, tags, and more~
It is shipped with a systemd service, so the user can either have the monitor module in their autostart scripts, or have systemd manage the service

# Development Roadmap
- [x] Backend
- [x] TUI / CLI based user interaction
- [ ] Django based web UI 
- [ ] QT6-pyside based native desktop application
- [ ] Windows Port

# Featureset
- [ ] Pie chart and bar graphs based visualisation
- [ ] Two tabs: 1 for application level stats, tab 2 for window level stats (more spammy == gross)
- [ ] Tags support:  sort applications by hardcoded types - productivity, gaming, development, miscellaneous 
- [ ] Browser extension: to track your browser activity as well
- [ ] Productivity mode: native to the desktop application, will use the provided notification daemon to help with productivity
- [x] JSON support: user can take raw collected data and use any online LLM for analysis
- [ ] Locally hosted LLM based statistics analysis and suggestion generator
