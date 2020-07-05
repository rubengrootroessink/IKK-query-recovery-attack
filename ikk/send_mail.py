# Import SMTP connections parameters from config.py
from config import Config

# Import Enum QueryDistribution
from ikk.distribution import QueryDistribution

# smtplib library is used to make a connection to an external SMTP server
import smtplib

# MIMEText and MIMEMultipart are used to define the body of an email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Class SendMail is used to send emails with status updates using a connection to an external SMTP server
class SendMail:

    # Method send_mail sends an email containing specific simulation parameters/results to a specific email address
    def send_mail(self, simulation_name, parameters):
        config = Config()
        s = smtplib.SMTP(host=config.hostname, port=config.port)
        s.starttls()
        s.login(config.username, config.password)
        message = MIMEMultipart("alternative")
        message["Subject"] = (
            "Your test "
            + str(simulation_name)
            + " ran succesfully on server: "
            + str(parameters["ip"])
        )
        message["From"] = config.sender_email
        message["To"] = config.receiver_email

        text = (
            """
        Hi """
            + config.email_username
            + """
            
        The test with the following parameters ran succesully:
        Start time: """
            + str(parameters["starttime"])
            + """
        End time: """
            + str(parameters["endtime"])
            + """
        -----------------------------------------------------------------
        Total time: """
            + str(parameters["endtime"] - parameters["starttime"])
            + """
        
        Initial temperature: """
            + str(parameters["initial_temperature"])
            + """
        Cool down rate: """
            + str(parameters["cool_down_rate"])
            + """
        Reject rate: """
            + str(parameters["reject_rate"])
            + """
         
        Dataset: """
            + str(parameters["dataset"])
            + """
        Ciphertext foldername: """
            + str(parameters["server_knowledge_folder_name"])
            + """
        Plaintext foldername: """
            + str(parameters["background_knowledge_folder_name"])
            + """
        Document percentage: """
            + str(parameters["document_percentage"])
            + """
        Keyword percentage: """
            + str(parameters["keyword_percentage"])
            + """
        Gaussian noise constant: """
            + str(parameters["gaussian_noise_constant"])
            + """
                
        Number of keywords: """
            + str(parameters["num_keywords"])
            + """
        Number of queries: """
            + str(parameters["num_queries"])
            + """
        Query distribution?: """
            + str(parameters["query_distribution"])
            + """
        Deterministic IKK?: """
            + str(parameters["deterministic_ikk"])
            + """
          
        Values: """
            + str(parameters["result_mapping"])
            + """
           
        Highest possible score: """
            + str(len(parameters["possible_score"]) / parameters["num_queries"])
            + """
        Possible correctly identified queries: """
            + str(parameters["possible_score"])
            + """
        Correctly identified queries: """
            + str(parameters["correctly_identified_queries"])
            + """
        Result: """
            + str(parameters["score"])
            + """
    
        Termination factors: """
            + str(parameters["success_reject"])
            + """/"""
            + str(parameters["current_temperature"])
            + """
        Number of accepted new states: """
            + str(parameters["accepted_count"])
            + """
        Number of total loops: """
            + str(parameters["total_count"])
            + """
        Values of E: """
            + str(parameters["guess_of_E"])
            + """
        
        Metric 1 (* keywords not occurring): """
            + str(parameters["sim_metric_1"])
            + """
        Metric 2 (* cells not occurring): """
            + str(parameters["sim_metric_2"])
            + """
        Metric 3 (* distance of ciphertext to plaintext matrix): """
            + str(parameters["sim_metric_3"])
            + """
        
        IP: """
            + str(parameters["ip"])
            + """
        ID: """
            + str(parameters["id"])
            + """
        Run: """
            + str(parameters["current_run"])
            + """/"""
            + str(parameters["num_runs"])
        )

        message.attach(MIMEText(text, "plain"))
        s.sendmail(config.sender_email, config.receiver_email, message.as_string())
        s.quit()

    # Method test_connection is used to test the SMTP connection before starting the simulation
    def test_connection(self):
        config = Config()
        try:
            s = smtplib.SMTP(host=config.hostname, port=config.port)
            s.starttls()
            s.login(config.username, config.password)
            s.quit()
            return True
        except:
            return False

    # Method send_error sends an error that occurred during Runtime
    def send_error(self, simulation_name, error, ip):
        config = Config()
        s = smtplib.SMTP(host=config.hostname, port=config.port)
        s.starttls()
        s.login(config.username, config.password)
        message = MIMEMultipart("alternative")
        message["Subject"] = (
            "Your test " + str(simulation_name) + " failed on server: " + str(ip)
        )
        message["From"] = config.sender_email
        message["To"] = config.receiver_email
        text = str(error)
        message.attach(MIMEText(text, "plain"))
        s.sendmail(config.sender_email, config.receiver_email, message.as_string())
        s.quit()
