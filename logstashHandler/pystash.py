"""
Simple logging handler for sending logstash messages
formatted as json via TCP or UDP
Author: Stewart Rutledge <stew.rutledge AT gmail.com>
License: BSD I guess
"""
import logging
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, getfqdn
from json import dumps


class handler(logging.Handler):

    def __init__(self, **kw):
        self.proto = kw.get('proto', 'UDP')
        self.host = kw.get('host', 'localhost')
        self.port = kw.get('port', None)
        self.fullInfo = kw.get('fullInfo', False)
        if self.proto == 'UDP' and self.port is None:
            raise ValueError('Must specify a port')
        if self.proto == 'TCP' and self.port is None:
            raise ValueError('Must specify a port')
        self.facility = kw.get('facility', None)
        self.fromHost = kw.get('fromHost', getfqdn())
        self.levelsDict = kw.get('levels', None)
        self.levelLabel = kw.get('levelLabel', 'level')
        logging.Handler.__init__(self)

    def transformLevels(self, level):
        if self.levelsDict and isinstance(self.levelsDict, dict):
            level = self.levelsDict.get(level, level)
            return(level)
        else:
            raise TypeError('Levels must be a dictionary')

    def emit(self, record, **kwargs):
        levelLabel = self.levelLabel
        if self.proto == 'UDP':
            self.sock = socket(AF_INET, SOCK_DGRAM)
        if self.proto == 'TCP':
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.host, int(self.port)))
        recordDict = record.__dict__
        msgDict = {}
        msgDict['version'] = '1'
        msgDict['timestamp'] = recordDict['created']
        msgDict[levelLabel] = self.transformLevels(recordDict['levelname'])
        msgDict['message'] = recordDict['msg']
        msgDict['host'] = self.fromHost
        if self.fullInfo is True:
            msgDict['pid'] = recordDict['process']
            msgDict['processName'] = recordDict['processName']
            msgDict['funcName'] = recordDict['funcName']
        if self.facility is not None:
            msgDict['facility'] = self.facility
        elif self.facility is None:
            msgDict['facility'] = recordDict['name']
        extra_props = recordDict.get('extraFields', None)
        if isinstance(extra_props, dict):
            for k, v in extra_props.iteritems():
                msgDict[k] = v
        if self.proto == 'UDP':
            msg = dumps(msgDict) + '\n'
            self.sock.sendto(msg, (self.host, self.port))
        if self.proto == 'TCP':
            msg = dumps(msgDict) + '\n'
            try:
                self.sock.sendall(msg)
                self.sock.close()
            except Exception as e:
                raise IOError('Could not send message via TCP: %s' % e)
