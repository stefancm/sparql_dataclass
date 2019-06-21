from unittest import TestCase
from sparql_dataclass import *


class TestSparqlFluentContext(TestCase):
    def test_cannot_instantiate_ResultContainer(self):
        with self.assertRaises(TypeError):
            ResultContainer()

    def test_cannot_inherit_ResultContainer(self):
        class InheritingClass(ResultContainer):
            prop1:str

        with self.assertRaises(TypeError):
            InheritingClass()

    def test_result_container_when_non_dataclass_type_provided_then_assertion_error(self):
        class TestNonDataClass:
            prop1:str

        with self.assertRaises(AssertionError):
            result_container(TestNonDataClass)

    def test_result_container_when_not_set_accessing_results_in_error(self):
        from dataclasses import dataclass

        @dataclass
        class TestDataclass:
            prop1: str

        result = result_container(TestDataclass)

        with self.assertRaises(AssertionError):
            results = result.results

    def test_when_having_traversed_subsequent_queries_are_performed_on_merged_rdf_graph(self):
        pass

    def test_query_when_dataclasstype_not_dataclass_assertion_error(self):
        pass

    def test_query_final(self):
        pass

    def test_query(self):
        pass

    def test_when_non_result_container_provided_then_assertion_error(self):
        pass