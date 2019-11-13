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
1.3. [References](#refs)

2. [Quantum Gate Array approach](#qga)

## <a name="qa">Quantum Annealer approach</a>

### <a name="prereqs">Prerequisites</a>

First of all you have to register to https://cloud.dwavesys.com .

Then you require an environment with the scripting language Python.

As an example with a Windows PC you can install the portable executables
(Zero Version) you can find here: http://winpython.github.io/ .

Once installed a Python environment you should be able to launch the following command: 

```
pip install dwave-ocean-sdk
```

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

The configuration can also be used from python. 
As an example, if you type the following lines at the python prompt:

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

### <a name="refs">References</a>

[OpenJij D-Wave Ocean SDK tutorial](https://openjij.github.io/OpenJijTutorial/_build/html/ja/4-DWaveOceanSDK.html)

[PyQubo graph coloring problem](https://github.com/recruit-communications/pyqubo/blob/master/notebooks/graph_coloring.ipynb)

### <a name="qga">Quantum Gate Array approach</a>
