# Import (abstract) Simulation class from Simulations.abstracted_simulation.py
from ikk.simulations.abstracted_simulation import Simulation

# Class MultipleRuns implements (abstract) class Simulation
# The MultipleRuns class is used to get an answer to RQ4 on whether the results of different simulations on the same input matrices can
#   be combined to increase the overall score
# In this class the set_parameters method of the Simulation class is re-implemented to set specific parameters to ensure the simulation works as intended
class MultipleRuns(Simulation):

    # During initialization of the MultipleRuns class the results_folder is changed to the once corresponding to the requested simulation
    def __init__(self):
        super(Simulation, self).__init__()
        self.results_folder = "RQ4-MultipleRuns"

    # Method set_parameters sets specific parameters according to the input of the user on the command line
    def set_parameters(self, parameters):
        self.num_runs = parameters["num_runs"]
