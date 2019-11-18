# A practical essay on Quantum Computing available today 

In 2019 there have been astonishing announcements on QC,
but actually what can everyone already try?

This is the question to which you could find an answer here. 

Today in Quantum Computing there are two main altenatives:

1. the DWave quantum annealer https://cloud.dwavesys.com
2. the IBM quantum gate array https://quantum-computing.ibm.com

The first alternative is oriented to particular problems 
and could be easier to apply.

The second alternative could face up to a larger number of problems
and is the most promising.

# Table of Contents

1. [Quantum Annealer approach](#qa)

1.1. [Prerequisites](#prereqs)

1.2. [D-Wave configuration](#dwconf)

1.3. [Graph coloring problem](#gcp)

1.4. [References](#refs)

2. [Quantum Gate Array approach](#qga)

## <a name="qa">Quantum Annealer approach</a>

Quantum Annealer allows to solve problems with variables that can be associated to a 
quadratic polynomial and a solution is found giving to the variables a set of values 
that minimize such a polynomial.

A problem of this kind is the Map Coloring Problem in which you have 
to map a state painting regions without using the same color for adjacent regions.
This problem can be represented as a Graph Coloring Problem if you think 
to regions as graph vertices and to adjacencies as graph edges. 

### <a name="prereqs">Prerequisites</a>

First of all you have to register to https://cloud.dwavesys.com .

Then you require an environment with the scripting language Python.

As an example with a Windows PC you can install the portable executables
(Zero Version) you can find here: http://winpython.github.io .

Once installed a Python environment you should be able to launch the following command: 

```
pip install dwave-ocean-sdk
pip install matplotlib
```

The matplotlib is suggested only to better understand results visualizing them.

### <a name="dwconf">D-Wave configuration</a>

Having installed per dwave-ocean-sdk you can launch the following command:

```
dwave config create
```

that ask you a few questions as in the example that follows:

```
Configuration file not found; the default location is: C:\Users\User\AppData\Local\dwavesystem\dwave\dwave.conf
Configuration file path [C:\Users\User\AppData\Local\dwavesystem\dwave\dwave.conf]:
Profile (create new) [prod]:
API endpoint URL [skip]: https://cloud.dwavesys.com/sapi
Authentication token [skip]: <copy API token from https://cloud.dwavesys.com/leap/>
Default client class (qpu or sw) [qpu]:
Default solver [skip]: DW_2000Q_2_1
Configuration saved.
```

Now you can check your connection to the quantum annealer with the following command:

```
dwave ping
```

that should return something like this:

```
Using endpoint: https://cloud.dwavesys.com/sapi
Using solver: DW_2000Q_2_1
Submitted problem ID: 5423d6ce-d469-4f28-af6e-6c47a5b4e549

Wall clock time:
 * Solver definition fetch: 1907.458 ms
 * Problem submit and results fetch: 6325.260 ms
 * Total: 8232.718 ms

QPU timing:
 * qpu_sampling_time = 164 us
 * qpu_anneal_time_per_sample = 20 us
 * qpu_readout_time_per_sample = 123 us
 * qpu_access_time = 7709 us
 * qpu_access_overhead_time = 556 us
 * qpu_programming_time = 7545 us
 * qpu_delay_time_per_sample = 21 us
 * total_post_processing_time = 230 us
 * post_processing_overhead_time = 230 us
 * total_real_time = 7709 us
 * run_time_chip = 164 us
 * anneal_time_per_run = 20 us
 * readout_time_per_run = 123 us
```

Ping requires about 0.01 seconds of the free minute per month you have. 
Alternative responses explain you the reason of the failure such as a time exhaustion. 

The configuration can also be used from Python. 
As an example, if you type the following lines at the Python prompt:

```
from dwave.cloud import Client
client = Client.from_config()
client.get_solvers()
```

you should receive back something like that: 

```
[StructuredSolver(id='DW_2000Q_2_1'), StructuredSolver(id='DW_2000Q_5')]
```

Moreover if you type the following lines:

```
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler()
sampler.parameters
```

you should receive back something like that: 

```
{'num_reads': ['parameters'], 'answer_mode': ['parameters'], 'max_answers': ['parameters'], 'auto_scale': ['parameters'], 'annealing_time': ['parameters'], 'beta': ['parameters'], 'chains': ['parameters'], 'num_spin_reversal_transforms': ['parameters'], 'postprocess': ['parameters'], 'programming_thermalization': ['parameters'], 'readout_thermalization': ['parameters'], 'anneal_offsets': ['parameters'], 'anneal_schedule': ['parameters'], 'initial_state': ['parameters'], 'reinitialize_state': ['parameters'], 'flux_biases': ['parameters'], 'reduce_intersample_correlation': ['parameters'], 'flux_drift_compensation': ['parameters'], 'h_gain_schedule': ['parameters']}
```

### <a name="gcp">Graph Coloring Problem</a>

From Python prompt you can initially import the libraries to use.

```
import random
import matplotlib.pyplot as plt
import networkx as nx
from pyqubo import Array, Placeholder, solve_qubo, Constraint, Sum
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from util_test import make_rnd_graph, plot_graph, get_qubo, get_colors, check_result, get_solution
```

Last import includes the functions shown hereafter.
Now define the number of vertices N, the colors and 
set a seed for random numbers
allowing you to repeat the same experiment:

```
N=25
palette=['red', 'green', 'blue', 'gray']
K=len(palette)
random.seed(42)
``

Now you can define a function
to create random graphs with a given number of
maximum neighbors:

```
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
```

Having installed networkx and matplotlib you can show the graph as follows:

```
def plot_graph(num_nodes, edges, colors, palette):
  G = nx.Graph()
  G.add_nodes_from([n for n in range(num_nodes)])
  for (i, j) in edges:
    G.add_edge(i, j)
  plt.figure(figsize=(4,4))
  nx.draw_networkx(G, nx.circular_layout(G), node_color=[palette[colors[i]] for i in G.nodes])
  plt.show()
```

Resuming you can now define and plot a graph:

```
E, clrs = make_rnd_graph(N, K, K+2)
plot_graph(N, E, clrs, palette)
```

To avoid that the extremes of an edge have the same color,
you can evaluate the configuration to give to quantum annealer.

First of all you have to define a binary matrix 
whose rows represent vertices and columns represent colors. 
Then you can define the polynomial to minimize (hamiltonian) with the constraints
that no adjacent nodes are colored with the same color,
and that every vertex is colored with just one color:

```
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
```

This function also returns a simulated solution and its result 
can be found with this function:

```
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
```

Finally you can check the result with this function:

```
def check_result(edges, colors):
  for (i, j) in edges:
    if colors[i] == colors[j]:
      print("Nodes {} and {} are connected and have the same color".format(i, j))
```

Resuming you can evaluate the qubo, simulate the annealing and check the result as follows:

```
qubo, sim_sol = get_qubo(N, K, E)
sim_clrs = get_colors(sim_sol, N, K)
check_result(E, sim_clrs)
plot_graph(N, E, sim_clrs, palette)
```

Now let see what happens giving the QUBO model to the quantum annealer
(proxy parameter required only behind a firewall):

```
sampler = EmbeddingComposite(DWaveSampler(proxy='http://127.0.0.1:3128'))
response = sampler.sample_qubo(qubo, num_reads=10)
```

If the problem is to big for the quantum annealer you get "no embedding found".

Now you can retrieve the best solution from the following function:

```
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
```

such that you can compare with the simulated result as follows:

```
qa_sol = get_solution(response, N, K)
qa_clrs = get_colors(qa_sol, N, K)
check_result(E, qa_clrs)
plot_graph(N, E, qa_clrs, palette)
```

### <a name="refs">References</a>

[OpenJij D-Wave Ocean SDK tutorial](https://openjij.github.io/OpenJijTutorial/_build/html/ja/4-DWaveOceanSDK.html)

[PyQubo graph coloring problem](https://github.com/recruit-communications/pyqubo/blob/master/notebooks/graph_coloring.ipynb)

### <a name="qga">Quantum Gate Array approach</a>
