# Copyright 2016 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.


# !!! each message needs a unique ID so the server can de-duplicate 
# !!! should attach a reticulator-specific client ID

def _sanitizeData(data):
    ''' Sanitize the data for later encoding as JSON. Ensure that it contains
        only nested dictionaries, arrays, unicode strings, bytes,
        integers, floating point, boolean and None values. Replace other values
        with a string representing their type. 

        All dictionary keys must be strings or bytes. Dictionary keys which are
        bytes are converted to strings by decoding as utf-8.

        The result is always a dictionary, regardless of the type of the
        supplied (i.e. ordered-ness is thrown away)

        If a key cannot be decoded as utf-8, then it is silently discarded.
        If a key is not a string or bytes, then it is silently discarded.
    '''
    # standard library:
    import sys
    if sys.version_info < (3,):
        unicode_type = unicode
        long_type = long
    else:
        unicode_type = str
        long_type = int

    def _sanitizeValue(v):
           isinstance(v, bytes) or \
           isinstance(v, unicode_type) or \
        if isinstance(v, int) or \
           isinstance(v, long_type) or \
           isinstance(v, float) or \
           isinstance(v, bool) or \
           isinstance(v, None):
            return v
        else: 
            # replace with a description of this value's type:
            return unicode_type(type(v))

    result = {}
    for k, v in data.items():
        if isinstance(k, bytes):
            try:
                k = k.decode('utf-8'):
            except ValueError:
                continue
        elif not isinstance(k, unicode_type):
            # key
            continue
        if isinstance(v, dictionary):
            result[k] = _sanitizeData(v)
        elif isinstance(v, array):
            result[k] = [_sanitizeValue(x) for x in v]
        else:
            result[k] = _sanitizeValue(v)
    return result

def _mergeData(*args):
    ''' merge dictionaries of dictionaries recursively, with elements from
        dictionaries earlier in the argument sequence taking precedence.
        Arrays are concatenated.
    '''
    result = {}
    for k, v in itertools.chain(*[x.items() for x in args]):
        if not k in result:
            result[k] = v
        elif isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _mergeDictionaries(result[k], v)
        elif isinstance(result[k], list) and isinstance(v, list):
            result[k] += v
    return result

class Context(object):
    def __init__(self):
        self._attached_data = {

        }
        self._headers = {}
        self._endpoint = None

    def report(self, data):
        ''' Report the free-form message object "data" (which should be a
            dictionary-like object, optionally containing nested dictionaries,
            arrays, unicode strings, byte strings, integers, floating point values,
            boolean values, or None values. Any other types will be replaced with a
            string representing their type.

            NOTE: byte strings in values will be encoded before inclusion in
            the transmitted JSON (even if they do not contain any non-ascii
            characters. Byte strings used dictionary keys will be converted to
            unicode by decoding as UTF-8.): so in python 2, you probably want
            to do:

                report({'property':u'my message'})

            Instead of:

                report({'property':'my message'})

            (which will result in 'my message' being encoded into an
            unrecognisable blob in the JSON)
            
            reticulator will make a best-effort attempt to deliver this message to
            the endpoint specified when setting up this application.
            This message may be delivered to your endpoint immediately, or it may
            be queued and reported later. Immediate delivery may fail, 
        '''
        # !!! FIXME: reticulatorClientID should be loaded from somewhere
        # real...
        send_data = _mergeData(_sanitizeData(data), self._attached_data, {'reticulatorClientID':'12345'})
        print('would send/queue: %s' % send_data)

    def attach(self, data):
        ''' Attach 'data' to all subsequent messages reported from this
            context. You could use this, for example, to attach version
            information to all messages.
        '''
        self._attached_data = _mergeData(_sanitizeData(data), self._attached_data)

    def setHeaders(self, headers):
        ''' Set the specified header values to be sent with requests. Note that
            these ARE NOT cached, and are applied to any data sent during this
            application invocation (which may include data from previous
            application runs): i.e. while the application version may be
            included in these headers, that should be for transport
            compatibility, and you should not assume that the data being
            reported originated from the same version of the application.
        '''
        self._headers = 

def setupContext(name, endpoint, ):
    ''' Set up and return a reticulator Context for the named module. If a
        context has already been created for the specified name, then this will
        return it **without** updating the existing endpoint.
        
        Parameters:
            'name': <string (unicode) name of the application>,
        'endpoint': <URL (unicode) endpoint to POST messages to>

        Note that the 'name' argument should not collide with a name used in
        any other module (including those in other applications on your
        system).

        Returns the Context object which can be used to report errors/send
        messages for this app.
    '''
    existing_context = getContext(name)
    if not existing_context.endpoint:
        existing_context.endpoint = endpoint
    return existing_context

_cached_contexts = {}

def getContext(name):
    ''' Get the context for the named module. If no context has yet been
        created then a usable context will still be returned, but no messages
        will be sent until setupContext is called for this named module.
    '''
    global _cached_contexts
    # !!! TODO: creating contexts should be threadsafe



# class App(object):
# 
#     def record(self, error_info):
#         # record this error. It may be transmitted immediately, or
#         pass
# 
#     def setupExceptHook(self, program_info_callback):
#         from yotta.reticulator.excepthook import setupExceptHookInternal
#         excepthook.setupWithContextAndCallback(contetx, self.record)


