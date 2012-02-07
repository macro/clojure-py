from py.clojure.lang.cljexceptions import AbstractMethodCall
from py.clojure.lang.ipersistentcollection import IPersistentCollection
from py.clojure.lang.counted import Counted

class IPersistentSet(IPersistentCollection, Counted):
    def disjoin(self, key):
        raise AbstractMethodCall(self)

    def __contains__(self, item):
        raise AbstractMethodCall(self)

    def __getitem__(self, item):
        return self.get(item)
