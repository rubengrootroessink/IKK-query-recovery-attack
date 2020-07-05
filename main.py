# Config file containing system parameters such as the SMTP connection and debug settings
from config import Config, DebugMode

# Allows user to input specific parameters per simulation
from ikk.params import Params

# The 5 different simulations, each corresponding to a Research Question (RQ)
from ikk.simulations.rq_1_coocsim import CoocSim  # RQ 1
from ikk.simulations.rq_2_paramsim import ParamSim  # RQ 2
from ikk.simulations.rq_3_deterministicikk import DeterministicIKK  # RQ 3
from ikk.simulations.rq_4_multipleruns import MultipleRuns  # RQ 4
from ikk.simulations.rq_5_querydist import QueryDistribution  # RQ 5

# Used to send an email containing all results
# Only used if send_result_email is True in config.py
from ikk.send_mail import SendMail

# Retrieves Public IP of machine for debugging purposes (parallelization)
from urllib.request import urlopen

# Import traceback for debugging purposes (sends error via mail/via command line)
import traceback

# Functions used throughout simulations
import re, random, string

# Function run allows a user to select one out of the 5 simulations and their respective parameters
def main():
    # The instance of one of the simulations (represented as a class, with a function run())
    instance = None

    # The name of the specific simulation, used to save results and decide on parameters
    simulation_name = None

    # A dictionary which will be filled with simulation specific parameters
    parameters = {}

    # STMP mail instance, which is used to send either debug mails or emails containing simulation results
    mail_instance = SendMail()

    # Debug instance, used to request system parameters
    config = Config()

    # If config.debug is True and the DebugMode is 'Mail' or the simulation sends a result email after its run
    # The system checks whether the SMTP connection works before it starts its run
    # Prints an error message if the SMTP connection cannot be set up and ends the run
    if (
        config.debug and config.debug_mode == DebugMode.Mail
    ) or config.send_result_email:
        if not mail_instance.test_connection():
            print("Failed to set up mail connection")
            return

    # Asks the user, on the command line, if it prefers a test run ('Y') or prefers a normal run ('N')
    # Each Simulation class has a test version and a normal version
    # The test version has certain parameters set very low, so test will not take to long 
    # Useful for debug purposes
    test_sim = False
    while True:
        try:
            choice = str(input("Test run? [Y/N]: ")).lower()
            if choice == "y":
                test_sim = True
                break
            elif choice == "n":
                break
        except Exception as e:
            print("The value you entered is not correct. Please try again!")

    # Asks the user, on the command line, to select the simulation it wants to run
    # Depending on the user choice it sets the global simulation instance to a specific simulation class
    # Input C corresponds to RQ1 regarding the correlation between co-occurrence similarity and results obtained
    # Input P corresponds to RQ2 regarding the correlation between the input parameters of the Simulated Annealing algorithm
    # Input D corresponds to RQ3 researching the effect of the proposed deterministic IKK attack
    #   (which takes in account overall word occurrence in a given dataset)
    # Input M corresponds to RQ4 researching the effect of combining multiple protocol runs to boost the obtained results
    # Input R corresponds to RQ5 researching the effect of using different distributions to simulate queries
    while True:
        try:
            question = "Simulation?\n"
            question += "\t1) C(o-occurrence similarity)\n"
            question += "\t2) P(arameter similarity)\n"
            question += "\t3) D(eterministic IKK)\n"
            question += "\t4) M(ultiple runs)\n"
            question += "\t5) Q(uery dist)\n"
            question += "[C/P/D/M/Q]: "
            choice = str(input(question)).lower()
            if choice == "c":
                simulation_name = "RQ1-CoocSim"
                instance = CoocSim()
                break
            elif choice == "p":
                simulation_name = "RQ2-ParamSim"
                instance = ParamSim()
                break
            elif choice == "d":
                simulation_name = "RQ3-DeterministicIKK"
                instance = DeterministicIKK()
                break
            elif choice == "m":
                simulation_name = "RQ4-MultipleRuns"
                instance = MultipleRuns()
                break
            elif choice == "q":
                simulation_name = "RQ5-QueryDist"
                instance = QueryDistribution()
                break
        except Exception as e:
            ip = str(get_pub_ip())
            sender = SendMail()
            sender.send_error(simulation_name, traceback.format_exc(), ip)

    # Generates an id of a run (combination of the simulation name and a random set of 9 ASCII letters and digits
    id = str(simulation_name) + "-" + str(random_id())

    # Retrieves the public IP of the machine the simulation is run on
    # Can be useful if multiple (public) machines are used to calculate simulations
    # Is set to 0.0.0.0 if the debugging mode is 'print' so that the test can be run easily without internet connection
    ip = str(get_pub_ip())
    if config.debug_mode == DebugMode.Print:
        ip = "0.0.0.0"

    # Requests the user to input parameters based on the selected simulation
    params = Params()
    parameters = params.get_params(simulation_name)

    # Runs a simulation based on whether it was a test run or not
    try:
        if test_sim:
            print("TEST RUN")
            instance.test_run(parameters, simulation_name, id, ip)
        else:
            print("NORMAL RUN")
            instance.run(parameters, simulation_name, id, ip)
    except Exception as e:
        sender = SendMail()
        sender.send_error(simulation_name, traceback.format_exc(), ip)

    # After the user observes 'TEST RUN' or 'NORMAL RUN' and config.debug == False and config.send_result_mail == True
    #   it can decide to uncouple the Python process from any terminal on a remote machine:
    # This ensures the process will not be killed after closing the terminal
    # This can be done on Linux (remote) machines using:
    # 'CTRL+Z' pauses the current process in the background
    # 'disown -h %X' uncouples background process X from the current opened terminal (X = 1 usually)
    # 'bg' puts the last process in the background


# Retrieves the current (public) ip of the machine running a simulation
def get_pub_ip():
    data = str(urlopen("http://checkip.dyndns.com/").read())
    return re.compile(r"Address: (\d+\.\d+\.\d+\.\d+)").search(data).group(1)


# Generates a random id of the form 'XXX-XXX-XXX' where X is an ASCII letter or a digit
def random_id():
    result = ""
    for i in range(0, 3):
        result += random.choice(string.ascii_letters + string.digits)
    result += "-"
    for i in range(0, 3):
        result += random.choice(string.ascii_letters + string.digits)
    result += "-"
    for i in range(0, 3):
        result += random.choice(string.ascii_letters + string.digits)
    return result


main()
