import os
import inspect
import random
import string
import sys
import types

def getWindowsHTTPProxy():
    """ in some intranets an issue: how to use a web proxy for WS. Here
    we assume a set environment variable 'http_proxy'.
    This is common in unix environments. suds does not like
    a leading 'http://'"""
    return os.environ["http_proxy"].replace("http://","")  if os.environ.has_key("http_proxy") else None

def isIterable(object):
    try:
        iter(object)
        return True
    except TypeError:
        return False

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_current_method_mame():
    return inspect.stack()[1][3]

def whoCalledMe():
    return inspect.stack()[2][3]

def mergeDictionaries(dicts):
    superDict={}
    for d in dicts:
        superDict.update(d)
    return superDict

##functions to build raw SOAP messages
def buildRawMessage(method,message):
    return buildOuterMessage(buildInnerMessage(method,message))

def buildOuterMessage(message):
    return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
    {0}
    </soap:Body>
</soap:Envelope>'''.format(message)

def buildInnerMessage(method,message):
    return '''<{0} xmlns="http://api.fromdoppler.com">
    {1}
</{0}>'''.format(method.strip(),message.strip())

def getActionName(action):
    return string.split(action,'.')[1]

def unbind(f):
    """
    Function that unbinds a given function if it's actually binded to an object. If it's not binded to an object it'll
    raise a TypeError Exception

    :param f: function to unbind from an object
    :type f: function
    :raises: TypeError
    """
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, types.ModuleType) and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')

def bind(f, obj,new_f_name):
    obj.__dict__[new_f_name] = types.MethodType(f, obj, obj.__class__)

def rebind(f, obj,new_f_name=None):
    bind(unbind(f), obj,new_f_name or f.__name__)
