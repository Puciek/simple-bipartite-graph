__author__ = 'mario alemi'

import collections


class Node(collections.MutableMapping):
    """Practically a dictionary with two mandatory, immutable attributes
    """
    def __init__(self, uid, kind, **kwargs):
        """
        :param uid: the ID of the Node
        :param kind: which kind of node (we use it for multipartite graphs)
        """
        self.__store = dict(**kwargs)
        self.__uid = uid
        self.__kind = kind

    def __setattr__(self, key, value):
        if key in {"uid", "kind"}:
            raise AttributeError("Cannot change %s" % key)
        else:
            collections.MutableMapping.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item == "uid":
            return self.__uid
        elif item == "kind":
            return self.__kind
        else:
            try:
                collections.MutableMapping.__getattribute__(self, item)
            except:
                raise AttributeError("Attribute not found")

    def __getitem__(self, key):
        if key == "uid":
            return self.__uid
        elif key == "kind":
            return self.__kind
        else:
            return self.__store[key]

    def __setitem__(self, key, value):
        if key in {"uid", "kind"}:
            raise AttributeError("Cannot change %s" % key)
        else:
            self.__store[key] = value

    def __delitem__(self, key):
        if key in {"uid", "kind"}:
            raise AttributeError("Cannot delete %s" % key)
        else:
            self.__store[key] = key

    def __len__(self):
        z = self.__get_full_dict()
        return len(z)

    def __hash__(self):
        return hash((self.__uid, self.__kind))

    def __eq__(self, other):
        return (self.__uid, self.__kind) == (other.uid, other.kind)

    def __iter__(self):
        z = self.__get_full_dict()
        return iter(z)

    def update(self, E=None, **F):
        """Update node's values with the given one, uid and kind excluded.
        """
        if E:
            try:
                for k in E:
                    if k not in {"uid", "kind"}:
                        self[k] = E[k]
            except:
                try:
                    for (k, v) in E:
                        if k not in {"uid", "kind"}:
                            self[k] = E[k]
                except:
                    raise TypeError("%s not iterable." % E)
        for k in F:
            if k not in {"uid", "kind"}:
                self[k] = F[k]

    def keys(self):
        z = self.__get_full_dict()
        return z.keys()

    def values(self):
        z = self.__get_full_dict()
        return z.values()

    def iteritems(self):
        z = self.__get_full_dict()
        return z.iteritems()

    def __str__(self):
        return str(self.__get_full_dict())

    def __repr__(self):
        return repr(self.__get_full_dict())

    def __get_full_dict(self):
        """This is apparently the most pythonic way to join two dict.
        see http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
        """
        z = self.__store.copy()
        z.update({"uid": self.__uid, "kind": self.__kind})
        return z
