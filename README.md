# logstashHandler

logstashHandler is a basic logging handler for sending to a logstash instance via UDP or TCP encoded as json.

## Basic usage

Install via pip:

`pip install logstashHandler`

Setup an input on the relevant logstash server:

```
input { 
  udp {
    port => 12345
    codec => json
  }
}

```python
from logstashHandler import logstashHandler

lhandler = logstashHandler(host='mylogserver.example.com',port=12345,proto='UDP')
logger.addHandler(lhandler)
logger.warn("Something went wrong")
```

There are three additional arguments: 

`fromHost='myhost'` which is the hostname field sent to logstash (default fqdn)

`facility='superlogger'` which is sent as the facility field in logstash (default is the loggers name)

`fullInfo=True` which sends the module the message came in, the pid of the process and the process name with the message

`levelLabel='severity'` Sets the label used for the log level

`levels=someDict` A dictionary for transforming the default level labels to something else, for example:

```python
   levels = {'ERROR': 3, 'WARNING': 2, 'INFO': 1, 'DEBUG': 0}
   lhandler = logstashHandler(
       host='mylogserver.example.com', 
       port=12345,proto='UDP',
       levels=levels,
       levelLabel='severity'
   )
```

The only protocols supports are UDP and TCP

To send additional fields to logstash, use the keyword extra and send a dict starting with `{'extraFields':`


```python
    logger.warn('DANGER DANGER',extra={'extraFields':{'name':'W. Robinsson', 'planet':'Unkown'}})
```



## Fallbacks

* TCP with SSL is not currently supported.
* Buffer size is not taken into account.

