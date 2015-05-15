## The Graph

*"Graph"* is a bipartite graph class. The aim is to be able to deal with hypotheses and observations and the relationships between them. These two dimensions must be specified at init:

    __init__(self, hypothesis_kind='hypothesis', observation_kind='observation', verbose=0)
        :param hypothesis_kind: a DictDimension.kind
        :param observation_kind: a DictDimension.kind

E.g.

    graph = Graph('hypothesis', 'observation')

## The nodes

*"Node"* objects are based on [collections.MutableMapping](https://docs.python.org/2/library/collections.html#collections.MutableMapping). They are basically dictionaries, with two immutable fields (<code>uid</code> and <code>kind</code>) which make the object hashable. 

## Relationship between nodes

Relationship should be dictionaries.

## Example

    from elegans_graph import Graph, SimpleDimensions, Node
    graph = Graph(hypothesis_kind=SimpleDimensions.HYPOTHESIS, observation_kind=SimpleDimensions.OBSERVATION)
    first_observation = Node(kind=SimpleDimensions.OBSERVATION, uid=1, date='20150110')
    second_observation = Node(kind=SimpleDimensions.OBSERVATION, uid=2, date='20150115')
    first_hypothesis = Node(kind=SimpleDimensions.HYPOTHESIS, uid=1, name='impossible')
    second_hypothesis = Node(kind=SimpleDimensions.HYPOTHESIS, uid=2, name='possible')
    graph.connect(result=first_observation, given=first_hypothesis, relationship={'weight': 0.1})
    graph.connect(result=first_observation, given=second_hypothesis, relationship={'weight': 0.2})
    graph.connect(result=second_observation, given=second_hypothesis, relationship={'weight': 0.3})
    print graph

