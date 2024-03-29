# Implementation of the Porters 2 stemming algorithm in the nltk library
from nltk.stem import SnowballStemmer

# Class WordExtractor extracts the words out of a single email file
class WordExtractor:
    # Method remove_header_ENRON removes the header of a single (email) file (ENRON dataset).
    # Each email starts with 'Message-ID:' and the header finishes with 'X-FileName:'
    def remove_header_ENRON(self, lines):
        in_header = False
        removed_header = False
        file = ""
        for i, line in enumerate(lines):
            if line.startswith("Message-ID:") and not removed_header:
                in_header = True
                pass
            elif line.startswith("X-FileName:"):
                in_header = False
                removed_header = True
                pass
            elif in_header and not removed_header:
                pass
            else:
                file += line
        return file

    # Method remove_header_and_footer_Apache removes the header and footer of a single (email) file (Apache dataset).
    def remove_header_and_footer_Apache(self, lines):
        file = ""
        for i, line in enumerate(lines):
            # Deletes header as generated by the 'Apache_dataset_crawler.py' file
            if line.startswith("FROM: "):
                pass
            elif line.startswith("SUBJECT: "):
                pass
            elif line.startswith("DATE: "):
                pass
            # Deletes footer as featured on: http://mail-archives.apache.org/mod_mbox/lucene-java-user/
            elif line.startswith("View this message in context:"):
                pass
            elif line.startswith("Sent from the Lucene - Java Users"):
                pass
            elif line.startswith(
                "---------------------------------------------------------------------"
            ):
                pass
            elif line.startswith("To unsubscribe, e-mail:"):
                pass
            elif line.startswith("For additional commands, e-mail:"):
                pass
            else:
                file += line
        return file

    # Method extract_words extracts the words of a single file by splitting the entire (email) file on whitespace (\t, \n and space)
    def extract_words(self, file_name, dataset="ENRON"):
        lines = []
        try:
            f = open(file_name, "r", encoding="latin-1")
            lines = f.readlines()
            f.close()
        except Exception:
            raise ValueError("File name is not correct")
        if dataset == "ENRON":
            contents = self.remove_header_ENRON(lines)
        elif dataset == "ApacheLucene-java-user":
            contents = self.remove_header_and_footer_Apache(lines)
        else:
            raise ValueError("Dataset name is not correct")
        lower_case = contents.lower()
        return lower_case.split()

    # Method preprocess_file first tokenizes the contents of a file by splitting the content on whitespace characters
    # It then stems all single words using the nltk library
    # It returns a list of all words and their occurrence count, which will be used to find the most occurring words
    def preprocess_file(self, filename, dataset="ENRON"):
        stemmer = SnowballStemmer("english")
        key_dict = {}
        temp_list = self.extract_words(filename, dataset=dataset)
        for i, word in enumerate(temp_list):
            stemmed = stemmer.stem(word)
            if stemmed in key_dict.keys():
                key_dict[stemmed] = key_dict[stemmed] + 1
            else:
                key_dict[stemmed] = 1
        return key_dict
