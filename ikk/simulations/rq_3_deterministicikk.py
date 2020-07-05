# Import (abstract) Simulation class from Simulations.abstracted_simulation.py
from ikk.simulations.abstracted_simulation import Simulation

# Class DeterministicIKK implements (abstract) class Simulation
# The DeterministicIKK class is used to get an answer to RQ3 on whether the results obtained are better using another method to select
#   new states as compared results obtained using the IKK attack (by Islam et al.)
# In this class only specific parameters are set to ensure the simulation works as intended
class DeterministicIKK(Simulation):

    # During initialization of the DeterministicIKK class the deterministic_ikk global variable of the Simulation class is set to True
    # and the results_folder is changed to the once corresponding to the requested simulation
    def __init__(self):
        super(Simulation, self).__init__()
        self.deterministic_ikk = True
        self.results_folder = "RQ3-DeterministicIKK"

    # Method set_parameters sets specific parameters according to the input of the user on the command line
    # set_parameters is used to simulate different background knowledges
    def set_parameters(self, parameters):
        if parameters["document_percentage"] is not None:
            self.document_percentage = parameters["document_percentage"]
        elif parameters["keyword_percentage"] is not None:
            self.keyword_percentage = parameters["keyword_percentage"]
        elif parameters["background_knowledge_folder_name"] is not None:
            self.background_knowledge_folder_name = parameters[
                "background_knowledge_folder_name"
            ]
        elif parameters["gaussian_noise_constant"] is not None:
            self.gaussian_noise_constant = parameters["gaussian_noise_constant"]
