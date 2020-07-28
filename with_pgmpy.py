from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models.ClusterGraph import ClusterGraph
import networkx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

num_people = 3
meetings = [[],[(0,1,0.5)],[(1,2,0.5)],[]]
tests = [[],[],[2],[]]

num_days = len(meetings)

graph = []
nodes = []
pos = {}
people_list = []
for i in range(num_people):
    n = TabularCPD('X_{}_0'.format(i), 2, [[0.9, 0.1]])
    nodes.append(n)
    pos[n.variable] = (0,i)
    people_list.append(n.variable)

for day in range(num_days):
    for meeting in meetings[day]:
        n1 = TabularCPD(
            variable='X_{}_{}'.format(meeting[0],day+meeting[2]),
            variable_card=2,
            evidence=[people_list[meeting[0]] , people_list[meeting[1]]],
            evidence_card=[2,2],
            values=[
                #SS   SI   IS   II
                [1.0, 0.9, 0.0, 0.0], #S
                [0.0, 0.1, 1.0, 1.0] #I
            ]
        )
        nodes.append(n1)
        pos[n1.variable] = (day+meeting[2], meeting[0])
        print(n1)
        n2 = TabularCPD(
            variable='X_{}_{}'.format(meeting[1],day+meeting[2]),
            variable_card=2,
            evidence=[people_list[meeting[1]] , people_list[meeting[0]]],
            evidence_card=[2,2],
            values=[
                #SS   SI   IS   II
                [1.0, 0.9, 0.0, 0.0], #S
                [0.0, 0.1, 1.0, 1.0] #I
            ]
        )
        nodes.append(n2)
        pos[n2.variable] = (day + meeting[2], meeting[1])
        graph.extend([
            (people_list[meeting[0]], n1.variable),
            (people_list[meeting[1]], n1.variable),
            (people_list[meeting[1]], n2.variable),
            (people_list[meeting[0]], n2.variable)
        ])
        people_list[meeting[0]] = n1.variable
        people_list[meeting[1]] = n2.variable

    for i in range(num_people):
        n = TabularCPD(
            variable='X_{}_{}'.format(i,day+1),
            variable_card=2,
            evidence=[people_list[i]],
            evidence_card=[2],
            values=[
                #S    I
                [1.0, 0.05], #S
                [0.0, 0.95] #I
            ]
        )
        nodes.append(n)
        pos[n.variable] = (day + 1, i)
        graph.append((people_list[i], n.variable))
        people_list[i] = n.variable

model = BayesianModel(graph)
model.add_cpds(*nodes)

observed_df = pd.DataFrame([{'X_2_4':1}])
preds_df = model.predict_probability(observed_df)
labels = preds_df.loc[0].to_dict()
labels = {k[:-2]:f'{v:.2f}' for k,v in labels.items() if k.endswith('_1')}

networkx.draw(model, pos, labels=labels, with_labels=True)
plt.show()