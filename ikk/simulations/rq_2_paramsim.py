# Import (abstract) Simulation class from Simulations.abstracted_simulation.py
from ikk.simulations.abstracted_simulation import Simulation

# Class ParamSim implements (abstract) class Simulation
# The ParamSim class is used to get an answer to RQ2 on the correlation between results obtained and the following input parameters:
# - Initial temperature
# - Cool down rate
# - Rejection rate
# - Dataset (ENRON/ApacheLucene-java-user)
# - The sub folders used in the datasets (ENRON: inbox/_sent_mail, ApacheLucene-java-user: mbox)
# In this class the set_parameters method of the Simulation class is re-implemented to set specific parameters to ensure the simulation works as intended
class ParamSim(Simulation):

    # During initialization of the ParamSim class the results_folder is changed to the once corresponding to the requested simulation
    def __init__(self):
        super(Simulation, self).__init__()
        self.results_folder = "RQ2-ParamSim"

    # Method set_parameters sets specific parameters according to the input of the user on the command line
    def set_parameters(self, parameters):
        self.initial_temperature = parameters["init_temp"]
        self.cool_down_rate = parameters["cool_down_rate"]
        self.reject_rate = parameters["reject_rate"]
        self.dataset = parameters["dataset"]
        if self.dataset == "ApacheLucene-java-user":
            self.server_knowledge_folder_name = "mbox"
            self.background_knowledge_folder_name = "mbox"
