# Import (abstract) Simulation class from Simulations.abstracted_simulation.py
from ikk.simulations.abstracted_simulation import Simulation

# Class CoocSim is used to answer RQ1 regarding the correlation between the input cooccurrence matrices and the scores obtained
# In this class the set_parameters method of the Simulation class is re-implemented to set specific parameters to ensure the simulation works as intended
class CoocSim(Simulation):

    # During initialization of the CoocSim class the results_folder is changed to the once corresponding to the requested simulation
    def __init__(self):
        super(Simulation, self).__init__()
        self.results_folder = "RQ1-CoocSim"

    # Method set_parameters sets specific parameters according to the input of the user on the command line
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
