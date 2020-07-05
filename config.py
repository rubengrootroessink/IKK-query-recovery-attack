# Import enum library
from enum import Enum

# Easy way of seeing throughout all files whether to debug to the command line (Print) or via email (Mail)
class DebugMode(Enum):
    Mail = "mail"
    Print = "print"


# Class Config contains global system parameters
class Config:

    # Used to set up an SMTP connection to send an email via the specified SMTP server
    hostname = ""
    sender_email = ""
    port = 587
    username = ""
    password = ""

    # The receiving email and the name of the addressee
    receiver_email = ""
    email_username = ""

    # Debug settings, send_result_email specifies whether to send an email that a simulation has finished
    debug = False
    debug_mode = DebugMode.Mail  # DebugMode.Mail or DebugMode.Print
    send_result_email = True
