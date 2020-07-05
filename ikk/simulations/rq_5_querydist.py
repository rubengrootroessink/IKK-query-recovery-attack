# Import (abstract) Simulation class from Simulations.abstracted_simulation.py
from ikk.simulations.abstracted_simulation import Simulation

# Class QueryDistribution implements (abstract) class Simulation
# The QueryDistribution class is used to get an answer to RQ5 on whether the results obtained are different using another method to simulate the queries
#   in the IKK attack
# This question is posed as we do not necessarily agree that the Zipfian distribution is the most logical choice for query selection as we believe
#   users tend to search more for words that occur less in a dataset rather than more as they might not want large results sets,
#   but prefer limited result sets
# In this class only specific parameters are set to ensure the simulation works as intended
class QueryDistribution(Simulation):

    # During initialization of the QueryDistribution class the results_folder is changed to the once corresponding to the requested simulation
    def __init__(self):
        super(Simulation, self).__init__()
        self.results_folder = "RQ5-QueryDist"

    # Method set_parameters sets specific parameters according to the input of the user on the command line
    def set_parameters(self, parameters):
        self.query_distribution = parameters["query_distribution"]
