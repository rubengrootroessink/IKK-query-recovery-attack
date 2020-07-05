# Library os is imported to read from/write to directories and files
import os

# Library json is used to write to/read from a .json structured file
import json

# Library random is used to randomly simulate queries, document deletion and keyword deletion
import random

# Import Enum containing different distributions for simulating queries
from ikk.distribution import QueryDistribution

# Imports the WordExtractor class from the word_extraction.py file
from ikk.word_extraction import WordExtractor

# Class DatasetExtractor is used to extract a dataset for efficiency reasons as a new dataset does not have to be generated each new simulation as
#   the underlying dataset will not change throughout all simulations. Different data distributions are simulated by disregarding
#   part of a dataset/adding noise
class DatasetExtractor:

    # Method write_to_json is used to write a dataset to a .json file
    # A dataset in this case is a dictionary of file and the words that occur in these files
    #   (together with a count of how much a keyword occurs in a specific file)
    def write_to_json(self, dictionary, file_name):
        file_path = os.path.join(os.getcwd(), "StemmedDatasets", file_name)
        with open(file_path, "w") as file:
            json.dump(dictionary, file)

    # Method read_from_json is used to read a dataset from a .json file
    # A dataset in this case is a dictionary of file and the words that occur in these files
    #   (together with a count of how much a keyword occurs in a specific file)
    def read_from_json(self, file_name):
        file_path = os.path.join(os.getcwd(), "StemmedDatasets", file_name)
        with open(file_path, "r") as file:
            dictionary = json.load(file)
        return dictionary

    # Method find_file_paths_recursively recursively finds files in a sub directory of a mailbox
    # This method is a helper function to the function find_file_paths
    def find_file_paths_recursively(
        self, directory_path, user, mailbox_name, directory_name
    ):
        result_dict = {}
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file = item
                result_dict[user + "-" + directory_name + "-" + file] = os.path.join(
                    directory_path, file
                )
            elif os.path.isdir(item_path):
                sub_directory_name = item
                recursive_file_paths = self.find_file_paths_recursively(
                    item_path,
                    user,
                    mailbox_name,
                    directory_name + "-" + sub_directory_name,
                )
                for key, value in recursive_file_paths.items():
                    result_dict[key] = value
        return result_dict

    # Method find_file_paths finds all files in a specific mailbox (sub directory) of a user directory in a dataset
    # It first assumes all directories in {{ directory }} are the names of users thereby potentially simulating mailboxes of these users
    # Then it finds the right mailbox in the user directory, using {{ mailbox_name }}
    # if {{ mailbox_name }} also contains directories the method recursively finds all files using method find_file_paths_recursively
    def find_file_paths(self, dataset_path, mailbox_name):
        file_paths = {}
        user_list = os.listdir(dataset_path)
        for user in user_list:
            try:
                user_directory = os.path.join(dataset_path, user, mailbox_name)
                for item in os.listdir(user_directory):
                    item_path = os.path.join(user_directory, item)
                    if os.path.isfile(item_path):
                        file_name = item
                        file_id = user + "-" + file_name
                        file_paths[file_id] = {}
                        file_paths[file_id]["id"] = os.path.join(
                            user_directory, file_name
                        )
                        file_paths[file_id]["user"] = user
                    elif os.path.isdir(item_path):
                        directory_name = item
                        recursive_file_paths = self.find_file_paths_recursively(
                            item_path, user, mailbox_name, directory_name
                        )
                        for key, value in recursive_file_paths.items():
                            file_paths[key] = {}
                            file_paths[key]["id"] = value
                            file_paths[key]["user"] = user
            except:
                pass
        return file_paths, user_list

    # Method extract_word_occurrence_per_file loops through a dataset and returns:
    # - A list of user is said dataset {{ user_list }}
    # - A dictionary containing file ids and all the words in said files {{ word_occurrence_per_file }}
    # - A dictionary of file ids and their paths {{ file_paths }}
    def extract_word_occurrence_per_file(self, dataset_name, mailbox_name):
        extract_words = WordExtractor()
        dataset_path = os.path.join(os.getcwd(), "Datasets", dataset_name)

        file_paths, user_list = self.find_file_paths(dataset_path, mailbox_name)
        word_occurrence_per_file = {}

        for file_id, file_path in file_paths.items():
            word_occurrence_per_file[file_id] = extract_words.preprocess_file(
                file_path["id"], dataset=dataset_name
            )

        return_dict = {}
        return_dict["file_ids"] = file_paths
        return_dict["word_occurrence_per_file"] = word_occurrence_per_file
        return_dict["user_list"] = user_list
        return return_dict

    # Method extract_file_occurrence_per_word is used to generate a dictionary containing {{ num_keywords }} words and the files
    #   each of these words occurs in from a dictionary of files and their corresponding word occurrence
    #   (which word occurs in which file and how many times)
    # The method includes an optional parameter {{ keyword_percentage }} to remove a certain percentage of words
    #   (while ensuring the amount of words returns still equals {{ num_keywords }})
    # The {{ keyword_percentage }} parameter is used to simulate non-full background knowledge in the IKK attack
    def extract_file_occurrence_per_word(
        self,
        word_occurrence_per_file,
        num_keywords,
        keyword_percentage=None,
        omit_top=200,
    ):
        file_occurrence_per_word = {}

        extra_num_of_words = 0
        if keyword_percentage is not None and keyword_percentage != 1.0:
            extra_num_of_words = round((1 - keyword_percentage) * num_keywords)

        for filename, words in word_occurrence_per_file.items():
            for word, occurrence_count in words.items():
                word_occurrence = {}
                if word in file_occurrence_per_word:
                    word_occurrence["amount"] = (
                        occurrence_count + file_occurrence_per_word[word]["amount"]
                    )
                    word_occurrence["files"] = file_occurrence_per_word[word][
                        "files"
                    ] + [filename]
                else:
                    word_occurrence["amount"] = occurrence_count
                    word_occurrence["files"] = [filename]
                file_occurrence_per_word[word] = word_occurrence

        assert len(file_occurrence_per_word) >= num_keywords + extra_num_of_words

        # Remove {{ omit_top }} (standard 200, in all simulations) most occurring and return {{ num_keywords }} most occurring data items after that
        sorted_file_occurrence_per_word = list(
            reversed(
                sorted(file_occurrence_per_word.items(), key=lambda x: x[1]["amount"])
            )
        )[omit_top:]

        file_occurrence_per_word = {}

        if keyword_percentage is None or keyword_percentage == 1.0:
            for word, occurrence in sorted_file_occurrence_per_word[:num_keywords]:
                file_occurrence_per_word[word] = occurrence
        elif keyword_percentage is not None and keyword_percentage != 1.0:
            for word, occurrence in random.sample(
                sorted_file_occurrence_per_word[:num_keywords],
                num_keywords - extra_num_of_words,
            ):
                file_occurrence_per_word[word] = occurrence
            for word, occurrence in sorted_file_occurrence_per_word[
                num_keywords : num_keywords + extra_num_of_words
            ]:
                file_occurrence_per_word[word] = occurrence

        assert len(file_occurrence_per_word) == num_keywords
        return file_occurrence_per_word

    # Method querify is used to querify a dictionary containing words, the total occurrence count of said words
    # and a list files a specific word occurs in at least once
    # The result is a dictionary of length {{ num_queries }}
    # The selection of queries (simulation) uses a Zipfian distribution, the reverse Zipfian distribution or a Uniform distribution
    # The probability of a word being chosen as a query (if using the Zipfian/Reverse Zipfian distribution) is calculated
    #   by its rank in total occurrence in a dataset
    # The method loops through the {{ file_occurrence_per_word }} dict until it obtains the right number of (unique) queries
    def querify(
        self,
        file_occurrence_per_word,
        num_queries,
        query_distribution=QueryDistribution.zipfian,
    ):
        assert len(file_occurrence_per_word) >= num_queries

        querified_file_occurrence_per_word = {}

        if not query_distribution == QueryDistribution.uniform:
            probability_distribution = {}
            sorted_file_occurrence_per_word = list(
                reversed(
                    sorted(
                        file_occurrence_per_word.items(), key=lambda x: x[1]["amount"]
                    )
                )
            )

            if query_distribution == QueryDistribution.reverse_zipfian:
                sorted_file_occurrence_per_word = list(
                    reversed(sorted_file_occurrence_per_word)
                )

            normalization_factor = 0
            for i in range(1, len(sorted_file_occurrence_per_word) + 1):
                normalization_factor += 1 / i

            for i, (word, occurrence) in enumerate(sorted_file_occurrence_per_word):
                probability_distribution[word] = 1 / ((i + 1) * normalization_factor)

            while len(querified_file_occurrence_per_word) < num_queries:
                for word, occurrence in sorted_file_occurrence_per_word:
                    if (
                        len(querified_file_occurrence_per_word) < num_queries
                        and random.random() < probability_distribution[word]
                    ):
                        if word not in querified_file_occurrence_per_word.keys():
                            querified_file_occurrence_per_word[
                                word
                            ] = file_occurrence_per_word[word]
        elif query_distribution == QueryDistribution.uniform:
            queries = random.sample(list(file_occurrence_per_word.keys()), num_queries)
            for query in queries:
                querified_file_occurrence_per_word[query] = file_occurrence_per_word[
                    query
                ]

        return querified_file_occurrence_per_word

    # Method omit_users removes the file from users that are in the dataset, but not in parameter user_list
    # This method is used to simulate partial background knowledge by omitting mailboxes (sub directories) of users
    def omit_users(
        self, file_paths, word_occurrence_per_file, user_list, document_percentage=1
    ):
        new_user_list = random.sample(
            user_list, round(len(user_list) * document_percentage)
        )
        new_file_paths = {}
        new_word_occurrence_per_file = {}

        for file, word_dict in word_occurrence_per_file.items():
            if file_paths[file]["user"] in new_user_list:
                new_file_paths[file] = file_paths[file]
                new_word_occurrence_per_file[file] = word_dict

        return new_file_paths, new_word_occurrence_per_file, new_user_list

    # Method read_dataset generates a dataset containing a dictionary with all file(s)(ids) and their corresponding paths,
    # a dictionary containing files and their corresponding keyword occurrences, and a list of users in the dataset
    # Depending on whether the exact settings have been executed before the method returns a earlier-generated dataset
    # or generates (and writes) a new one
    def read_dataset(self, dataset_name, mailbox_name):
        # .json file (name) used to read the dataset from if it already exists or write the dataset to if not
        # The .json file contains a full dataset with:
        # - A dictionary {{ file_ids }} with file ids, the user of said file and the path to said file
        # - A dictionary {{ word_occurrence_per_file }} of all files and the (stemmed) word occurrence in said file
        # - A list {{ user_list }} of all users in the dataset folder
        # directory_name points to the folder 'StemmedDatasets' which might contain already processed datasets
        file_name = dataset_name + "-" + mailbox_name + ".json"
        directory_name = os.path.join(os.getcwd(), "StemmedDatasets")

        # If the .json file is already present in the 'StemmedDatasets' folder this means the (full) dataset has already been extracted and
        #   can be re-used for efficiency sake
        if file_name in os.listdir(directory_name):
            dataset = self.read_from_json(os.path.join(directory_name, file_name))
            # file_paths is a dictionary containing short names of files and their corresponding paths
            file_paths = dataset["file_ids"]
            # words_occurrence_per_file is a dictionary of files/documents and dictionaries of words and their occurrence count in specific files
            word_occurrence_per_file = dataset["word_occurrence_per_file"]
            # user_list contains the list of all users (the name of the sender in the ENRON/Apache dataset) in a dataset
            user_list = dataset["user_list"]
            return file_paths, word_occurrence_per_file, user_list
        # Else it calls method extract_word_occurrence_per_file to extract the dataset from a specified folder, using a specified mail box of a user
        else:
            dataset = self.extract_word_occurrence_per_file(dataset_name, mailbox_name)
            file_paths = dataset["file_ids"]
            word_occurrence_per_file = dataset["word_occurrence_per_file"]
            user_list = dataset["user_list"]
            self.write_to_json(dataset, file_name)
            return file_paths, word_occurrence_per_file, user_list

    # Method get_dataset is used to extract a dataset according to specific parameters
    # The dataset is given to this class using parameters {{ file_paths }}, {{ word_occurrence_per_file }} and {{ user_list }}
    # The user is able to choose:
    # - The number of words {{ num_keywords }} while simulating background/full/server knowledge
    # - The number of queries {{ num_queries }} while simulating the server knowledge
    # - The document percentage {{ document_percentage }} while simulating background knowledge
    # - The keyword percentage {{ keyword_percentage }} while simulating background knowledge
    # - Querify or not {{ querify }}, Boolean to specify whether or not to querify the dataset (to simulate server knowledge)
    # - Which (query) distribution used to simulate queries {{ query_distribution }} (choices are (reverse) Zifian and uniform distribution)
    def get_dataset(
        self,
        file_paths,
        word_occurrence_per_file,
        user_list,
        num_keywords,
        num_queries,
        document_percentage=None,
        keyword_percentage=None,
        querify=False,
        query_distribution=QueryDistribution.zipfian,
        omit_top=200,
    ):
        # This part is used to select only part of all documents in the dataset (to simulate partial background knowledge)
        # document_percentage specifies a percentage of users instead of from all documents
        # This setting is believed to be more realistic as an adversary is more likely to get access to mailboxes of users than
        #   a random subset of all documents
        # The amount of documents in (partial) background knowledge differs based on the which users were omitted from the simulations
        if document_percentage is not None and document_percentage != 1.0:
            file_paths, word_occurrence_per_file, user_list = self.omit_users(
                file_paths,
                word_occurrence_per_file,
                user_list,
                document_percentage=document_percentage,
            )
        document_list = list(file_paths.keys())

        # Takes the right number of words ({{ num_keywords }}) and their corresponding files
        # Depending on the value of {{ keyword_percentage }} it takes more words and their corresponding files and deletes a certain percentage
        file_occurrence_per_word = self.extract_file_occurrence_per_word(
            word_occurrence_per_file,
            num_keywords,
            keyword_percentage=keyword_percentage,
            omit_top=omit_top,
        )

        # Querifies the file_occurrence_per_word list to simulate server knowledge
        if querify:
            file_occurrence_per_word = self.querify(
                file_occurrence_per_word,
                num_queries,
                query_distribution=query_distribution,
            )

        # Removes 'amount' key from file_occurrence_per_word dict
        new_file_occurrence_per_word = {}
        for word, occurrence in file_occurrence_per_word.items():
            new_file_occurrence_per_word[word] = occurrence["files"]
        return new_file_occurrence_per_word, document_list

    # Function get_background_knowledge is used to simulate (partial) background knowledge for the IKK attack
    # Background knowledge is simulated by taking the top {{ num_keywords }} + 200 words in a set of documents that occur the most together with
    #   the lists of documents each word occurs in at least once
    # The top 200 words are removed after that (as they are assumed words that occur in almost every document like 'a' and 'the')
    # The remaining {{ num_keywords }}, together with a list of each documents each word occurs in at least once is returned as well as
    #   a list of all documents used in the simulations
    # The get_background_knowledge simulates partial background knowledge by taking a percentage of the documents in the full dataset or by removing
    #   a percentage of the keywords (while ensuring the total amount of keywords returned remains the same)
    def get_background_knowledge(
        self,
        dataset_name,
        mailbox_name,
        num_keywords,
        num_queries,
        document_percentage=None,
        keyword_percentage=None,
    ):
        file_paths, word_occurrence_per_file, user_list = self.read_dataset(
            dataset_name, mailbox_name
        )
        background_knowledge_dataset, background_knowledge_documents = self.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=document_percentage,
            keyword_percentage=keyword_percentage,
        )
        return background_knowledge_dataset, background_knowledge_documents

    # Function get_server_knowledge is used to simulate the knowledge of the 'server'/adversary
    # It also returns the 'full' dataset stored on the server (unquerified) used in the simulations as this is used to calculate metrics in these simulations
    # The knowledge of the 'server'/adversary is simulated by taking the top {{ num keywords }} + 200 words in a set of documents that
    #   occur the most together with the lists of documents each word occurs in at least once
    # The top 200 words are removed after that (as they are assumed words that occur in almost every document like 'a' and 'the')
    # From the remaining {{ num_keywords }} words, using the (reversed) Zipfian/Uniform distribution, {{ num_queries }} words are simulated and
    #   these are returned together with the list of documents each word occurs in at least once
    # The list of documents is also returned
    # The 'full' {{ dataset_stored_on_the_server }} variable contains the {{ num_keywords }} most occurring words without simulating queries,
    #   this is used for calculating metrics
    def get_server_knowledge(
        self,
        dataset_name,
        mailbox_name,
        num_keywords,
        num_queries,
        query_distribution=QueryDistribution.zipfian,
    ):
        file_paths, word_occurrence_per_file, user_list = self.read_dataset(
            dataset_name, mailbox_name
        )
        server_knowledge_dataset, documents_on_server = self.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            querify=True,
            query_distribution=query_distribution,
        )
        dataset_stored_on_server, documents_on_server = self.get_dataset(
            file_paths, word_occurrence_per_file, user_list, num_keywords, num_queries
        )
        return server_knowledge_dataset, documents_on_server, dataset_stored_on_server
