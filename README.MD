IKK Query Recovery Attack
=========================

## Project Structure

```
ikk (project root)
├── Datasets
│   ├── ApacheLucene-java-user
│   │   └── Different email users
│   │       └── mbox
│   └── ENRON
│       └── Different email users
│           ├── _sent_mail
│           ├── inbox
│           └── etc.
│
├── ikk (Python package)
│   ├── simulations (Python package)
│   │   ├── abstracted_simulation.py    
│   │   ├── rq_1_coocsim.py            
│   │   ├── rq_2_paramsim.py
│   │   ├── rq_3_deterministicikk.py
│   │   ├── rq_4_multipleruns.py
│   │   ├── rq_5_query_dist.py
│   │   └── etc.
│   │
│   ├── dataset_extraction.py           
│   ├── distribution.py
│   ├── ikk.py
│   ├── matrix_generation.py
│   ├── params.py
│   ├── read_write.py
│   ├── send_mail.py
│   ├── similarity_calculation.py
│   └── word_extraction.py
│
├── Results
│   ├── RQ1-CoocSim
│   ├── RQ2-ParamSim
│   ├── RQ3-DeterministicIKK
│   ├── RQ4-MultipleRuns
│   ├── RQ5-QueryDist
│   ├── etc.
│   └── Test
│
├── StemmedDatasets
│
├── test (Python package)
│   ├── Apache_test_file
│   ├── ENRON_test_file
│   ├── test_dataset_extraction.py
│   ├── test_ikk.py
│   ├── test_matrix_generation.py
│   ├── test_similarity_calculation.py
│   └── test_word_extraction.py
│
├── config.py
├── main.py
├── Apache_dataset_crawler.py
├── READ.ME
└── requirements.txt
```

### Explanation
The project root contains the following folders/files:
* ```Datasets``` contains the Apache and ENRON datasets
* ```ikk``` contains specific methods to simulate input data and execute the IKK attack (Python package)
   * ```simulations``` - Contains an abstract method that incorporates a single attack run and simulations specific methods that implement the abstract method and set simulation specific parameters in a certain manner (Python package). A new simulation (with specific parameters) is added easily, by:
      1) Adding a simulation file in the ```simulations``` package
      2) Creating a corresponding folder in the ```Results``` folder (and add a ```placeholder``` file, so git sees the folder if applicable)
      3) Adding the simulation in ```main.py``` and specific parameters in ```params.py```
      4) You might also want to add a test method in ```test```
   * ```dataset_extraction.py``` extracts word occurrences per file (according to simulation specific parameters) from a dataset
   * ```distribution.py``` contains an Enum containing different distributions to select queries
   * ```ikk.py``` implements the IKK implementation as proposed by Islam et al. in their paper [1]
   * ```matrix_generation.py``` generates inverted indices and cooccurrence matrices from word occurrences per file lists (as generated in ```dataset_extraction.py```)
   * ```params.py``` reads user input from the command line and allows the user to input simulation specific parameters and their values
   * ```read_write.py``` writes/reads .json structured result files to/from specific result folders
   * ```send_mail.py``` (optional) allows the user to choose whether to send emails containing the results of a simulation to a specific mail address (specified in config.py)
   * ```similarity_calculation.py``` calculates the similarity between two matrices, used for finding a correlation between the input matrices of the IKK attack and the results obtained
   * ```word_extraction.py``` processes and stems the words of a single (email) file
* ```Results``` contains folders for each simulation so simulation results can be found easily. When adding a new simulation (folder) you might want to add a ```placeholder``` file in that new folder so .git sees it). The ```Test``` folder contains test simulation results which are invoked by the test method in one of the simulations
* ```StemmedDatasets``` can contain datasets which were already extracted/stemmed as this process can be quite lengthy for large(r) dataset. ```dataset_extraction.py``` by default saves a specific extracted dataset and reuses that dataset the next simulation
* ```test``` contains two test files (used by ```test_word_extraction.py```) to simulate emails of respectively the ENRON/ApacheLucene-java-user dataset and 5 test files corresponding to the files in the ```ikk``` folder.
* ```config.py``` contains system specific parameters
* ```main.py``` is the main instance of the system
* ```Apache_dataset_crawler.py``` scrapes the Apache Lucene project's mail archive website for the ApacheLucene-java-user dataset
* ```READ.ME``` (You are here)
* ```requirements.txt``` contains all (external) Python(3) libraries used in the system

## Installation/Deployment
1) The project uses Python 3.6 (you might want to install a virtual environment to run the simulations)
2) Set the correct system parameters in config.py
3) To install the required libraries run (in the virtual environment): ```$ pip3 install -r requirements.txt```

## Execution
1) Run a simulation by running: ```$ python3 main.py```
   You might encounter problems as the settings in config.py are not correct
2) The user is asked whether to run a test instance or not (Y(es)/N(o))
   A test instance in this case means the parameters of simulations are set to very low settings and thus the simulation won't take long (but also won't give good results)
3) The user is asked which simulation to run, options are:
   1) C(o-ccurrence similarity)  --> runs the simulation in package ```ikk.simulations.rq_1_coocsim.py```
   2) P(arameter similiarity)    --> runs the simulation in ```ikk.simulations.rq_2_paramsim.py```
   3) D(eterministic IKK)        --> runs the simulation in ```ikk.simulations.rq_3_deterministicikk.py```
   4) M(ultiple Runs)            --> runs the simulation in ```ikk.simulations.rq_4_multipleruns.py```
   5) Q(uery Dist)               --> runs the simulation in ```ikk.simulations.rq_5_querydist.py```
4) Depending on the chosen simulation the user might have to input simulation specific parameters and their values (specified in ```params.py```)
5) Runs can also be executed on an external server, meaning that the code contains almost no print statements as this fails the process on an external server if the terminal the simulation was started on was closed and thus the simulation has no location to print to. However, if you want to print to the terminal you can change the debug mode in ```config.py```. In order to run the simulation on an external server (and be able to disconnect the terminal) you simply have to:
   1) Run the program normally and wait until you see the message 'NORMAL RUN' or 'TEST RUN'
   2) ```$ CTRL + Z``` pauses the current process running in the terminal
   3) ```$ disown -h $X``` disconnects the paused process with id X from the current terminal (```X``` is usually 1)
   4) ```$ bg``` runs the process in the background
   5) You can now close the connection to the external server

## Testing
- Tests are located in the ```test``` folder
- All tests assume their working directory to be the project root (ikk)
- The tests can be executed together using the command (in the project root): ```$ python3 -m unittest discover```

## Acknowledgements
Most of this work is based on the following papers:
1) [Access Pattern Disclosure on Searchable Encryption: Ramification, Attack and Mitigation, Islam et al., 2012](https://www.ndss-symposium.org/ndss2012/ndss-2012-programme/access-pattern-disclosure-searchable-encryption-ramification-attack-and-mitigation/)
2) [Leakage-Abuse attacks on Searchable Encryption, Cash et al., 2016](https://eprint.iacr.org/2016/718)

## Datasets used
1) [ENRON dataset (May 7, 2015 version)](https://www.cs.cmu.edu/~enron/), data re-arranged to fit data structure. Note, email names end in a '.', which is not Windows compatible. This project does not contain a method to rename all files ending in a '.'.
2) [Apache dataset](http://mail-archives.apache.org/mod_mbox/lucene-java-user/), retrieved using ikk.Apache_dataset_crawler.py for all mails from 2001 till August 2011 (August not included)
