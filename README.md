# jarMonitor
This is a lightweight tool written in python to monitor jar applications in your host, pull up apps once it crashed, hot reload is supported.

## How do I use it?
      1. edit conf.json to add your app in the list:
          Add your monitoring app under "apps" list, include its dir and jar file name.
          start or stop the monitoring by setting "activated" as true or false.
          set polling interval by setting "polling_interval", default is 10 seconds.
          set log file name by setting "log_file".
          {
              "apps": [
                  {
                      "cwd" : "/home/sw/jarfiles/",
                      "name": "china.tower-1.0-SNAPSHOT.jar"
                  }
              ],
              "activated": true,
              "polling_interval": 10,
              "log_file": "jarMonitor.log"
          }

      2. run it:
        > nohup python jarMonitor.py &

      3. Hot reload is supported:
         To edit the apps list, "activated" flag and "polling_interval", you DON'T need to restart the monitor.

## Logging?
      The default log file is stored at jarMonitor.log
