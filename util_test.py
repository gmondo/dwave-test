import random
import matplotlib.pyplot as plt
import networkx as nx
from pyqubo import Array, Placeholder, solve_qubo, Constraint, Sum

def make_rnd_graph(num_nodes, num_colors, max_near):
  edges = []
  colors = []
  for i in range(num_nodes):
    colors.append(random.randint(0, num_colors - 1))
    j = 0
    for k in range(i + 1, num_nodes):
       if random.randint(0, 1) == 0:
         edges.append((i, k))
         j += 1
         if j == max_near:
           break
  return edges, colors

def plot_graph(num_nodes, edges, colors, palette):
  G = nx.Graph()
  G.add_nodes_from([n for n in range(num_nodes)])
  for (i, j) in edges:
    G.add_edge(i, j)
  plt.figure(figsize=(4,4))
  nx.draw_networkx(G, nx.circular_layout(G), node_color=[palette[colors[i]] for i in G.nodes])
  plt.show()

def get_qubo(num_nodes, num_colors, edges):
  x = Array.create('x', (num_nodes, num_colors), "BINARY")
  adjacent_const = 0.0
  for (i, j) in edges:
    for k in range(num_colors):
      adjacent_const += Constraint(x[i, k] * x[j, k], label="adjacent({},{})".format(i, j))
  onecolor_const = 0.0
  for i in range(num_nodes):
    onecolor_const += Constraint((Sum(0, num_colors, lambda j: x[i, j]) - 1)**2, label="onecolor{}".format(i))
  # combine the two components 
  alpha = Placeholder("alpha")
  H = alpha * onecolor_const + adjacent_const
  model = H.compile()
  alpha = 1.0
  # search for an alpha for which each node has only one color
  print("Broken constraints")
  while True:
    qubo, offset = model.to_qubo(feed_dict={"alpha": alpha})
    solution = solve_qubo(qubo)
    decoded_solution, broken_constraints, energy = model.decode_solution(solution, vartype="BINARY", feed_dict={"alpha": alpha})
    print(len(broken_constraints))
    if not broken_constraints:
      break
    for (key, value) in broken_constraints.items():
      if 'o' == key[0]: # onecolor
        alpha += 0.1
        break
    if 'a' == key[0]: # adjacent
      break
  return qubo, decoded_solution

def get_colors(solution, num_nodes, num_colors):
  colors = [0 for i in range(num_nodes)]
  for i in range(num_nodes):
    for k in range(num_colors):
      found = False
      if solution['x'][i][k] == 1:
        if found:
          print("Multiple colors assigned to node ", i)
          break
        else:
          colors[i] = k
          found = True
      if k == num_colors and not found:
          print("No color assigned to node ", i)
  return colors

def check_result(edges, colors):
  for (i, j) in edges:
    if colors[i] == colors[j]:
      print("Nodes {} and {} are connected and have the same color".format(i, j))

def get_solution(qa_res, num_nodes, num_colors):
  energy = float("inf")
  qa_sol = {}
  for datum in qa_res.data(["energy", "sample"]):   
    print(datum.energy)
    if datum.energy < energy:
      energy = datum.energy
      qa_sol = datum.sample 
  res = {}
  x_val = {}
  for i in range(num_nodes):
    node_val = {}
    for k in range(num_colors):
      node_val[k] = qa_sol['x['+str(i)+']['+str(k)+']']
    x_val[i] = node_val
  res['x'] = x_val
  return res 
