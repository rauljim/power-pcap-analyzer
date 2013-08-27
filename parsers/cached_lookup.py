import socket
import cPickle

filename = 'cached_lookups'
cached_lookups = {}

def load():
    global cached_lookups
    try:
        cached_lookups = cPickle.load(open(filename))
    except:
        cached_lookups = {}
    print 'loaded DNS lookups:', len(cached_lookups)

def gethostbyaddr(addr):
    try:
        return cached_lookups[addr]
    except (KeyError):
        try:
            return cached_lookups.setdefault(addr,
                                         socket.gethostbyaddr(addr))
        except (socket.herror):
            return cached_lookups.setdefault(addr, 'NA')

def save():
    cPickle.dump(cached_lookups, open(filename, 'wb'))
    print 'saved DNS lookups:', len(cached_lookups)
