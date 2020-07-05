# Loads in configuration settings in config.py
from config import Config, DebugMode

# Import Enum QueryDistribution which defines the possible query distributions used in the system
from ikk.distribution import QueryDistribution

# DatasetExtractor is a class which gives a simulation all the tools to load in a set of words together with a list the documents these words occur in
from ikk.dataset_extraction import DatasetExtractor

# MatrixGenerator is a class which gives a simulation all the tools to generate an inverted index from a list of words and the documents these words occur in
from ikk.matrix_generation import MatrixGenerator

# SimilarityCalculator is a class which gives a simulation all the tools to calculate the similarity from on matrix to another
from ikk.similarity_calculation import SimilarityCalculator

# SendMail is a class which is used to send updates regarding simulations from a remote machine via SMTP to an email adress specified
from ikk.send_mail import SendMail

# IO is a class which is used to write the results of a simulation to a file
from ikk.read_write import IO

# IKK is a class which implements the proposed algorithm by Islam et al. in their paper
#   'Access Pattern disclosure on Searchable Encryption: Ramification, Attack and Mitigation'
from ikk.ikk import IKK

# Library datetime is used to find the current timestamp to add the total time of a simulation to the results obtained
import datetime

# Class Simulation is meant to be an abstract method with all parameters set to specific values
# Simulations corresponding to specific Research Questions implement this method and set parameters to the right values using the
#   __init__() method or the set_parameters() method
class Simulation:

    # initial_temperature, cool_down_rate and reject_rate are input parameters of the Simulated Annealing algorithm used in the IKK attack
    initial_temperature = 1.0
    cool_down_rate = 0.999
    reject_rate = 50000

    # The dataset to use, options currently are 'ENRON' and 'ApacheLucene-java-user'
    dataset = "ENRON"

    # Folder name is used to give the user a choice on which folder of a dataset to use:
    # The ENRON dataset has a lot of subfolders, in our simulations we only used '_sent_mail' and 'inbox'
    # The ApacheLucene-java-user dataset currently only has a subfolder 'mbox'
    # Note, if the folder names here don't match the dataset the algorithm might fail
    server_knowledge_folder_name = "_sent_mail"
    background_knowledge_folder_name = "_sent_mail"

    # The number of keywords in the background_knowledge_cooccurrence_matrix and the number of queries in the server_knowledge_cooccurrence_matrix
    num_keywords = 1500
    num_queries = 150

    # The percentage of the total number of documents/keywords used while generating the background_knowledge cooccurence matrix
    # These percentages are used to simulate a setting where the background knowledge (background_knowledge cooccurrence matrix) is incomplete
    document_percentage = 1.0
    keyword_percentage = 1.0

    # The distribution used to select queries. Islam et al. (IKK) use the Zipfian distribution, other options are the reversed Zipfian distribution and
    #   the Uniform distribution.
    query_distribution = QueryDistribution.zipfian

    # Whether to use the proposed Deterministic IKK attack where new states in the Simulated Annealing algorithm are not selected randomly, but,
    #   based on the relative amount of documents a keyword occurs in
    deterministic_ikk = False

    # Used to simulate a setting where the background knowledge (background_knowledge cooccurrence matrix) is incomplete
    gaussian_noise_constant = None

    # The amount of runs the simulation should execute on the same input cooccurrence matrices. Used to find the effect of combining multiple runs
    num_runs = 1

    # The folder where the results should be written to (specific on the simulation selected)
    results_folder = None

    # The results which are written to a file/send via email to a specified mail address
    results = {}

    # The debug settings. 'debug' is a boolean specifying whether to debug or not. 'debug_mode' has options Mail/Print whether to debug on the command line or
    #   send updates via mail
    debug = Config.debug
    debug_mode = Config.debug_mode

    # 'send_result_email' specifies whether the user should receive an email with the results when a simulation is done
    # Only usable when a user inputs his SMTP server credentials in config.py
    send_result_email = Config.send_result_email

    # Method __init__ initializes the class Simulation
    def __init__(self):
        super().__init__()

    # Method set_parameters sets the parameters of a specific simulation, based on the input parameters given to this class
    # Not implemented in this setting as all variables are already set
    # Different simulations which implement the Simulation class have an implementation for this method
    def set_parameters(self, parameters):
        pass

    # Method set_results adds all parameters to the results dictionary, including the ip, id and three similarity measurements
    def set_results(self, ip, id, sim_metric_1, sim_metric_2, sim_metric_3):
        self.results["ip"] = ip
        self.results["id"] = id

        self.results["initial_temperature"] = self.initial_temperature
        self.results["cool_down_rate"] = self.cool_down_rate
        self.results["reject_rate"] = self.reject_rate

        self.results["dataset"] = self.dataset
        self.results["server_knowledge_folder_name"] = self.server_knowledge_folder_name
        self.results[
            "background_knowledge_folder_name"
        ] = self.background_knowledge_folder_name

        self.results["num_keywords"] = self.num_keywords
        self.results["num_queries"] = self.num_queries

        self.results["document_percentage"] = self.document_percentage
        self.results["keyword_percentage"] = self.keyword_percentage
        self.results["gaussian_noise_constant"] = self.gaussian_noise_constant

        # .value is added to get the JSON serializable value (string) from the QueryDistribution Enum
        self.results["query_distribution"] = self.query_distribution.value

        self.results["deterministic_ikk"] = self.deterministic_ikk

        self.results["num_runs"] = self.num_runs

        self.results["sim_metric_1"] = sim_metric_1
        self.results["sim_metric_2"] = sim_metric_2
        self.results["sim_metric_3"] = sim_metric_3

    # Method debug_message is used to debug a certain input message
    # It output either to the command line (DebugMode.Print) or to a specified email adress (in config.py) (DebugMode.Mail)
    def debug_message(self, mail_instance, simulation_name, message, id, ip):
        if self.debug:
            if self.debug_mode == DebugMode.Print:
                print(message)
            elif self.debug_mode == DebugMode.Mail:
                mail_instance.send_progress_message(simulation_name, message, id, ip)

    # Method generate_dataset generates dictionaries of words and the files these words occur in
    # The server_knowledge_dataset is always of size num_queries
    # While generating the server_knowledge_dataset first the most occurring {{ num_keywords }} are chosen (- the top 200 most occurring words)
    # From these {{ num_keywords }} the simulation simulates a set of queries of size num_queries using the (reverse) Zipfian/Uniform distribution
    # The background_knowledge_dataset always of size {{ num_keywords }}
    # While generating the background_knowledge dataset the user has the option to disregard a specified set of documents (1 - document_percentage) or
    #   a specified percentage of words is disregarded (1 - keyword_percentage)
    # While disregarding part of the keywords the system ensures the total amount of keywords remains the same by taking more than
    #   the top {{ num_keywords }} keywords.
    # The variable server_knowledge_dataset_full is used to calculate the similarity between the complete underlying dataset on the server and
    #   the background dataset (the latter known to the adversary)
    def generate_datasets(self):
        extractor = DatasetExtractor()
        (
            server_knowledge_dataset,
            server_knowledge_documents,
            full_server_dataset,
        ) = extractor.get_server_knowledge(
            self.dataset,
            self.server_knowledge_folder_name,
            self.num_keywords,
            self.num_queries,
            query_distribution=self.query_distribution,
        )
        (
            background_knowledge_dataset,
            background_knowledge_documents,
        ) = extractor.get_background_knowledge(
            self.dataset,
            self.background_knowledge_folder_name,
            self.num_keywords,
            self.num_queries,
            document_percentage=self.document_percentage,
            keyword_percentage=self.keyword_percentage,
        )
        return (
            server_knowledge_dataset,
            server_knowledge_documents,
            full_server_dataset,
            background_knowledge_dataset,
            background_knowledge_documents,
        )

    # Method generate_indices generates two inverted indices from two dictionaries containing a certain amount of words and the documents these words occur in
    def generate_indices(
        self,
        generator,
        server_knowledge_dataset,
        server_knowledge_documents,
        server_knowledge_dataset_full,
        background_knowledge_dataset,
        background_knowledge_documents,
    ):
        server_knowledge_index = generator.generate_inverted_index(
            server_knowledge_dataset, server_knowledge_documents
        )
        server_knowledge_index_full = generator.generate_inverted_index(
            server_knowledge_dataset_full, server_knowledge_documents
        )
        background_knowledge_index = generator.generate_inverted_index(
            background_knowledge_dataset, background_knowledge_documents
        )
        return (
            server_knowledge_index,
            server_knowledge_index_full,
            background_knowledge_index,
        )

    # Method generate_coocs generates two cooccurrence matrices from two inverted indices
    # The user has the option to add a certain level of Gaussian noise to the background_knowledge cooccurrence matrix to simulate
    #   incomplete background knowledge
    def generate_coocs(
        self,
        generator,
        server_knowledge_index,
        server_knowledge_index_full,
        background_knowledge_index,
    ):
        server_knowledge_cooc = generator.generate_cooccurrence_matrix(
            server_knowledge_index
        )
        server_knowledge_cooc_full = generator.generate_cooccurrence_matrix(
            server_knowledge_index_full
        )
        background_knowledge_cooc = generator.generate_cooccurrence_matrix(
            background_knowledge_index, self.gaussian_noise_constant
        )
        return (
            server_knowledge_cooc,
            server_knowledge_cooc_full,
            background_knowledge_cooc,
        )

    # Method test_run sets parameters such that a simulation takes much less time (less keywords/queries, lower rejection rate)
    # This method is useful for debugging purposes
    def test_run(self, parameters, simulation_name, id, ip):
        self.reject_rate = 20
        self.num_keywords = 20
        self.num_queries = 10
        self.results_folder = "Test"
        self.run(parameters, simulation_name, id, ip)

    # Method run implements the full IKK run including loading in all data
    def run(self, parameters, simulation_name, id, ip):

        # First of all all parameters are set according to the needs of specific simulations
        # Method set_parameters is not implemented in the Simulation class and therefore does not change any values
        self.set_parameters(parameters)

        # generator is an instance of the GenerateMatrix class which gives all the tools necessary to generate inverted indices and cooccurrence matrices
        generator = MatrixGenerator()

        # similarity_calc is an instance of the SimilarityCalc class which allows a user to calculate the similarity between two matrices
        similarity_calc = SimilarityCalculator()

        # mail_instance is an instance of the SendMail class used to send progress/error/results emails to a specified email address)
        mail_instance = SendMail()

        # ikk_instance is an instance of the IKK class which gives all the tools necessary to execute the (Deterministic) IKK attack
        ikk_instance = IKK()

        # io is an instance of the IO class which allows for reading/writing .json files containing results of simulation runs
        io = IO()

        message = (
            "Started test "
            + str(simulation_name)
            + " at "
            + str(datetime.datetime.now())
        )
        self.debug_message(mail_instance, simulation_name, message, id, ip)

        # Generate datasets
        (
            server_knowledge_dataset,
            server_knowledge_documents,
            server_knowledge_dataset_full,
            background_knowledge_dataset,
            background_knowledge_documents,
        ) = self.generate_datasets()
        message = "Generated datasets at " + str(datetime.datetime.now())
        self.debug_message(mail_instance, simulation_name, message, id, ip)

        # Generate indices
        (
            server_knowledge_index,
            server_knowledge_index_full,
            background_knowledge_index,
        ) = self.generate_indices(
            generator,
            server_knowledge_dataset,
            server_knowledge_documents,
            server_knowledge_dataset_full,
            background_knowledge_dataset,
            background_knowledge_documents,
        )
        message = "Generated indices at " + str(datetime.datetime.now())
        self.debug_message(mail_instance, simulation_name, message, id, ip)

        # Generate coocs
        (
            server_knowledge_cooc,
            server_knowledge_cooc_full,
            background_knowledge_cooc,
        ) = self.generate_coocs(
            generator,
            server_knowledge_index,
            server_knowledge_index_full,
            background_knowledge_index,
        )
        message = "Generated coocs at " + str(datetime.datetime.now())
        self.debug_message(mail_instance, simulation_name, message, id, ip)

        # Calculate similarity between the (full) server_knowledge and background_knowledge cooccurrence matrices
        sim_metric_1, sim_metric_2, sim_metric_3 = similarity_calc.calc_metrics(
            server_knowledge_cooc_full, background_knowledge_cooc
        )
        message = (
            "Similarities are "
            + str(sim_metric_1)
            + ", "
            + str(sim_metric_2)
            + ", "
            + str(sim_metric_3)
            + ", respectively"
        )
        self.debug_message(mail_instance, simulation_name, message, id, ip)

        # Fill a dictionary containing results for easy conversion to .json files
        self.set_results(ip, id, sim_metric_1, sim_metric_2, sim_metric_3)

        # Calculate highest possible 'recovery score' of simulation run
        self.results["possible_score"] = list(
            set(server_knowledge_cooc.keys().tolist()).intersection(
                set(background_knowledge_cooc.keys().tolist())
            )
        )

        # For loop allows for multiple simulation run on same dataset (for Research Question 4)
        for i in range(1, self.num_runs + 1):
            message = (
                "Started "
                + str(i)
                + " out of "
                + str(self.num_runs)
                + " runs at "
                + str(datetime.datetime.now())
            )
            self.debug_message(mail_instance, simulation_name, message, id, ip)

            # Add number of current run to simulation results
            self.results["current_run"] = i

            # Calls method single_ikk to perform the IKK attack once
            result = self.single_ikk(
                server_knowledge_cooc,
                background_knowledge_cooc,
                server_knowledge_index,
                background_knowledge_index,
                ikk_instance,
            )

            message = "Run " + str(i) + " finished at " + str(datetime.datetime.now())
            self.debug_message(mail_instance, simulation_name, message, id, ip)

            # If config.send_result_email == True sends email to specified email containing all the results
            if self.send_result_email:
                mail_instance.send_mail(simulation_name, result)

            # Writes the results of a single simulation run to a file
            simulation_folder = self.results_folder
            file_name = (
                str(self.results["id"])
                + "-"
                + str(i)
                + "-"
                + str(self.results["starttime"])
            )
            data = result
            io.save_to_file(simulation_folder, file_name, data)

    # One IKK run simulation
    def single_ikk(
        self,
        server_knowledge_cooc,
        background_knowledge_cooc,
        server_knowledge_index,
        background_knowledge_index,
        ikk_instance,
    ):
        starttime = datetime.datetime.now()

        # Performs the IKK attack once, first finds an initial mapping in the optimizer method in ikk.py
        (
            result_mapping,
            current_temperature,
            success_reject,
            guess_of_E,
            total_count,
            accepted_count,
        ) = ikk_instance.optimizer(
            server_knowledge_cooc,
            background_knowledge_cooc,
            server_knowledge_index,
            background_knowledge_index,
            self.initial_temperature,
            self.cool_down_rate,
            self.reject_rate,
            self.deterministic_ikk,
        )

        endtime = datetime.datetime.now()

        # Calculates the correctly mapped queries in the mapping returned by the IKK run
        correctly_identified_queries = []
        counter = 0
        for query, keyword in result_mapping.items():
            if query == keyword:
                counter += 1
                correctly_identified_queries.append(query)

        # Adds IKK run specific results to self.results
        self.results["score"] = counter / len(result_mapping)
        self.results["starttime"] = starttime
        self.results["endtime"] = endtime
        self.results["result_mapping"] = result_mapping
        self.results["current_temperature"] = current_temperature
        self.results["success_reject"] = success_reject
        self.results["guess_of_E"] = guess_of_E
        self.results["total_count"] = total_count
        self.results["accepted_count"] = accepted_count
        self.results["correctly_identified_queries"] = correctly_identified_queries
        return self.results
