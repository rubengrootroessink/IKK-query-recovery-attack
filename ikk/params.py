# Imports Enum QueryDistribution
from ikk.distribution import QueryDistribution

# Class Params is used in main.py to ask the user for simulation specific parameters on the command line
# This makes it easy for a user to change inputs without having to change files
# The selection of the parameter menu is based on the name of the simulation
# New simulations can be easily added by creating a new file menu and adding the simulation name in the get_params method
class Params:

    # Global variable params is initially empty and filled according to the requirements of different simulations
    params = {}

    # Method get_params is used to select the parameter selection menu based on the simulation name
    def get_params(self, simulation_name):
        if simulation_name == "RQ1-CoocSim":  # RQ1
            self.get_rq_1_coocsim_params()
        elif simulation_name == "RQ2-ParamSim":  # RQ2
            self.get_rq_2_paramsim_params()
        elif simulation_name == "RQ3-DeterministicIKK":  # RQ3
            self.get_rq_3_deterministicikk_params()
        elif simulation_name == "RQ4-MultipleRuns":  # RQ4
            self.get_rq_4_multipleruns_params()
        elif simulation_name == "RQ5-QueryDist":  # RQ5
            self.get_rq_5_querydist_params()
        return self.params

    # Method get_rq_1_coocsim_params asks the user to input parameters for the RQ1-CoocSim simulation
    # This RQ tries to find whether there exists a correlation between the similarity of the input matrices of the IKK algorithm and the results obtained
    # The method asks the user to input specific parameters based on the following selection menu:
    # 1) Document percentage -> Simulates a setting where the full background knowledge is not known to the adversary, documents are deleted according to
    #   the document_percentage parameter
    #   - Only the document_percentage parameter is set to a value between 0 and 1 whereas keyword_percentage, background_knowledge_folder_name and
    #     gaussian_noise_constant are set to None
    # 2) Keyword percentage -> Simulates a setting where the full background knowledge is not known to the adversary, keywords are deleted according to
    #   the keyword_percentage parameter
    #   - Only the keyword_percentage parameter is set to a value between 0 and 1 whereas document_percentage, background_knowledge_folder_name and
    #     gaussian_noise_constant are set to None
    # 3) Input folder -> Simulates a setting where the full background knowledge is not known to the adversary, this knowledge is estimated by
    #   taking another folder containing files
    #   - Only the background_knowledge_folder_name parameter is set to the non-standard folder 'inbox' of the ENRON dataset,
    #     where all other simulations use the '_sent_mail' folder
    #   - document_percentage, keyword_percentage and gaussian_noise_constant are set to None
    # 4) Gaussian noise -> Simulates a setting where the full background knowledge is not known to the adversary,
    #   by adding noise to the actual full background knowledge
    #   - Only the gaussian_noise_constant parameter is set (usually between 0 and 1, but can be higher than 1, variable taken from the paper by IKK et al.)
    #   - document_percentage, keyword_percentage and background_knowledge_folder remain set to None
    # Keep in mind that these values are not necessarily represented in the actual simulation as values set to None are (usually) disregarded and set to
    #   their default setting
    def get_rq_1_coocsim_params(self):
        document_percentage = None
        keyword_percentage = None
        background_knowledge_folder_name = None
        gaussian_noise_constant = None
        while True:
            try:
                question = "Co-occurrence similarity setting?\n"
                question += "\t1) D(ocument percentage)\n"
                question += "\t2) K(eyword percentage)\n"
                question += "\t3) I(nput folder)\n"
                question += "\t4) G(aussian noise)\n"
                question += "[D/K/I/G]: "
                choice = str(input(question)).lower()
                if choice == "d":
                    while True:
                        try:
                            document_percentage = float(
                                input("Document percentage? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for document_deletion_percentage is not a float. Try again!"
                            )
                    break
                elif choice == "k":
                    while True:
                        try:
                            keyword_percentage = float(
                                input("Keyword percentage? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for keyword_deletion_percentage is not a float. Try again!"
                            )
                    break
                elif choice == "i":
                    background_knowledge_folder_name = "inbox"
                    break
                elif choice == "g":
                    gaussian_noise_constant = True
                    while True:
                        try:
                            gaussian_noise_constant = float(
                                input("Gaussian noise constant? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for gaussian noise constant is not a float. Try again!"
                            )
                    break
            except:
                print(
                    "Error! The value you entered for the setting is not correct. Try again!"
                )
        self.params["document_percentage"] = document_percentage
        self.params["keyword_percentage"] = keyword_percentage
        self.params[
            "background_knowledge_folder_name"
        ] = background_knowledge_folder_name
        self.params["gaussian_noise_constant"] = gaussian_noise_constant

    # Method get_rq_2_paramsim_params asks the user to input parameters necessary for the RQ2-ParamSim simulation
    # This RQ tries to find whether there exists a correlation between the input parameters
    #   (init_temp, cool_down_rate, reject_rate and dataset) and the results obtained
    def get_rq_2_paramsim_params(self):
        init_temp = 1
        cool_down_rate = 0.999
        reject_rate = 50000
        dataset = "ENRON"
        while True:
            try:
                init_temp = float(input("Initial temperature? (float): "))
            except ValueError:
                print(
                    "Error! The value you entered for initial temperature is not a float. Try again!"
                )
            else:
                break
        while True:
            try:
                cool_down_rate = float(input("Cool down rate? (float): "))
            except ValueError:
                print(
                    "Error! The value you entered for cool down rate is not a float. Try again!"
                )
            else:
                break
        while True:
            try:
                reject_rate = int(input("Rejection rate? (int): "))
            except ValueError:
                print(
                    "Error! The value you entered for rejection rate is not an integer. Try again!"
                )
            else:
                break
        while True:
            try:
                choice = str(
                    input("Dataset choice? ApacheLucene-java-user or ENRON [A/E]: ")
                ).lower()
                if choice == "a":
                    dataset = "ApacheLucene-java-user"
                    break
                elif choice == "e":
                    dataset = "ENRON"
                    break
            except Exception as e:
                print("The value you entered is not correct. Please try again!")
        self.params["init_temp"] = init_temp
        self.params["cool_down_rate"] = cool_down_rate
        self.params["reject_rate"] = reject_rate
        self.params["dataset"] = dataset
    
    # Method get_rq_3_deterministic_ikk params asks the user to input parameters for the RQ3-DeterministicIKK simulation
    # This RQ tries to find whether the proposed 'Deterministic IKK' method delivers better results than the original IKK method as proposed by IKK et al.
    # The method asks the user to input specific parameters based on the following selection menu:
    # 1) Document percentage -> Simulates a setting where the full background knowledge is not known to the adversary, documents are deleted according to
    #   the document_percentage parameter
    #   - Only the document_percentage parameter is set to a value between 0 and 1 whereas keyword_percentage, background_knowledge_folder_name and
    #     gaussian_noise_constant are set to None
    # 2) Keyword percentage -> Simulates a setting where the full background knowledge is not known to the adversary, keywords are deleted according to
    #   the keyword_percentage parameter
    #   - Only the keyword_percentage parameter is set to a value between 0 and 1 whereas document_percentage, background_knowledge_folder_name and
    #     gaussian_noise_constant are set to None
    # 3) Input folder -> Simulates a setting where the full background knowledge is not known to the adversary, this knowledge is estimated by
    #   taking another folder containing files
    #   - Only the background_knowledge_folder_name parameter is set to the non-standard folder 'inbox' of the ENRON dataset,
    #     where all other simulations use the '_sent_mail' folder
    #   - document_percentage, keyword_percentage and gaussian_noise_constant are set to None
    # 4) Gaussian noise -> Simulates a setting where the full background knowledge is not known to the adversary,
    #   by adding noise to the actual full background knowledge
    #   - Only the gaussian_noise_constant parameter is set (usually between 0 and 1, but can be higher than 1, variable taken from the paper by IKK et al.)
    #   - document_percentage, keyword_percentage and background_knowledge_folder remain set to None
    # Keep in mind that these values are not necessarily represented in the actual simulation as values set to None are (usually) disregarded and set to
    #   their default setting
    def get_rq_3_deterministicikk_params(self):
        document_percentage = None
        keyword_percentage = None
        background_knowledge_folder_name = None
        gaussian_noise_constant = None
        while True:
            try:
                question = "Deterministic IKK setting?\n"
                question += "\t1) D(ocument percentage)\n"
                question += "\t2) K(eyword percentage)\n"
                question += "\t3) I(nput folder)\n"
                question += "\t4) G(aussian noise)\n"
                question += "[D/K/I/G]: "
                choice = str(input(question)).lower()
                if choice == "d":
                    while True:
                        try:
                            document_percentage = float(
                                input("Document percentage? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for document_deletion_percentage is not a float. Try again!"
                            )
                    break
                elif choice == "k":
                    while True:
                        try:
                            keyword_percentage = float(
                                input("Keyword percentage? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for keyword_deletion_percentage is not a float. Try again!"
                            )
                    break
                elif choice == "i":
                    background_knowledge_folder_name = "inbox"
                    break
                elif choice == "g":
                    gaussian_noise_constant = True
                    while True:
                        try:
                            gaussian_noise_constant = float(
                                input("Gaussian noise constant? (float): ")
                            )
                            break
                        except ValueError:
                            print(
                                "Error! The value you entered for gaussian noise constant is not a float. Try again!"
                            )
                    break
            except:
                print(
                    "Error! The value you entered for the setting is not correct. Try again!"
                )
        self.params["document_percentage"] = document_percentage
        self.params["keyword_percentage"] = keyword_percentage
        self.params[
            "background_knowledge_folder_name"
        ] = background_knowledge_folder_name
        self.params["gaussian_noise_constant"] = gaussian_noise_constant

    # Method get_rq_4_multipleruns_params asks the user to input the num_runs parameter necessary for the RQ4-MultipleRuns simulation
    # This RQ tries to find whether multiple runs on the same input matrices can be combined to improve the overall scores by using a majority voting scheme
    def get_rq_4_multipleruns_params(self):
        num_runs = 1
        while True:
            try:
                num_runs = int(input("Amount of runs? (int): "))
            except ValueError:
                print(
                    "Error! The value you entered for the amount of runs is not an integer. Try again!"
                )
            else:
                break
        self.params["num_runs"] = num_runs

    # Method get_rq_5_querydist_params asks the user to input the preferred distribution used to select queries necessary for the RQ5-QueryDist simulation
    # This RQ tries to find whether different distributions used to select queries influences the results
    def get_rq_5_querydist_params(self):
        query_distribution = QueryDistribution.reverse_zipfian
        while True:
            question += "Query distribution?\n"
            question += "\t1) Z(ipfian distribution)\n"
            question += "\t2) R(everse Zipfian distribution)\n"
            question += "\t3) U(niform distribution)\n"
            question += "[Z/R/U]: "
            try:
                choice = str(input(question)).lower()
                if choice == "z":
                    query_distribution = QueryDistribution.zipfian
                    break
                elif choice == "r":
                    query_distribution = QueryDistribution.reverse_zipfian
                    break
                elif choice == "u":
                    query_distribution = QueryDistribution.uniform
                    break
            except:
                print(
                    "Error! The value you entered for the query distribution is not correct. Try again!"
                )
        self.params["query_distribution"] = query_distribution
