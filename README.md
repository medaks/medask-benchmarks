# SymptomCheck Bench


SymptomCheck Bench is an OSCE-style benchmark designed to evaluate the diagnostic accuracy of Large Language Model (LLM) based medical agents in symptom assessment conversations.

The benchmark simulates medical consultations through a structured four-step process:
1. Initialization: Selection of a clinical vignette
2. Dialogue: Simulated conversation between an LLM agent and patient
3. Diagnosis: Generation of top 5 differential diagnoses
4. Evaluation: Automated assessment of diagnostic accuracy

For more details about the benchmark, methodology, and results, read our blog post:
https://medask.tech/blogs/introducing-symptomcheck-bench/

* Results of our ICD-10 evaluation are also found in the results folder. For more information refer to:
https://medask.tech/blogs/how-medasks-cognitive-architecture-improves-icd-10-coding-accuracy/

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
python medask/benchmark/main.py

# Output
usage: main.py [-h] [--doctor_llm DOCTOR_LLM] [--patient_llm PATIENT_LLM]
               [--evaluator_llm EVALUATOR_LLM] --file {avey,agentclinic}
               [--num_vignettes NUM_VIGNETTES] [--num_experiments NUM_EXPERIMENTS]
               [--comment COMMENT] [--result_name_suffix RESULT_NAME_SUFFIX]
main.py: error: the following arguments are required: --file
```

#### Running a complex example.

##### Starting the script...
```
# Run the benchmark on 3 random vignettes from Avey. Repeat the experiment 2 times.
# Use gpt-4o for the LLM simulating the doctor.
# By default, gpt-4o-mini is used for the LLM simulating the patient.
# By default, gpt-4o is used to evaluate the correctness of the resulting diagnoses.

python medask/benchmark/main.py --file=avey --doctor_llm=gpt-4o  --num_vignettes=3 --num_experiments=2
```

##### ... generates the following output.
```
2024-10-28 21:52:59,084 - [INFO] - benchmark - Running experiment over vignettes [68, 166, 334]
2024-10-28 21:53:24,619 - [INFO] - benchmark - Dumping results to medask/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json

position=1      Nephrolithiasis : [Kidney stones, Ureteral obstruction, Urinary tract infection, Pyelonephritis, Renal colic]
position=1      Measles : [Measles, Viral exanthem, Roseola, Rubella, Scarlet fever]
position=1      Cerebral Stroke : [Ischemic stroke, Hemorrhagic stroke, Transient ischemic attack (TIA), Bell's palsy, Intracranial hemorrhage]

2024-10-28 21:53:27,234 - [INFO] - benchmark.evaluate - Results of run i=0
   positions=[1.0, 1.0, 1.0]
   Number of correct diagnoses: 3 / 3
   Average position of correct diagnosis: 1.0

position=1      Nephrolithiasis : [Kidney stones, Ureteral stones, Renal colic, Hematuria, Urinary tract obstruction]
position=1      Measles : [Measles, Viral exanthem, Rubella, Scarlet fever, Roseola]
position=1      Cerebral Stroke : [Acute Ischemic Stroke, Transient Ischemic Attack, Hemorrhagic Stroke, Bell's Palsy, Migraine with Aura]

2024-10-28 21:53:30,660 - [INFO] - benchmark.evaluate - Results of run i=1
   positions=[1.0, 1.0, 1.0]
   Number of correct diagnoses: 3 / 3
   Average position of correct diagnosis: 1.0
```

##### Understanding the output.
```
# You can see the indices of the vignettes that are used in the experiment.

2024-10-28 21:52:59,084 - [INFO] - benchmark - Running experiment over vignettes [68, 166, 334]
```

```
# All the data about the experiment is saved to disk, in this case to  medask/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json

2024-10-28 21:53:24,619 - [INFO] - benchmark - Dumping results to medask/benchmark/results/2024-10-28T21:52:59_gpt-4o_3.json
```


```
position=1      Nephrolithiasis : [Kidney stones, Ureteral obstruction, Urinary tract infection, Pyelonephritis, Renal colic]

# This shows the evaluation of the first diagnosis of the first experiment run.
#  * Nephrolithiasis (Kidney stones) was the correct diagnosis.
#  * [Kidney stones, Ureteral obstruction, Urinary tract infection, Pyelonephritis, Renal colic] Are the 5 most likely diagnoses the symptom #    checker agent decided upon
#  * position=1 Is the result of the evaluator LLM. It decided the correct diagnosis was found in position 1 in the differential diagnosis #    list

```

```
2024-10-28 21:53:27,234 - [INFO] - benchmark.evaluate - Results of run i=0
   positions=[1.0, 1.0, 1.0]
   Number of correct diagnoses: 3 / 3
   Average position of correct diagnosis: 1.0

# This shows the aggregated results of the first experiment run:
#  * For the first vignette, the evaluator thought that the first diagnosis is the correct one, hence 1.
#  * For the second vignette, the evaluator thought that the first diagnosis is the correct one, hence 1.
#  * For the third vignette, the evaluator thought that the first diagnosis is the correct one, hence 1.
# Overall, thus 3 / 3 diagnoses were correct, and the average position of the correct diagnoses is (1.0 + 1.0 + 1.0) / 3 = 1.0

```

### Inspect the results of a benchmark run.

```
Here you see how to read from disk the result of the benchmark you ran above.
```

![screenshot-2024-10-28_21:57:54](https://github.com/user-attachments/assets/e5abad75-e85d-451c-ba5c-e496522614de)

