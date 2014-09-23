===============
logstashHandler
===============

logstashHandler is a basic logging handler for sending to a logstash instance via UDP or TCP encoded as json.


Basic usage
===========

Setup an input on the relevant logstash server::

  input { 
    udp {
      port => 12345
      codec => json
    }
  }

Setup handler and ship logs::

  python
  from logstashHandler import logstashHandler

  lhandler = logstashHandler(host='mylogserver.example.com',port=12345,proto='UDP')
  logger.addHandler(lhandler)
  logger.warn("Something went wrong")


To send additional fields to logstash, use the keyword extra and send a dict starting with extraFields::

    logger.warn('DANGER DANGER',extra={'extraFields':{'name':'W. Robinsson', 'planet':'Unkown'}})

More info can be found on the github page.
