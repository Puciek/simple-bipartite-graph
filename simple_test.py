from graph import Graph, SimpleDimensions, Node
graph = Graph(hypothesis_kind=SimpleDimensions.HYPOTHESIS, observation_kind=SimpleDimensions.OBSERVATION)
first_observation = Node(kind=SimpleDimensions.OBSERVATION, uid=1, date='20150110')
second_observation = Node(kind=SimpleDimensions.OBSERVATION, uid=2, date='20150115')
first_hypothesis = Node(kind=SimpleDimensions.HYPOTHESIS, uid=1, name='impossible')
second_hypothesis = Node(kind=SimpleDimensions.HYPOTHESIS, uid=2, name='possible')
graph.connect(result=first_observation, given=first_hypothesis, relationship={'weight': 0.1})
graph.connect(result=first_observation, given=second_hypothesis, relationship={'weight': 0.2})
graph.connect(result=second_observation, given=second_hypothesis, relationship={'weight': 0.3})
print graph
