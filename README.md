### Installation

   ```
   conda create -n benchmark python=3.12

   conda activate benchmark

   pip install -r requirements/development.txt
   pip install -e .

   export KEY_OPENAI="sk-..." # Set your API key in an ENV variable.
   ```

### Usage

#### Running the script

```
# By default uses gpt-4o-mini.
# Inspect the code for other options.
python medask/tools/benchmark/main.py --file=avey --doctor_llm=gpt-4o  --num_vignettes=3 --num_experiments=2

# Output
2024-10-28 21:52:59,084 - [INFO] - benchmark - Running experiment over vignettes [145, 193, 263]

2024-10-28 21:53:10,490 - [INFO] - benchmark.simulator - Function <simulate> took 11.4037 seconds.
2024-10-28 21:53:10,492 - [INFO] - benchmark.simulator - Function <simulate> took 11.3955 seconds.
2024-10-28 21:53:10,897 - [INFO] - benchmark.simulator - Function <simulate> took 11.7917 seconds.
2024-10-28 21:53:10,897 - [INFO] - benchmark - Function <run_experiment> took 11.8118 seconds.
2024-10-28 21:53:10,897 - [INFO] - benchmark - Dumping results to medask/tools/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json

2024-10-28 21:53:21,856 - [INFO] - benchmark.simulator - Function <simulate> took 10.9379 seconds.
2024-10-28 21:53:21,857 - [INFO] - benchmark.simulator - Function <simulate> took 10.9581 seconds.
2024-10-28 21:53:24,618 - [INFO] - benchmark.simulator - Function <simulate> took 13.7098 seconds.
2024-10-28 21:53:24,618 - [INFO] - benchmark - Function <run_experiment> took 13.7201 seconds.
2024-10-28 21:53:24,619 - [INFO] - benchmark - Dumping results to medask/tools/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json

positions=[-1, 1, 1]	Colonic Polyps	: [Colorectal polyps, Colorectal cancer, Diverticular disease]
positions=[-1, -1, -1]	Pseudogout	: [Rheumatoid arthritis, Reactive arthritis, Polyarticular gout]
positions=[1, 1, 1]	Unstable Angina	: [Angina, Acute Coronary Syndrome, Myocardial Infarction]

2024-10-28 21:53:27,234 - [INFO] - benchmark.evaluate - Results of run i=0
   positions=[1.0, -111, 1.0]
   Number of correct diagnoses: 2 / 3
   Average position of correct diagnosis: 1.0


positions=[3, 3, 3]	Colonic Polyps	: [hemorrhoids, anal fissure, colorectal polyps]
positions=[-1, -1, -1]	Pseudogout	: [Rheumatoid arthritis, Osteoarthritis, Gout]
positions=[2, 2, 2]	Unstable Angina	: [Angina pectoris, Unstable angina, Myocardial infarction]

2024-10-28 21:53:30,660 - [INFO] - benchmark.evaluate - Results of run i=1
   positions=[3.0, -111, 2.0]
   Number of correct diagnoses: 2 / 3
   Average position of correct diagnosis: 2.5
```

#### Inspect the results of a benchmark run.

![screenshot-2024-10-28_21:57:54](https://github.com/user-attachments/assets/e5abad75-e85d-451c-ba5c-e496522614de)

