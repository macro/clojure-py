from clojure.lang.namespace import findOrCreate as findNamespace

class ProtocolException(Exception):
    def __init__(self, msg):
        Exception.__init__(msg)



def getFuncName(protocol, funcname):
    return str(protocol) + funcname
    
class ProtocolFn(object):
    """Defines a function that dispatches on the type of the first argument
    passed to __call__"""
    
    def __init__(self, fname):
        self.dispatchTable = {}
        self.name = intern(fname)
        self.attrname = intern("__proto__" + self.name)
        self.default = None
        
    def extend(self, tp, fn):
           
        try:
            setattr(tp, self.attrname, fn)
        except:
            self.dispatchTable[tp] = fn
            
    def extendForTypes(self, tps, fn):
        for tp in tps:
            self.extend(tp, fn)
            
    def setDefault(self, fn):
        self.default = fn
            
    def isExtendedBy(self, tp):
        if hasattr(tp, self.attrname) or tp in self.dispatchTable:
            return True
        return False
            
    def __call__(self, *args):
        x = type(args[0])
        if hasattr(x, self.attrname):
            return getattr(x, self.attrname)(*args)
        else:
            try:
                return self.dispatchTable[x](*args)
            except:
                if self.default:
                    return self.default(*args)
                raise
            
    def __repr__(self):
        return "ProtocolFn<" + self.name + ">"
        
    
    
class Protocol(object):
    def __init__(self, ns, name, fns):
        """Defines a protocol in the given ns with the given name and functions"""
        self.ns = ns
        self.name = name
        self.fns = fns
        self.protofns = registerFns(ns, fns)
        self.__name__ = name
        self.implementors = {}
        
    def markImplementor(self, tp):
        if tp.__name__ in self.implementors:
            return
            
        self.implementors[tp.__name__] = tp
        
    def __repr__(self):
        return "Protocol<" + self.name + ">"
        
        
        
def registerFns(ns, fns):
    ns = findNamespace(ns)
    protofns = {}
    for fn in fns:
        fname = ns.__name__ + fn
        if hasattr(ns, fn):
            proto = getattr(ns, fn)
        else:
            proto = ProtocolFn(fname)
            setattr(ns, fn, proto)
        proto.__name__ = fn
        protofns[fn] = proto
        
    return protofns
        
        
def protocolFromType(ns, tp):
    """Considers the input type to be a prototype for a protocol. Useful for
    turning abstract classes into protocols"""
    fns = []    
    for x in dir(tp):
        if not x.startswith("_"):
            fns.append(x)
            

        
    thens = findNamespace(ns)
    proto = Protocol(ns, tp.__name__, fns)
    
    if not hasattr(tp, "__protocols__"):
        tp.__protocols__ = []
    tp.__protocols__.append(proto)
    
    if not hasattr(thens, tp.__name__):
        setattr(thens, tp.__name__, proto)
    return proto
    
def extendForAllSubclasses(tp):
    if not hasattr(tp, "__protocols__"):
        return
    
    for proto in tp.__protocols__:
        _extendProtocolForAllSubclasses(proto, tp)
        
def _extendProtocolForAllSubclasses(proto, tp):
    extendProtocolForClass(proto, tp)
    
    for x in tp.__subclasses__():
        _extendProtocolForAllSubclasses(proto, x)
    

def extendForType(interface, tp):
    if not hasattr(interface, "__protocols__"):
        return
    
    for proto in interface.__protocols__:
        extendProtocolForClass(proto, tp)

def extendProtocolForClass(proto, tp):
    for fn in proto.protofns:
        
        pfn = proto.protofns[fn]
        if hasattr(tp, fn):
            pfn.extend(tp, getattr(tp, fn))
        
    proto.markImplementor(tp)
    
        
    
    
    
    
    
    
        
