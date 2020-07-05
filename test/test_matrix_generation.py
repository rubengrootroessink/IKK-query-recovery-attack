# Imports TestCase class of unittest library
from unittest import TestCase

# Imports MatrixGenerator
from ikk.matrix_generation import MatrixGenerator

# Class TestGenerateMatrix is used to test the GenerateMatrix class in matrix_generation.py
class TestGenerateMatrix(TestCase):

    # Test files
    file_per_word_occurrence = {
        "the": ["file_1", "file_2", "file_4", "file_9"],
        "set": ["file_7"],
        "test": ["file_1", "file_4"],
        "a": ["file_1", "file_3", "file_9"],
        "blank": ["file_5"],
        "to": ["file_4"],
        "inspiration": ["file_8"],
        "creative": ["file_7"],
        "need": ["file_9"],
        "spelling": ["file_8"],
    }

    document_list = [
        "file_1",
        "file_2",
        "file_3",
        "file_4",
        "file_5",
        "file_6",
        "file_7",
        "file_8",
        "file_9",
        "file_10",
    ]

    # Method setUp initializes a MatrixGenerator class
    def setUp(self):
        self.generator = MatrixGenerator()

    # Method test_generate_inverted_index tests the generate_inverted_index method in matrix_generation.py
    def test_generate_inverted_index(self):
        inverted_index = self.generator.generate_inverted_index(
            self.file_per_word_occurrence, self.document_list
        )

        true_pairs = [
            ("the", "file_1"),
            ("the", "file_2"),
            ("the", "file_4"),
            ("the", "file_9"),
            ("set", "file_7"),
            ("test", "file_1"),
            ("test", "file_4"),
            ("a", "file_1"),
            ("a", "file_3"),
            ("a", "file_9"),
            ("blank", "file_5"),
            ("to", "file_4"),
            ("inspiration", "file_8"),
            ("creative", "file_7"),
            ("need", "file_9"),
            ("spelling", "file_8"),
        ]

        columns = self.document_list
        self.assertEqual(sorted(columns), sorted(list(inverted_index.columns)))

        rows = [
            "the",
            "set",
            "test",
            "a",
            "blank",
            "to",
            "inspiration",
            "creative",
            "need",
            "spelling",
        ]
        self.assertEqual(sorted(rows), sorted(list(inverted_index.index)))

        for row in rows:
            for column in columns:
                if (row, column) in true_pairs:
                    self.assertTrue(inverted_index.loc[row, column])
                else:
                    self.assertFalse(inverted_index.loc[row, column])

        self.inverted_index = inverted_index

    # Method test_generate_cooccurrence_matrix tests the generate_cooccurrence_matrix method in matrix_generation.py
    def test_generate_cooccurrence_matrix(self):
        inverted_index = self.generator.generate_inverted_index(
            self.file_per_word_occurrence, self.document_list
        )
        cooc_matrix = self.generator.generate_cooccurrence_matrix(inverted_index)

        overlapping_pairs = {
            "the": {"test": 2, "a": 2, "to": 1, "need": 1, "the": 4},
            "test": {"the": 2, "a": 1, "to": 1, "test": 2},
            "a": {"test": 1, "the": 2, "need": 1, "a": 3},
            "set": {"creative": 1, "set": 1},
            "creative": {"set": 1, "creative": 1},
            "to": {"test": 1, "the": 1, "to": 1},
            "blank": {"blank": 1},
            "inspiration": {"spelling": 1, "inspiration": 1},
            "need": {"the": 1, "a": 1, "need": 1},
            "spelling": {"inspiration": 1, "spelling": 1},
        }

        rows = [
            "the",
            "set",
            "test",
            "a",
            "blank",
            "to",
            "inspiration",
            "creative",
            "need",
            "spelling",
        ]
        self.assertEqual(sorted(rows), sorted(list(cooc_matrix.index)))
        self.assertEqual(sorted(rows), sorted(list(cooc_matrix.columns)))

        # Asserts perfect symmetry
        for row in rows:
            for row_2 in rows:
                self.assertEqual(
                    cooc_matrix.loc[row, row_2], cooc_matrix.loc[row_2, row]
                )

                if row in overlapping_pairs.keys():
                    if row_2 in overlapping_pairs[row].keys():
                        self.assertEqual(
                            cooc_matrix.loc[row, row_2],
                            overlapping_pairs[row][row_2] / 10,
                        )
                    else:
                        self.assertEqual(cooc_matrix.loc[row, row_2], 0.0)
                else:
                    self.assertEqual(cooc_matrix.loc[row, row_2], 0.0)

    # Method test_add_gaussian_noise tests the add_gaussian_noise method in matrix_generation.py
    def test_add_gaussian_noise(self):
        inverted_index = self.generator.generate_inverted_index(
            self.file_per_word_occurrence, self.document_list
        )
        cooc_matrix = self.generator.generate_cooccurrence_matrix(inverted_index)
        rows = [
            "the",
            "set",
            "test",
            "a",
            "blank",
            "to",
            "inspiration",
            "creative",
            "need",
            "spelling",
        ]

        mu = (27 / 10) / 55
        values = [4, 2, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        sigma_squared = sum([(x / 10 - mu) ** 2 for x in values]) / 55

        for noise in range(0, 20):
            C = noise / 5
            noisy_cooc_matrix = self.generator.generate_cooccurrence_matrix(
                inverted_index, gaussian_noise_constant=C
            )
            significance = 0
            for decimals in range(-10, 10):
                if round(C * sigma_squared, decimals) != 0.0:
                    significance = decimals
                    break

            for row in rows:
                for row_2 in rows:
                    if C == 0.0:
                        self.assertEqual(
                            cooc_matrix.loc[row, row_2],
                            noisy_cooc_matrix.loc[row, row_2],
                        )
                    self.assertEqual(
                        cooc_matrix.loc[row, row_2], cooc_matrix.loc[row_2, row]
                    )
                    self.assertAlmostEqual(
                        cooc_matrix.loc[row, row_2],
                        noisy_cooc_matrix.loc[row, row_2],
                        significance - 2,
                    )
