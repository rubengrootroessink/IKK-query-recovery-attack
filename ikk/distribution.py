# Import Enum class of enum library
from enum import Enum

# Class QueryDistribution is used allow the user to select the distribution to simulate queries
# Options are:
# - Zipfian distribution (the more a word occurs the higher the chance it is chosen)
# - reverse Zipfian distribution (self explanatory)
# - Uniform distribution (the occurrence count of words does not influence its chance of being chosen)
class QueryDistribution(Enum):
    reverse_zipfian = "Reverse Zipfian"
    zipfian = "Zipfian"
    uniform = "Uniform"
