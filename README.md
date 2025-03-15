# Linux-Remote-Monitor
This repo contains a Linux Remote Monitor that upon setup with a firewall rule for the API on the server, allows clients to connect to the server and obtain data through the API. The following information is collected: CPU usage, disk usage, memory usage, swap usage, 1-min load average, network sent/received, and server uptime. 

All of this information is sent into the client through the /stats endpoint made available by the server. The stat_writer puts all of the statistical information into a pipe to allow multiple client requests to be more efficient. 

In addition to collect server information, there is a built in stress test script using the stress-ng module to periodically conduct stress tests on the server to change the output shown to the client. 
