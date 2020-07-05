# Class SimilarityCalculator computes three similarity metrics on two (pd.DataFrame) cooccurrence matrices
# Metric 1 calculates the similarity score by:
# 	1) Finding the total squared Euclidean distance between cells that occur in both matrices
# 	   If cell [row = 'a', column = 'b'] (due to similarity cell [row = 'b', column = 'a'] also is present) occurs in both matrices:
# 	   Total Euclidean distance squared += abs(matrix_1[row = 'a', column = 'b'] - matrix_2[row = 'a', column = 'b'])**2
# 	2) The total score squared Euclidean distance is divided by the total amount of cells that occur in both matrices
#            (ensures the score is always between 0 and 1)
# 	3) At this moment a higher average Euclidean distance squared means that the matrices are less similar thus
#            we reverse the score metric by subtracting the score from 1
# 	4) To include the cells that do not occur in both matrices we take the amount of words that are not featured on the axis of both (symmetric) matrices
# 	   This value is subtracted from the total amount of words that are featured on the axis of both matrices (dimensions of the matrices are the same)
#            and normalized by dividing the result with the total amount of words featured on the axis of the matrices
# 	5) We obtain a similarity score from matrix_1 to matrix_2 which is between 0 and 1. 1 means the matrices are completely similar, whereas
#             0 means they are completely not the same

# Metric 2 calculates the similarity score by:
# 	1) Repeating steps 1, 2 and 3 from Metric 1
# 	2) Instead of using the percentage of words featured in both matrices we use the total amount of overlapping cells by computing
#            the total amount of overlapping cells (as before) and dividing this amount by the total amount of cells in both (symmetric) matrices and
#            multiply this value with the average Euclidean distance obtained in step 1).
# 	3) We obtain a similarity score from matrix_1 to matrix_2 which is between 0 and 1. 1 means the matrices are completely similar,
#            0 means they are completely not the same

# Metric 3 calculates the similarity score by:
# 	1) Repeating step 1 from Metric 1
# 	2) Adding the Euclidean distance squared values from all cells in matrix 1 that don't occur in matrix 2. We assume all values are
#            0 in matrix 2 for simplicity sake
# 	3) The value obtained in step 2 is normalized by dividing it by the total amount of cells in matrix 1 (and matrix 2 as the dimensions are the same)
# 	4) We obtain a similarity score from matrix_1 to matrix_2 which is between 0 and 1. 1 means the matrices are completely similar,
#            0 means they are completely not the same
class SimilarityCalculator:
    def calc_metrics(self, matrix_1, matrix_2):
        score = 0
        score_euc_dist = 0
        rows = matrix_1.index.values.tolist()
        columns = matrix_1.columns.tolist()
        non_overlapping_words = 0
        overlapping_cells = 0
        dimensions = len(rows) * len(columns)
        for row in rows:
            try:
                matrix_2.loc[row, :]
            except:
                non_overlapping_words += 1
            for column in columns:
                value_1 = matrix_1.loc[row, column]
                try:
                    value_2 = matrix_2.loc[row, column]
                    overlapping_cells += 1
                    score += (abs(value_1 - value_2)) ** 2
                    score_euc_dist += (abs(value_1 - value_2)) ** 2
                except Exception as e:
                    score_euc_dist += (abs(value_1)) ** 2
        if overlapping_cells != 0:
            score_1 = (1 - (score / overlapping_cells)) * (
                (len(rows) - non_overlapping_words) / len(rows)
            )
            score_2 = (1 - (score / overlapping_cells)) * (
                overlapping_cells / dimensions
            )
            score_3 = 1 - (score_euc_dist / dimensions)
            return score_1, score_2, score_3
        else:
            return 0, 0, 0
