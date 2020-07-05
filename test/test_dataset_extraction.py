# Imports TestCase class of unittest library
from unittest import TestCase

# Imports Enum QueryDistribution
from ikk.distribution import QueryDistribution

# Imports os library to allow for access to file on the Operating Systems (such as the datasets)
import os

# Imports DatasetExtractor
from ikk.dataset_extraction import DatasetExtractor

# TestCase TestDatasetExtractor tests methods in class DatasetExtractor
class TestDatasetExtractor(TestCase):
    user_list = ["user_a", "user_b", "user_c", "user_d"]

    file_paths = {
        "file_1": {"id": "dataset/user_b/mbox/file_1", "user": "user_b"},
        "file_2": {"id": "dataset/user_a/mbox/file_2", "user": "user_a"},
        "file_3": {"id": "dataset/user_b/mbox/file_3", "user": "user_b"},
        "file_4": {"id": "dataset/user_c/mbox/file_4", "user": "user_c"},
        "file_5": {"id": "dataset/user_c/mbox/file_5", "user": "user_c"},
        "file_6": {"id": "dataset/user_d/mbox/file_6", "user": "user_d"},
        "file_7": {"id": "dataset/user_a/mbox/file_7", "user": "user_a"},
        "file_8": {"id": "dataset/user_b/mbox/file_8", "user": "user_b"},
        "file_9": {"id": "dataset/user_d/mbox/file_9", "user": "user_d"},
        "file_10": {"id": "dataset/user_c/mbox/file_10", "user": "user_c"},
    }

    word_occurrence_per_file = {
        "file_1": {"a": 5, "the": 4, "test": 12},
        "file_2": {"alarm": 1, "the": 8, "number": 1, "first": 2},
        "file_3": {"a": 8},
        "file_4": {"welcome": 2, "the": 6, "test": 4, "to": 8},
        "file_5": {"help": 2, "randomize": 5, "blank": 9},
        "file_6": {"less": 3, "again": 4},
        "file_7": {"games": 1, "creative": 7, "set": 18},
        "file_8": {
            "spelling": 6,
            "name": 3,
            "inspiration": 7,
            "event": 5,
            "product": 4,
        },
        "file_9": {"a": 2, "the": 1, "see": 3, "need": 6},
        "file_10": {"quite": 3, "can": 2, "this": 4},
    }

    # Method setUp initializes a DatasetExtractor class
    def setUp(self):
        self.extractor = DatasetExtractor()

    # Method test_write_to_json tests write_to_json in dataset_extraction.py
    # Not tested as it is assumed to work
    def test_write_to_json(self):
        pass

    # Method test_read_from_json tests read_from_json in dataset_extraction.py
    # Not tested as it is assumed to work
    def test_read_from_json(self):
        pass

    # Method test_find_file_paths_recursively tests find_file_paths_recursively in dataset_extraction.py
    # Not tested as it is assumed to work
    def test_find_find_paths_recursively(self):
        pass

    # Method test_find_file_paths tests find_file_paths in dataset_extraction.py
    def test_find_find_paths(self):
        path_to_ENRON_dataset = os.path.join(os.getcwd(), "Datasets", "ENRON")
        ENRON_sent_mail = self.extractor.find_file_paths(
            path_to_ENRON_dataset, "_sent_mail"
        )
        self.assertEqual(30109, len(ENRON_sent_mail[0]))
        self.assertEqual(150, len(ENRON_sent_mail[1]))

        ENRON_inbox = self.extractor.find_file_paths(path_to_ENRON_dataset, "inbox")
        self.assertEqual(44859, len(ENRON_inbox[0]))
        self.assertEqual(150, len(ENRON_inbox[1]))

        path_to_Apache_dataset = os.path.join(
            os.getcwd(), "Datasets", "ApacheLucene-java-user"
        )
        Apache_mbox = self.extractor.find_file_paths(path_to_Apache_dataset, "mbox")
        self.assertEqual(50116, len(Apache_mbox[0]))
        self.assertEqual(4916, len(Apache_mbox[1]))

    # Method test_extract_word_occurrence_per_file tests extract_word_occurrence_per_file
    # Not tested as it assumed to work
    def test_extract_word_occurrence_per_file(self):
        pass

    # Method test_extract_files_per_word tests
    def test_extract_file_occurrence_per_word(self):
        self.assertEqual(
            sorted(
                list(
                    self.extractor.extract_file_occurrence_per_word(
                        self.word_occurrence_per_file, 4, omit_top=0
                    ).keys()
                )
            ),
            ["a", "set", "test", "the"],
        )
        self.assertEqual(
            sorted(
                list(
                    self.extractor.extract_file_occurrence_per_word(
                        self.word_occurrence_per_file, 5, omit_top=0
                    ).keys()
                )
            ),
            ["a", "blank", "set", "test", "the"],
        )

        for i in range(1, 27):
            self.assertEqual(
                i,
                len(
                    self.extractor.extract_file_occurrence_per_word(
                        self.word_occurrence_per_file, i, omit_top=0
                    )
                ),
            )
        for i in range(1, 27):
            keyword_percentage = 0.7
            if i <= 26 - round((1 - keyword_percentage) * i):
                self.assertEqual(
                    i,
                    len(
                        self.extractor.extract_file_occurrence_per_word(
                            self.word_occurrence_per_file,
                            i,
                            keyword_percentage=keyword_percentage,
                            omit_top=0,
                        )
                    ),
                )
            else:
                with self.assertRaises(AssertionError):
                    self.assertEqual(
                        i,
                        len(
                            self.extractor.extract_file_occurrence_per_word(
                                self.word_occurrence_per_file,
                                i,
                                keyword_percentage=keyword_percentage,
                                omit_top=0,
                            )
                        ),
                    )

    # Method test_querify tests method querify in dataset_extraction.py
    def test_querify(self):
        file_occurrence_per_word = {
            "a": {"amount": 8, "files": ["file_1", "file_2", "file_4"]},
            "the": {"amount": 6, "files": ["file_2", "file_3", "file_4", "file_6"]},
            "test": {"amount": 14, "files": ["file_3", "file_8", "file_4"]},
            "merge": {"amount": 1, "files": ["file_1"]},
        }
        # The tests simply asserts that the length of the dictionary is equal to the input parameters {{ num_queries }}
        for i in range(1, len(file_occurrence_per_word.keys()) + 1):
            self.assertEqual(
                i,
                len(
                    self.extractor.querify(
                        file_occurrence_per_word,
                        i,
                        query_distribution=QueryDistribution.zipfian,
                    )
                ),
            )
            self.assertEqual(
                i,
                len(
                    self.extractor.querify(
                        file_occurrence_per_word,
                        i,
                        query_distribution=QueryDistribution.reverse_zipfian,
                    )
                ),
            )
            self.assertEqual(
                i,
                len(
                    self.extractor.querify(
                        file_occurrence_per_word,
                        i,
                        query_distribution=QueryDistribution.uniform,
                    )
                ),
            )

        with self.assertRaises(AssertionError):
            self.extractor.querify(
                file_occurrence_per_word,
                len(file_occurrence_per_word) + 1,
                query_distribution=QueryDistribution.zipfian,
            )

    # Method test_omit_users tests method omit_users in dataset_extraction.py
    def test_omit_users(self):
        (
            new_file_paths,
            new_word_occurrence_per_file,
            new_user_list,
        ) = self.extractor.omit_users(
            self.file_paths,
            self.word_occurrence_per_file,
            self.user_list,
            document_percentage=0.75,
        )

        self.assertEqual(
            sorted(list(new_file_paths.keys())),
            sorted(list(new_word_occurrence_per_file.keys())),
        )
        if sorted(new_user_list) == ["user_a", "user_b", "user_c"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                [
                    "file_1",
                    "file_10",
                    "file_2",
                    "file_3",
                    "file_4",
                    "file_5",
                    "file_7",
                    "file_8",
                ],
            )
        elif sorted(new_user_list) == ["user_a", "user_b", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_1", "file_2", "file_3", "file_6", "file_7", "file_8", "file_9"],
            )
        elif sorted(new_user_list) == ["user_a", "user_c", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_10", "file_2", "file_4", "file_5", "file_6", "file_7", "file_9"],
            )
        elif sorted(new_user_list) == ["user_b", "user_c", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                [
                    "file_1",
                    "file_10",
                    "file_3",
                    "file_4",
                    "file_5",
                    "file_6",
                    "file_8",
                    "file_9",
                ],
            )
        else:
            raise RuntimeError("Encountered non-existent setting")

        (
            new_file_paths,
            new_word_occurrence_per_file,
            new_user_list,
        ) = self.extractor.omit_users(
            self.file_paths,
            self.word_occurrence_per_file,
            self.user_list,
            document_percentage=0.44,
        )
        self.assertEqual(
            sorted(list(new_file_paths.keys())),
            sorted(list(new_word_occurrence_per_file.keys())),
        )
        if sorted(new_user_list) == ["user_a", "user_b"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_1", "file_2", "file_3", "file_7", "file_8"],
            )
        elif sorted(new_user_list) == ["user_a", "user_c"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_10", "file_2", "file_4", "file_5", "file_7"],
            )
        elif sorted(new_user_list) == ["user_a", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_2", "file_6", "file_7", "file_9"],
            )
        elif sorted(new_user_list) == ["user_b", "user_c"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_1", "file_10", "file_3", "file_4", "file_5", "file_8"],
            )
        elif sorted(new_user_list) == ["user_b", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_1", "file_3", "file_6", "file_8", "file_9"],
            )
        elif sorted(new_user_list) == ["user_c", "user_d"]:
            self.assertEqual(
                sorted(list(new_file_paths.keys())),
                ["file_10", "file_4", "file_5", "file_6", "file_9"],
            )
        else:
            raise RuntimeError("Encountered non-existent setting")

    # Method read_dataset tests read_dataset in dataset_extraction.py
    # Not tested as it is assumed to work
    def read_dataset(self):
        pass

    # Method test_get_dataset tests get_dataset in dataset_extraction.py
    # It tests:
    # - (key)word deletion
    # - (document) deletion
    # - (reverse) Zipfian/Uniform distribution querification
    # - amount of omitted (most occurring) words
    # - error usage
    def test_get_dataset(self):
        file_paths = self.file_paths
        word_occurrence_per_file = self.word_occurrence_per_file
        user_list = self.user_list

        # Parameters
        num_keywords = 10
        num_queries = 5

        # Base case
        base_file_occurrence_per_word, base_docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=1.0,
            querify=False,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertEqual(10, len(set(base_docs)))
        self.assertEqual(num_keywords, len(set(base_file_occurrence_per_word.keys())))

        # Test document percentage
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=0.8,
            keyword_percentage=1.0,
            querify=False,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertLess(len(docs), len(file_paths))
        with self.assertRaises(AssertionError):
            file_occurrence_per_word, docs = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_queries,
                document_percentage=0.1,
                keyword_percentage=1.0,
                querify=False,
                query_distribution=QueryDistribution.zipfian,
                omit_top=0,
            )

        # Test keyword percentage
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=0.9,
            querify=False,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertEqual(len(file_occurrence_per_word), num_keywords)
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=0.1,
            querify=False,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertEqual(len(file_occurrence_per_word), num_keywords)
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            20,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=0.9,
            querify=False,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertEqual(len(file_occurrence_per_word), 20)
        with self.assertRaises(AssertionError):
            file_occurrence_per_word, docs = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                20,
                num_queries,
                document_percentage=1.0,
                keyword_percentage=0.5,
                querify=False,
                query_distribution=QueryDistribution.zipfian,
                omit_top=0,
            )

        # Test querification and different distributions
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=1.0,
            querify=True,
            query_distribution=QueryDistribution.zipfian,
            omit_top=0,
        )
        self.assertNotEqual(len(file_occurrence_per_word), num_keywords)
        self.assertEqual(len(file_occurrence_per_word), num_queries)
        with self.assertRaises(AssertionError):
            file_occurrence_per_word, docs = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_keywords + 1,
                document_percentage=1.0,
                keyword_percentage=1.0,
                querify=True,
                query_distribution=QueryDistribution.zipfian,
                omit_top=0,
            )

        count_zipfian = 0
        count_reverse_zipfian = 0
        count_uniform = 0
        for i in range(0, 100):
            zipfian_result = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_queries,
                document_percentage=1.0,
                keyword_percentage=1.0,
                querify=True,
                query_distribution=QueryDistribution.zipfian,
                omit_top=0,
            )

            # Asserts either one of these words (or both) occurs in the result set at least 95% of the time
            if "the" in zipfian_result[0].keys() or "set" in zipfian_result[0].keys():
                count_zipfian += 1

            reverse_zipfian_result = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_queries,
                document_percentage=1.0,
                keyword_percentage=1.0,
                querify=True,
                query_distribution=QueryDistribution.reverse_zipfian,
                omit_top=0,
            )

            # Asserts either one of these words (or both) occurs in the result set at least 95% of the time
            if (
                "need" in reverse_zipfian_result[0].keys()
                or "spelling" in reverse_zipfian_result[0].keys()
            ):
                count_reverse_zipfian += 1

            uniform_result = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_queries,
                document_percentage=1.0,
                keyword_percentage=1.0,
                querify=True,
                query_distribution=QueryDistribution.uniform,
                omit_top=0,
            )

            # Asserts these keywords occur almost half of the time (len(keywords) = 2*len(queries))
            if "the" in uniform_result[0].keys():
                count_uniform += 1
            if "set" in uniform_result[0].keys():
                count_uniform += 1
            if "need" in uniform_result[0].keys():
                count_uniform += 1
            if "spelling" in uniform_result[0].keys():
                count_uniform += 1

        self.assertGreaterEqual(count_zipfian, 95)
        self.assertGreaterEqual(count_reverse_zipfian, 95)
        count_uniform = count_uniform / 4
        self.assertTrue(45 < count_uniform and count_uniform < 55)

        # omit_top
        file_occurrence_per_word, docs = self.extractor.get_dataset(
            file_paths,
            word_occurrence_per_file,
            user_list,
            num_keywords,
            num_queries,
            document_percentage=1.0,
            keyword_percentage=1.0,
            querify=False,
            query_distribution=QueryDistribution.reverse_zipfian,
            omit_top=26 - num_keywords,
        )
        self.assertEqual(len(file_occurrence_per_word), num_keywords)
        with self.assertRaises(AssertionError):
            file_occurrence_per_word, docs = self.extractor.get_dataset(
                file_paths,
                word_occurrence_per_file,
                user_list,
                num_keywords,
                num_queries,
                document_percentage=1.0,
                keyword_percentage=1.0,
                querify=False,
                query_distribution=QueryDistribution.reverse_zipfian,
                omit_top=26 - num_keywords + 1,
            )

    # Method test_get_background_knowledge tests get_background_knowledge in dataset_extraction.py
    # Not tested as it is assumed to work
    def test_get_background_knowledge(self):
        pass

    # Method test_get_server_knowledge tests get_server_knowledge in dataset_extraction.py
    # Not tested as it is assumed to work
    def test_get_server_knowledge(self):
        pass
