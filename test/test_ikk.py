# Imports TestCase class of unittest library
from unittest import TestCase

# Imports pandas library used to express matrices
import pandas as pd

# Imports IKK
from ikk.ikk import IKK

# TestCase TestIKK tests methods in class IKK
class TestIKK(TestCase):
    server_knowledge_docs = [
        "d_1",
        "d_2",
        "d_3",
        "d_4",
        "d_5",
        "d_6",
        "d_7",
        "d_8",
        "d_9",
        "d_10",
    ]
    server_knowledge_queries = ["q_1", "q_2", "q_3"]
    server_knowledge_index = [
        [False, False, False, False, True, False, False, False, False, True],
        [False, True, False, False, True, True, False, False, True, False],
        [True, False, True, True, False, True, True, True, False, False],
    ]
    server_knowledge_index = pd.DataFrame(
        data=server_knowledge_index,
        index=server_knowledge_queries,
        columns=server_knowledge_docs,
    )

    background_knowledge_docs = ["d_1", "d_2", "d_4", "d_5", "d_6", "d_7", "d_8", "d_9"]
    background_knowledge_keywords = ["k_1", "k_2", "k_3", "k_4", "k_5", "k_6", "k_7"]
    background_knowledge_index = [
        [False, False, True, True, False, False, False, True],
        [True, False, False, True, False, False, False, False],
        [False, False, False, False, False, False, True, False],
        [False, True, False, False, False, False, False, True],
        [False, False, True, True, False, True, True, False],
        [False, True, True, False, False, False, True, False],
        [True, True, True, True, True, True, True, True],
    ]
    background_knowledge_index = pd.DataFrame(
        data=background_knowledge_index,
        index=background_knowledge_keywords,
        columns=background_knowledge_docs,
    )

    server_knowledge_cooccurrence_matrix = [
        [0.2, 0.1, 0.0],
        [0.1, 0.4, 0.1],
        [0.0, 0.1, 0.6],
    ]
    server_knowledge_cooccurrence_matrix = pd.DataFrame(
        data=server_knowledge_cooccurrence_matrix,
        index=server_knowledge_queries,
        columns=server_knowledge_queries,
    )

    background_knowledge_cooccurrence_matrix = [
        [0.375, 0.125, 0.000, 0.125, 0.250, 0.125, 0.375],
        [0.125, 0.250, 0.000, 0.000, 0.125, 0.000, 0.250],
        [0.000, 0.000, 0.125, 0.000, 0.125, 0.125, 0.125],
        [0.125, 0.000, 0.000, 0.250, 0.000, 0.125, 0.250],
        [0.250, 0.125, 0.125, 0.000, 0.500, 0.250, 0.500],
        [0.125, 0.000, 0.125, 0.125, 0.250, 0.375, 0.375],
        [0.375, 0.250, 0.125, 0.250, 0.500, 0.375, 1.000],
    ]
    background_knowledge_cooccurrence_matrix = pd.DataFrame(
        data=background_knowledge_cooccurrence_matrix,
        index=background_knowledge_keywords,
        columns=background_knowledge_keywords,
    )

    server_knowledge_docs_2 = [
        "d_1",
        "d_2",
        "d_3",
        "d_4",
        "d_5",
        "d_6",
        "d_7",
        "d_8",
        "d_9",
        "d_10",
    ]
    server_knowledge_queries_2 = ["q_1", "q_2", "q_3"]
    server_knowledge_index_2 = [
        [False, False, False, False, False, False, False, False, False, True],
        [False, False, False, False, False, False, False, False, True, False],
        [True, True, True, True, True, True, True, True, True, True],
    ]
    server_knowledge_index_2 = pd.DataFrame(
        data=server_knowledge_index_2,
        index=server_knowledge_queries_2,
        columns=server_knowledge_docs_2,
    )

    background_knowledge_docs_2 = [
        "d_1",
        "d_2",
        "d_4",
        "d_5",
        "d_6",
        "d_7",
        "d_8",
        "d_9",
    ]
    background_knowledge_keywords_2 = ["k_1", "k_2", "k_3", "k_4", "k_5"]
    background_knowledge_index_2 = [
        [False, False, False, False, False, False, False, True],
        [False, False, False, False, False, False, True, False],
        [False, False, False, False, False, True, False, False],
        [False, False, False, False, True, False, False, False],
        [False, False, False, True, False, False, False, False],
    ]
    background_knowledge_index_2 = pd.DataFrame(
        data=background_knowledge_index_2,
        index=background_knowledge_keywords_2,
        columns=background_knowledge_docs_2,
    )

    # Method setUp initializes an IKK class
    def setUp(self):
        self.ikk = IKK()

    # Method test_find_occurrence_dicts tests whether the occurrence dicts are generated correctly by find_occurrence_dicts in ikk.py
    # Some asserts in find_occurrence_dicts are also used to ensure correctly generated occurrence dicts
    def test_find_occurrence_dicts(self):
        query_in_range_dict, keyword_in_range_dict = self.ikk.find_occurrence_dicts(
            self.server_knowledge_index, self.background_knowledge_index
        )

        self.assertEqual(
            sorted(query_in_range_dict["q_1"]),
            ["k_1", "k_2", "k_3", "k_4", "k_5", "k_6"],
        )
        self.assertEqual(
            sorted(query_in_range_dict["q_2"]),
            ["k_1", "k_2", "k_3", "k_4", "k_5", "k_6"],
        )
        self.assertEqual(
            sorted(query_in_range_dict["q_3"]),
            ["k_1", "k_2", "k_4", "k_5", "k_6", "k_7"],
        )

        self.assertEqual(sorted(keyword_in_range_dict["k_1"]), ["q_1", "q_2", "q_3"])
        self.assertEqual(sorted(keyword_in_range_dict["k_2"]), ["q_1", "q_2", "q_3"])
        self.assertEqual(sorted(keyword_in_range_dict["k_3"]), ["q_1", "q_2"])
        self.assertEqual(sorted(keyword_in_range_dict["k_4"]), ["q_1", "q_2", "q_3"])
        self.assertEqual(sorted(keyword_in_range_dict["k_5"]), ["q_1", "q_2", "q_3"])
        self.assertEqual(sorted(keyword_in_range_dict["k_6"]), ["q_1", "q_2", "q_3"])
        self.assertEqual(sorted(keyword_in_range_dict["k_7"]), ["q_3"])

        query_in_range_dict, keyword_in_range_dict = self.ikk.find_occurrence_dicts(
            self.server_knowledge_index_2, self.background_knowledge_index_2
        )
        self.assertEqual(
            sorted(query_in_range_dict["q_1"]), ["k_1", "k_2", "k_3", "k_4", "k_5"]
        )
        self.assertEqual(
            sorted(query_in_range_dict["q_2"]), ["k_1", "k_2", "k_3", "k_4", "k_5"]
        )
        self.assertEqual(query_in_range_dict["q_3"], None)

        self.assertEqual(sorted(keyword_in_range_dict["k_1"]), ["q_1", "q_2"])
        self.assertEqual(sorted(keyword_in_range_dict["k_2"]), ["q_1", "q_2"])
        self.assertEqual(sorted(keyword_in_range_dict["k_3"]), ["q_1", "q_2"])
        self.assertEqual(sorted(keyword_in_range_dict["k_4"]), ["q_1", "q_2"])
        self.assertEqual(sorted(keyword_in_range_dict["k_5"]), ["q_1", "q_2"])

    # Method test_fill_deterministic_init_state tests the deterministic_init_state method in ikk.py which is used by method optimizer to
    #   set an initial state which takes the occurrence count of words into regard
    def test_deterministic_init_state(self):
        query_in_range_dict, keyword_in_range_dict = self.ikk.find_occurrence_dicts(
            self.server_knowledge_index, self.background_knowledge_index
        )
        for i in range(0, 1000):
            init_state = self.ikk.deterministic_init_state(
                query_in_range_dict, self.background_knowledge_keywords.copy()
            )
            self.assertNotEqual(init_state["q_1"], "k_7")
            self.assertNotEqual(init_state["q_2"], "k_7")
            self.assertNotEqual(init_state["q_3"], "k_3")

        query_in_range_dict, keyword_in_range_dict = self.ikk.find_occurrence_dicts(
            self.server_knowledge_index_2, self.background_knowledge_index_2
        )
        value_list = self.background_knowledge_keywords_2.copy()
        init_state = self.ikk.deterministic_init_state(query_in_range_dict, value_list)

        self.assertIsNotNone(init_state["q_1"])
        self.assertIsNotNone(init_state["q_2"])
        self.assertIsNone(init_state["q_3"])

        query_in_range_dict = {
            "q_1": ["k_1", "k_2", "k_3"],
            "q_2": ["k_1", "k_2", "k_3"],
            "q_3": ["k_1", "k_2", "k_3"],
            "q_4": ["k_1", "k_2", "k_3"],
        }
        value_list = ["k_1", "k_2", "k_3"]
        init_state = self.ikk.deterministic_init_state(query_in_range_dict, value_list)

        self.assertIsNotNone(init_state["q_1"])
        self.assertIsNotNone(init_state["q_2"])
        self.assertIsNotNone(init_state["q_3"])
        self.assertIsNone(init_state["q_4"])

    # Method test_fill_init_state tests the fill_init_state method in ikk.py which is used by method optimizer to set
    #   an initial state for the Simulated Annealing algorithm (ANNEAL)
    def test_fill_init_state(self):
        domain_list = self.background_knowledge_index.index.tolist()
        variable_list = self.server_knowledge_index.index.tolist()

        # The following block of code generates the initial state in case of the IKK algorithm as proposed by IKK et al. their paper
        init_state = self.ikk.fill_init_state({}, domain_list.copy(), variable_list)
        self.assertEqual(type(init_state), type({}))
        self.assertEqual(len(init_state), 3)
        self.assertEqual(len(init_state.values()), 3)

        # The following block of code generates the initial state and in_range_dicts as proposed in our 'deterministic IKK' algorithm
        # This means the initial state is not chosen at random
        result = self.ikk.fill_init_state(
            {},
            domain_list.copy(),
            variable_list,
            server_knowledge_index=self.server_knowledge_index,
            background_knowledge_index=self.background_knowledge_index,
        )
        init_state, query_in_range_dict, keyword_in_range_dict = (
            result[0],
            result[1],
            result[2],
        )
        self.assertNotEqual(type(result), type({}))
        self.assertEqual(type(init_state), type({}))
        self.assertEqual(len(init_state), 3)
        self.assertEqual(type(query_in_range_dict), type({}))
        self.assertEqual(len(query_in_range_dict), 3)
        self.assertEqual(type(keyword_in_range_dict), type({}))
        self.assertEqual(len(keyword_in_range_dict), 7)

        # Tests that mappings 'q_1': 'k_7', 'q_2': 'k_7' and 'q_3': 'k_3' will never occur
        for i in range(0, 10000):
            result = self.ikk.fill_init_state(
                {},
                domain_list.copy(),
                variable_list,
                server_knowledge_index=self.server_knowledge_index,
                background_knowledge_index=self.background_knowledge_index,
            )
            init_state = result[0]
            if "q_1" in init_state.keys():
                self.assertNotEqual(init_state["q_1"], "k_7")
            elif "q_2" in init_state.keys():
                self.assertNotEqual(init_state["q_2"], "k_7")
            elif "q_3" in init_state.keys():
                self.assertNotEqual(init_state["q_3"], "k_3")

        # Tests the situation where a query has no keywords within range in the IKK method, so every query should still be assigned a non-None keyword
        domain_list = self.background_knowledge_index_2.index.tolist()
        variable_list = self.server_knowledge_index_2.index.tolist()
        init_state = self.ikk.fill_init_state({}, domain_list.copy(), variable_list)
        self.assertIsNotNone(init_state["q_1"])
        self.assertIsNotNone(init_state["q_2"])
        self.assertIsNotNone(init_state["q_3"])

        # Tests the situation where a query has no keywords within range in the Deterministic IKK method, so each of these queries is assigned the value None
        result = self.ikk.fill_init_state(
            {},
            domain_list.copy(),
            variable_list,
            server_knowledge_index=self.server_knowledge_index_2,
            background_knowledge_index=self.background_knowledge_index_2,
        )
        init_state, query_in_range_dict, keyword_in_range_dict = (
            result[0],
            result[1],
            result[2],
        )
        self.assertEqual(
            query_in_range_dict["q_1"], ["k_1", "k_2", "k_3", "k_4", "k_5"]
        )
        self.assertEqual(query_in_range_dict["q_3"], None)
        self.assertIsNotNone(init_state["q_1"])
        self.assertIsNotNone(init_state["q_2"])
        self.assertIsNone(init_state["q_3"])

    # Method test_optimizer tests method optimizer in ikk.py
    # This method is not implemented as we assume it works correctly
    def test_optimizer(self):
        pass

    # Method test_remove_None_queries tests method remove_None_queries in ikk.py
    def test_remove_None_queries(self):
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_3"}
        none_assigned_queries, new_current_state = self.ikk.remove_None_queries(
            current_state
        )
        self.assertEqual(none_assigned_queries, [])
        self.assertEqual(current_state, new_current_state)
        self.assertEqual(
            len(none_assigned_queries) + len(new_current_state), len(current_state)
        )

        current_state["q_2"] = None
        none_assigned_queries, new_current_state = self.ikk.remove_None_queries(
            current_state
        )
        self.assertEqual(none_assigned_queries, ["q_2"])
        self.assertNotEqual(current_state, new_current_state)
        self.assertEqual(
            len(none_assigned_queries) + len(new_current_state), len(current_state)
        )

    # Method test_find_squared_Euclidean_distance tests method find_squared_Euclidean_distance in ikk.py
    def test_find_squared_Euclidean_distance(self):
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_3"}
        euc_dist = self.ikk.find_squared_Euclidean_distance(
            current_state,
            self.server_knowledge_cooccurrence_matrix,
            self.background_knowledge_cooccurrence_matrix,
        )
        self.assertAlmostEqual(euc_dist, 0.3)

        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_4"}
        euc_dist = self.ikk.find_squared_Euclidean_distance(
            current_state,
            self.server_knowledge_cooccurrence_matrix,
            self.background_knowledge_cooccurrence_matrix,
        )
        self.assertAlmostEqual(euc_dist, 0.228125)

    # Method test_choose_new_state tests method choose_new_state in ikk.py
    def test_choose_new_state(self):

        # Tests IKK method (completely random, without using relative document occurrence of keywords/queries) to choose a new state
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_3"}
        reversed_current_state = dict((v, k) for k, v in current_state.items())
        domain_list = ["k_1", "k_2", "k_3", "k_4", "k_5", "k_6", "k_7"]
        (
            next_state,
            reversed_next_state,
            random_query,
            random_query_2,
        ) = self.ikk.choose_new_state(
            current_state, reversed_current_state, domain_list
        )

        self.assertNotEqual(current_state, next_state)
        self.assertNotEqual(reversed_current_state, reversed_next_state)
        self.assertEqual(current_state.keys(), next_state.keys())
        self.assertEqual(
            reversed_next_state, dict((v, k) for k, v in next_state.items())
        )
        self.assertNotEqual(current_state[random_query], next_state[random_query])
        if random_query_2 is None:
            next_state_not_changed = sorted(
                [
                    (query, keyword)
                    for query, keyword in next_state.items()
                    if query != random_query
                ]
            )
            current_state_not_changed = sorted(
                [
                    (query, keyword)
                    for query, keyword in current_state.items()
                    if query != random_query
                ]
            )
            self.assertEqual(
                len(next_state_not_changed), len(current_state_not_changed)
            )
            self.assertEqual(len(next_state_not_changed), len(next_state) - 1)
            self.assertEqual(next_state_not_changed, current_state_not_changed)
        else:
            self.assertNotEqual(
                current_state[random_query_2], next_state[random_query_2]
            )
            self.assertEqual(current_state[random_query_2], next_state[random_query])
            self.assertEqual(next_state[random_query_2], current_state[random_query])
            next_state_not_changed = sorted(
                [
                    (query, keyword)
                    for query, keyword in next_state.items()
                    if query != random_query and query != random_query_2
                ]
            )
            current_state_not_changed = sorted(
                [
                    (query, keyword)
                    for query, keyword in current_state.items()
                    if query != random_query and query != random_query_2
                ]
            )
            self.assertEqual(
                len(next_state_not_changed), len(current_state_not_changed)
            )
            self.assertEqual(len(next_state_not_changed), len(next_state) - 2)
            self.assertEqual(next_state_not_changed, current_state_not_changed)

        # Test 'Deterministic' IKK method (new states are chosen not completely at random but with the relative document occurrence of
        #   keywords/queries in mind)
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_4"}
        none_assigned_queries, current_state = self.ikk.remove_None_queries(
            current_state
        )
        self.assertEqual(none_assigned_queries, [])
        reversed_current_state = dict((v, k) for k, v in current_state.items())
        domain_list = ["k_1", "k_2", "k_3", "k_4", "k_5", "k_6", "k_7"]
        query_in_range_dict, keyword_in_range_dict = self.ikk.find_occurrence_dicts(
            self.server_knowledge_index, self.background_knowledge_index
        )

        # Tests that mappings 'q_1': 'k_7', 'q_2': 'k_7' and 'q_3': 'k_3' will never occur
        for i in range(0, 10000):

            (
                next_state,
                reversed_next_state,
                random_query,
                random_query_2,
            ) = self.ikk.choose_new_state(
                current_state,
                reversed_current_state,
                domain_list,
                query_in_range_dict,
                keyword_in_range_dict,
            )
            self.assertNotEqual(current_state, next_state)
            self.assertNotEqual(reversed_current_state, reversed_next_state)
            self.assertEqual(current_state.keys(), next_state.keys())
            self.assertEqual(
                reversed_next_state, dict((v, k) for k, v in next_state.items())
            )
            if random_query_2 is None:
                next_state_not_changed = sorted(
                    [
                        (query, keyword)
                        for query, keyword in next_state.items()
                        if query != random_query
                    ]
                )
                current_state_not_changed = sorted(
                    [
                        (query, keyword)
                        for query, keyword in current_state.items()
                        if query != random_query
                    ]
                )
                self.assertEqual(
                    len(next_state_not_changed), len(current_state_not_changed)
                )
                self.assertEqual(len(next_state_not_changed), len(next_state) - 1)
                self.assertEqual(next_state_not_changed, current_state_not_changed)
            else:
                next_state_not_changed = sorted(
                    [
                        (query, keyword)
                        for query, keyword in next_state.items()
                        if query != random_query and query != random_query_2
                    ]
                )
                current_state_not_changed = sorted(
                    [
                        (query, keyword)
                        for query, keyword in current_state.items()
                        if query != random_query and query != random_query_2
                    ]
                )
                self.assertEqual(
                    len(next_state_not_changed), len(current_state_not_changed)
                )
                self.assertEqual(len(next_state_not_changed), len(next_state) - 2)
                self.assertEqual(next_state_not_changed, current_state_not_changed)

            self.assertFalse(next_state["q_1"] == "k_7")
            self.assertFalse(next_state["q_2"] == "k_7")
            self.assertFalse(next_state["q_3"] == "k_3")

    # Method test_calculate_cost_change tests method calculate_cost_change in ikk.py
    def test_calculate_cost_change(self):

        # Tests 1 mapping changed
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_3"}
        next_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_4"}
        query_1 = "q_3"
        query_2 = None
        cost_change_old, cost_change_new = self.ikk.calculate_cost_change(
            current_state,
            next_state,
            self.server_knowledge_cooccurrence_matrix,
            self.background_knowledge_cooccurrence_matrix,
            query_1,
            query_2,
        )

        self.assertAlmostEqual(
            0.245625, cost_change_old
        )  # AlmostEqual as Python floats behave a bit weird
        self.assertAlmostEqual(0.17375, cost_change_new)

        # Tests 2 mappings changed
        current_state = {"q_1": "k_1", "q_2": "k_2", "q_3": "k_3"}
        next_state = {"q_1": "k_1", "q_2": "k_3", "q_3": "k_2"}
        query_1 = "q_3"
        query_2 = "q_2"
        cost_change_old, cost_change_new = self.ikk.calculate_cost_change(
            current_state,
            next_state,
            self.server_knowledge_cooccurrence_matrix,
            self.background_knowledge_cooccurrence_matrix,
            query_1,
            query_2,
        )

        self.assertAlmostEqual(
            0.269375, cost_change_old
        )  # AlmostEqual as Python floats behave a bit weird
        self.assertAlmostEqual(0.269375, cost_change_new)

    # Method test_accept_new_state tests method accept_new_state in ikk.py
    # This method is not implemented as we assume it works correctly
    def test_accept_new_state(self):
        pass

    # Method test_merge_queries tests method merge_queries in ikk.py
    # This method is not implemented as we assume it works correctly
    def test_merge_queries(self):
        pass

    # Method test_ANNEAL tests method otimizer method in ikk.py
    # This method is not implemented as we assume it works correctly
    def test_ANNEAL(self):
        pass
