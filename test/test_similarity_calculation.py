# Imports TestCase class of unittest library
from unittest import TestCase

# Imports SimilarityCalculator
from ikk.similarity_calculation import SimilarityCalculator

# Import pandas and numpy as these libraries are used to define matrices throughout these simulations
import pandas as pd
import numpy as np

# Class TestSimilarityCalculator is used to test the SimilarityCalculator class in similarity_calculation.py
class TestSimilarityCalculator(TestCase):

    # Method setUp initializes a SimilarityCalculator class
    def setUp(self):
        self.calculator = SimilarityCalculator()

    # Method test_calc_metrics tests different settings in the calc_metrics method in similarity_calculation.py
    def test_calc_metrics(self):

        # Defines a 6x6 base matrix
        columns = ["w_1", "w_2", "w_3", "w_4", "w_5", "w_6"]
        rows = columns
        data = np.array(
            [
                [0.02, 0.03, 0.015, 0.006, 0.07, 0.08],
                [0.03, 0.037, 0.017, 0.014, 0.021, 0.018],
                [0.015, 0.017, 0.019, 0.008, 0.0076, 0.0135],
                [0.006, 0.014, 0.008, 0.025, 0.0062, 0.0068],
                [0.07, 0.021, 0.0076, 0.0062, 0.012, 0.0134],
                [0.08, 0.018, 0.0135, 0.0068, 0.0134, 0.029],
            ]
        )
        base_matrix = pd.DataFrame(data, columns=columns, index=rows)

        # Same matrix as the base matrix 'dataset', following assertions test whether the matrices are completely the same
        matrix_2 = pd.DataFrame(data, columns=columns, index=rows)
        metric_1, metric_2, metric_3 = self.calculator.calc_metrics(
            base_matrix, matrix_2
        )
        self.assertEqual(metric_1, 1.0)
        self.assertEqual(metric_2, 1.0)
        self.assertEqual(metric_3, 1.0)

        # Tests if the scores match if only the value of the first cell in the matrix differs (from 0.02 to 0.01) as opposed to the base matrix
        data_new = np.array(
            [
                [0.01, 0.03, 0.015, 0.006, 0.07, 0.08],
                [0.03, 0.037, 0.017, 0.014, 0.021, 0.018],
                [0.015, 0.017, 0.019, 0.008, 0.0076, 0.0135],
                [0.006, 0.014, 0.008, 0.025, 0.0062, 0.0068],
                [0.07, 0.021, 0.0076, 0.0062, 0.012, 0.0134],
                [0.08, 0.018, 0.0135, 0.0068, 0.0134, 0.029],
            ]
        )
        matrix_3 = pd.DataFrame(data_new, columns=columns, index=rows)
        difference_in_scores_squared = 0.0001
        metric_1_manual = (1 - (difference_in_scores_squared / 36)) * ((6 - 0) / 6)
        metric_2_manual = (1 - (difference_in_scores_squared / 36)) * (36 / (6 * 6))
        metric_3_manual = 1 - (difference_in_scores_squared / (6 * 6))
        metric_1, metric_2, metric_3 = self.calculator.calc_metrics(
            base_matrix, matrix_3
        )
        self.assertEqual(metric_1, metric_1_manual)
        self.assertEqual(metric_2, metric_2_manual)
        self.assertEqual(metric_3, metric_3_manual)

        # Tests if the scores match if only the value of the second cell (and because of symmetry the first cell of the second row as well)
        # in the matrix differs (from 0.03 to 0.02) as opposed to the base matrix
        data_new = np.array(
            [
                [0.02, 0.02, 0.015, 0.006, 0.07, 0.08],
                [0.02, 0.037, 0.017, 0.014, 0.021, 0.018],
                [0.015, 0.017, 0.019, 0.008, 0.0076, 0.0135],
                [0.006, 0.014, 0.008, 0.025, 0.0062, 0.0068],
                [0.07, 0.021, 0.0076, 0.0062, 0.012, 0.0134],
                [0.08, 0.018, 0.0135, 0.0068, 0.0134, 0.029],
            ]
        )
        matrix_4 = pd.DataFrame(data_new, columns=columns, index=rows)
        difference_in_scores_squared = 0.01 ** 2 + 0.01 ** 2
        metric_1_manual = (1 - (difference_in_scores_squared / 36)) * ((6 - 0) / 6)
        metric_2_manual = (1 - (difference_in_scores_squared / 36)) * (36 / (6 * 6))
        metric_3_manual = 1 - (difference_in_scores_squared / (6 * 6))
        metric_1, metric_2, metric_3 = self.calculator.calc_metrics(
            base_matrix, matrix_4
        )
        self.assertEqual(metric_1, metric_1_manual)
        self.assertEqual(metric_2, metric_2_manual)
        self.assertEqual(metric_3, metric_3_manual)

        # Tests if the scores match if the first words do not match between the base matrix and matrix_5 (from 'w_1', to 'w_x') as opposed to the base matrix
        columns_new = ["w_x", "w_2", "w_3", "w_4", "w_5", "w_6"]
        rows_new = columns_new

        matrix_5 = pd.DataFrame(data, columns=columns_new, index=rows_new)
        values = [0.02, 0.03, 0.015, 0.006, 0.07, 0.08, 0.03, 0.015, 0.006, 0.07, 0.08]
        difference_in_scores_squared = sum([abs(x) ** 2 for x in values])
        metric_1_manual = (1 - (0 / 25)) * ((6 - 1) / 6)
        metric_2_manual = (1 - (0 / 25)) * (25 / 36)
        metric_3_manual = 1 - (difference_in_scores_squared / (6 * 6))
        metric_1, metric_2, metric_3 = self.calculator.calc_metrics(
            base_matrix, matrix_5
        )
        self.assertEqual(metric_1, metric_1_manual)
        self.assertEqual(metric_2, metric_2_manual)
        self.assertEqual(metric_3, metric_3_manual)
