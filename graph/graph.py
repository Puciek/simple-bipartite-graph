__date__ = 'January 2015'
__version__ = 0.1
__license__ = 'Apache License 2.0'
__authors__ = 'Mario Alemi'

from collections import defaultdict
from simple_dimensions import SimpleDimensions
from node import Node


class Graph:
    """
    Bipartite graph. There are two kinds of nodes: hypotheses and observations.
    At the moment the Graph.to_dict and Graph.from_dict do not allow relationships
    between hypotheses or between observations, only between the two different kinds.
    """

    def __init__(self, hypothesis_kind=SimpleDimensions.HYPOTHESIS,
                 observation_kind=SimpleDimensions.OBSERVATION,
                 verbose=0):
        """
        Name of the hypotheses' dimension and observations'

        :param hypothesis_kind: a Node.kind
        :param observation_kind: a Node.kind
        :param verbose: 0=silent, 1=errors, 2=warnings, 3=debug
        """
        self._links = defaultdict(dict)
        self._collection = {}
        self._dimensions = []
        self.observation_kind = observation_kind
        self.hypothesis_kind = hypothesis_kind
        self.verbose = verbose
        for dimension in [hypothesis_kind, observation_kind]:
            self.__add_dimension(dimension)
        self.unknown = None

    def __add_dimension(self, kind):
        self._dimensions.append(kind)

    def connect(self, result, given, relationship=None):
        """
        Create a relationship from given to result:
        If relationship is a Probability, this is P(result|given).
        Normally we have likelihood(observation, hypothesis), therefore is
        normally something like:

        In: graph.update(observation)
        In: graph.update(hypothesis)
        In: graph.connect(result=observation,
                          given=hypothesis,
                          relationship={'probabilities': 0.5})
        :param result: Dimension
        :param given: Dimension
        """
        if result.kind not in self._dimensions:
            raise NameError("Dimension %s not in %s" % (result.kind, self._dimensions))

        if given.kind not in self._dimensions:
            raise NameError("Dimension %s not in %s" % (given.kind, self._dimensions))

        if relationship is None:
            relationship = {}

        if not self.find(uid=result.uid, kind=result.kind):
            self.update(result)
        if not self.find(uid=given.uid, kind=given.kind):
            self.update(given)

        self._links[(result.uid, result.kind)][(given.uid, given.kind)] = relationship
        if not self._links[(given.uid, given.kind)].get((result.uid, result.kind)):
            self._links[(given.uid, given.kind)][(result.uid, result.kind)] = {}

        self._collection[(result.uid, result.kind)] = result
        self._collection[(given.uid, given.kind)] = given

    def nodes(self, dimension):
        """
        :param dimension:
        :return: all node of a certain dimension
        """
        return {self.find(uid, kind) for uid, kind in self._collection if kind == dimension}

    def connected(self, item, relationship_query=None, nodes_query=None):
        """
        Returns all connected items except the ones added through Graph.smooth(), or makes a query, e.g.:
        relationship_query={'foo': None}
        :param item: item to which the returned nodes are connected
        :param relationship_query
        :param nodes_query
        :return:
        """
        for (uid, kind) in self._links[(item.uid, item.kind)]:
            connection = self.find(uid, kind)
            try:
                if relationship_query:
                    for k, v in relationship_query.iteritems():
                        if not self.relationship(result=connection, given=item).get(k) == v:
                            raise GeneratorExit
                if nodes_query:
                    for k, v in nodes_query.iteritems():
                        if not connection.get(k) == v:
                            raise GeneratorExit
                yield connection
            except GeneratorExit:
                continue

    def relationship(self, result, given):
        return self._links[(result.uid, result.kind)].get((given.uid, given.kind))

    def find(self, uid, kind):
        return self._collection.get((uid, kind))

    def update(self, item):
        self._collection[(item.uid, item.kind)] = item

    def keys(self):
        return [self.find(item.uid, item.kind) for item in self._links.iterkeys()]

    def values(self):
        return [self.find(item.uid, item.kind) for item in self._links.itervalues()]

    def iterkeys(self):
        return (self.find(item.uid, item.kind) for item in self._links.iterkeys())

    def itervalues(self):
        return (self.find(item.uid, item.kind) for item in self._links.itervalues())

    def iteritems(self):
        return ((self.find(k.uid, k.kind), self.find(v.uid, v.kind)) for k, v in self._links.iteritems())

    def collapse_nodes(self, old, new):
        """
        All relationship of id_old are moved to id_new.

            . If id_old does not exist does nothing (warning)
            . If id_new does not exist just rename

        :param old
        :param new
        :return: nothing, update the similarity matrix
        """
        pass

    def from_dict(self, dic):
        """
        Read a dict and build/update the graph
        """
        for k in dic:
            for v in dic[k]:
                # print 'g[' + k + '] = ' + v
                self.connect(given=Node(**v),
                             result=Node(**k))

    def to_dict(self, keys_dimension, verbose=0):
        """
        Return a dict representation of the graph.
        If keys_dimension=hypothesis and values are observations:
        {hypothesis1: [observation1, observation2...], ....}
        Vice versa:
        {observation1: [hypothesis1, hypothesis2....], ....}
        """
        if keys_dimension not in [self.hypothesis_kind, self.observation_kind]:
            if self.verbose > 0:
                print("Graph.from_dict: wrong nodes for keys and values: %s" %
                      keys_dimension)
            return None

        d = defaultdict(set)
        for k in self.nodes(keys_dimension):
            for node in self.connected(k):
                if verbose > 3:
                    print('g[' + k.uid + '] = ' + node.uid)
                d[k].add(node)
        return d

    def __str__(self):
        s = u"%s\tconnections\n" % self.hypothesis_kind
        for hypothesis in self.nodes(self.hypothesis_kind):
            s += u"'%s'" % hypothesis.uid
            for node in self.connected(hypothesis):
                s += u"\t<=\t '%s' (%s) \n" % (node.uid, node.kind)
        return s

    def __repr__(self):
        s = u"%s\tconnections\n" % self.hypothesis_kind
        for hypothesis in self.nodes(self.hypothesis_kind):
            s += u"'%s'" % hypothesis.uid
            for node in self.connected(hypothesis):
                s += u"\t<=\t '%s' (%s) \n" % (node.uid, node.kind)
        return s
