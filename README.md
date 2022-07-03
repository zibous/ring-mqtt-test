## RING MQTT Testcase

### Requirements
Ring MQTT
see: https://github.com/tsightler/ring-mqtt


## Install

On a modern Linux system just a few steps are needed to get the daemon working. The following example 
shows the installation under Debian/Raspbian below the `/opt` directory:

```bash
$ git clone https://github.com/zibous/ring-mqtt-test.git /opt/ring-mqtt-test
$ cd /opt/ring-mqtt-test
$ sudo pip3 install -r requirements.txt
```

## Run testcase
`python3 app.py -l DEBUG`

