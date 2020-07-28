import random
from time import time

import matplotlib.pyplot as plt
import networkx
import numpy as np
from pomegranate import BayesianNetwork, ConditionalProbabilityTable, DiscreteDistribution, Node

seed = 38938943
random.seed(seed)
np.random.seed(seed)

def generate_meetings(num_days, num_people, num_meetings_per_day):
    meetings = []
    for _ in range(num_days):
        meetings.append([])
        for t in np.linspace(0.4,0.6,num_meetings_per_day):
            p1, p2 = np.random.choice(range(num_people), 2, replace=False)
            meetings[-1].append((int(p1), int(p2), float(t)))

    return meetings


num_people = 4
num_days = 4
num_meetings_per_day = 1
infect_prob = 0.1
initial_infect_prob = 0.1
daily_healing_prob = 0.1
meetings = generate_meetings(num_days, num_people, num_meetings_per_day)

model = BayesianNetwork("SI")
people_list = []
pos = {}
edges = []

t1 = time()
# beginning of first day
for person in range(num_people):
    n = Node(DiscreteDistribution({'S': 1.0 - initial_infect_prob, 'I': initial_infect_prob}),
             name='X_{}_0'.format(person))
    people_list.append(n)
    model.add_node(n)
    pos[n.name] = (0, person)

for day in range(num_days):
    for meeting in meetings[day]:
        n1 = Node(
            ConditionalProbabilityTable(
                [
                    ['S', 'S', 'S', 1.0],
                    ['S', 'S', 'I', 0.0],
                    ['S', 'I', 'S', 1.0 - infect_prob],
                    ['S', 'I', 'I', infect_prob],
                    ['I', 'S', 'S', 0.0],
                    ['I', 'S', 'I', 1.0],
                    ['I', 'I', 'S', 0.0],
                    ['I', 'I', 'I', 1.0],
                ],
                [people_list[meeting[0]].distribution, people_list[meeting[1]].distribution]
            ),
            name='X_{}_{}'.format(meeting[0], day + meeting[2])
        )
        n2 = Node(
            ConditionalProbabilityTable(
                [
                    ['S', 'S', 'S', 1.0],
                    ['S', 'S', 'I', 0.0],
                    ['S', 'I', 'S', 1.0 - infect_prob],
                    ['S', 'I', 'I', infect_prob],
                    ['I', 'S', 'S', 0.0],
                    ['I', 'S', 'I', 1.0],
                    ['I', 'I', 'S', 0.0],
                    ['I', 'I', 'I', 1.0],
                ],
                [people_list[meeting[1]].distribution, people_list[meeting[0]].distribution]
            ),
            name='X_{}_{}'.format(meeting[1], day + meeting[2])
        )
        model.add_node(n1)
        pos[n1.name] = (day + meeting[2], meeting[0])
        model.add_node(n2)
        pos[n2.name] = (day + meeting[2], meeting[1])
        model.add_edge(people_list[meeting[0]], n1)
        edges.append((people_list[meeting[0]].name, n1.name))
        model.add_edge(people_list[meeting[1]], n1)
        edges.append((people_list[meeting[1]].name, n1.name))
        model.add_edge(people_list[meeting[1]], n2)  # TODO: check order of edges!!!
        edges.append((people_list[meeting[1]].name, n2.name))
        model.add_edge(people_list[meeting[0]], n2)
        edges.append((people_list[meeting[0]].name, n2.name))
        people_list[meeting[0]] = n1
        people_list[meeting[1]] = n2

    # propagate people to next day
    for person in range(num_people):
        n = Node(
            ConditionalProbabilityTable(
                [
                    ['S', 'S', 1.0],
                    ['S', 'I', 0.0],
                    ['I', 'S', daily_healing_prob],
                    ['I', 'I', 1.0 - daily_healing_prob]
                ],
                [people_list[person].distribution]
            ),
            name='X_{}_{}'.format(person, day + 1)
        )
        model.add_node(n)
        pos[n.name] = (day + 1, person)
        model.add_edge(people_list[person], n)
        edges.append((people_list[person].name, n.name))
        people_list[person] = n

model.bake()
elapsed = time()-t1
print('graph building time:  {} seconds'.format(elapsed))

t1 = time()
probs = model.predict_proba(
    {
        'X_0_0': DiscreteDistribution({'S': 0.0, 'I': 1.0}),
        'X_1_0': DiscreteDistribution({'S': 1.0, 'I': 0.0}),
        'X_2_0': DiscreteDistribution({'S': 1.0, 'I': 0.0}),
        'X_3_0': DiscreteDistribution({'S': 1.0, 'I': 0.0})
    },
    max_iterations=20,
    n_jobs=1,
    check_input=False
)
elapsed = time()-t1
print('predict probs time:  {} seconds'.format(elapsed))


for person, prob in enumerate(probs[-num_people:]):
    s = f'{person:<5d} : '
    if prob == 'S':
        s += '0.0'
    elif prob == 'I':
        s += '1.0'
    else:
        s += '{:.2f}'.format(prob.probability('I'))
    print(s)


labels = {}
for node, prob in zip(model.states, probs):
    labels[node.name] = '{:.2f}'.format(prob.probability('I'))

g = networkx.Graph(edges)
networkx.draw(g, pos, labels=labels, with_labels=True)
plt.show()






