## A novel approach to evaluating AI agents on diagnostic accuracy in symptom checking tasks.


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

##### Inspecting the available script options.
```
# Run without any arguments to see all available options.
python medask/tools/benchmark/main.py

# Output
usage: main.py [-h] [--doctor_llm DOCTOR_LLM] [--patient_llm PATIENT_LLM]
               [--evaluator_llm EVALUATOR_LLM] --file {avey,agentclinic}
               [--num_vignettes NUM_VIGNETTES] [--num_experiments NUM_EXPERIMENTS]
               [--comment COMMENT] [--result_name_suffix RESULT_NAME_SUFFIX]
main.py: error: the following arguments are required: --file
```

#### Running a complex example.

##### Starting the script.
```
# Run the benchmark on 3 random vignettes from Avey. Repeat the experiment 2 times.
# Use gpt-4o for the LLM simulating the doctor.
# By default, gpt-4o-mini is used for the LLM simulating the patient.
# By default, gpt-4o is used to evaluate the correctnes of the resulting diagnoses.
python medask/tools/benchmark/main.py --file=avey --doctor_llm=gpt-4o  --num_vignettes=3 --num_experiments=2

# Output
2024-10-28 21:52:59,084 - [INFO] - benchmark - Running experiment over vignettes [145, 193, 263]
...
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

##### Understanding the output
```
# You can see the indices of the vignettes that are used in the experiment.
2024-10-28 21:52:59,084 - [INFO] - benchmark - Running experiment over vignettes [145, 193, 263]
```

```
# All the data about the experiment is saved to disk, in this case to  medask/tools/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json
2024-10-28 21:53:24,619 - [INFO] - benchmark - Dumping results to medask/tools/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json
```


```
# This shows the evaluation of the first diagnosis of the first experiment run.
#  * Colonic Polyps was the correct diagnosis.
#  * [Colorectal polyps, Colorectal cancer, Diverticular disease] Are the 3 most likely diagnoses the doctor LLM decided upon
#  * positions=[-1, 1, 1] Is the result of the evaluator LLM. We run it 3 times for each diagnosis prediction.
#        In the first run, the evaluator thought none of the 3 given diagnoses is close enough to the correct one, hence -1.
#        In the second run, the evaluator thought the first diagnosis (Colorectal polyps) is close enough to the correct one, hence 1.
#        In the third run, the evaluator thought the first diagnosis (Colorectal polyps) is close enough to the correct one, hence 1.
positions=[-1, 1, 1]	Colonic Polyps	: [Colorectal polyps, Colorectal cancer, Diverticular disease]
```

```
# This shows the aggregated results of the first experiment run:
#  * For the first diagnosis, the evaluator thought that the first diagnosis is the correct one, hence 1.
#  * For the second diagnosis, the evaluator thought that all diagnoses were incorrect, hence -111.
#  * For the third diagnosis, the evaluator thought that the first diagnosis is the correct one, hence 1.
# Overall, thus 2 / 3 diagnoses were correct, and the average position of the correct diagnoses is (1.0 + 1.0) / 2 = 1.0
2024-10-28 21:53:27,234 - [INFO] - benchmark.evaluate - Results of run i=0
   positions=[1.0, -111, 1.0]
   Number of correct diagnoses: 2 / 3
   Average position of correct diagnosis: 1.0
```

### Inspect the results of a benchmark run.

```
Here you see how to read from disk the result of the benchmark you ran above.
```

![screenshot-2024-10-28_21:57:54](https://github.com/user-attachments/assets/e5abad75-e85d-451c-ba5c-e496522614de)

