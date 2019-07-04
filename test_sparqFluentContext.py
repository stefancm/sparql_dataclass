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

    def test_result_container_when_not_set_accessing_results_in_error(self):
        from dataclasses import dataclass

        @dataclass
        class TestDataclass:
            prop1: str

        result = result_container(TestDataclass)

        with self.assertRaises(AssertionError):
            results = result.results

    def test_query_when_having_traversed_subsequent_queries_are_performed_on_merged_rdf_graph(self):
        url = 'https://scigraph.springernature.com/pub.10.1007/978-3-642-04441-0_57'
        navigation_query = """
        SELECT DISTINCT ?author ?authorSurname ?authorName ?license
        WHERE {
            ?subject <http://schema.org/author>/rdf:rest*/rdf:first ?author.
            ?author <http://schema.org/familyName> ?authorSurname.
            ?author <http://schema.org/givenName> ?authorName.
            } """
        navigation_attributes = ['author']

        check_query = """
            SELECT DISTINCT ?author ?p ?o
            WHERE {
                ?subject <http://schema.org/author>/rdf:rest*/rdf:first ?author.
                ?author ?p ?o.
                } """

        c1 = result_container(dict)
        final_result = start_traversal(url).query_and_continue(check_query, c1, dict)\
            .traverse(navigation_query, navigation_attributes)\
            .query(check_query, dict)

        self.assertGreater(len(final_result), len(c1.results))

    def test_query_when_dataclasstype_not_dataclass_works(self):
        pass

    def test_query_when_no_dataclass_type_provided_returns_raw_dictionary(self):
        pass

    def test_query(self):
        pass

    def test_query_and_continue(self):
        pass

    def test_query_and_continue_when_no_dataclass_type_provided_returns_raw_dictionary(self):
        container = result_container()
        query = """
            SELECT DISTINCT ?springer_url ?author_surname ?author_name
            WHERE {
                ?subject <http://schema.org/author>/rdf:rest*/rdf:first ?springer_url.
                ?springer_url <http://schema.org/familyName> ?author_surname.
                ?springer_url <http://schema.org/givenName> ?author_name.
                } """

        start_traversal('https://scigraph.springernature.com/pub.10.1007/978-3-642-04441-0_57').query_and_continue(query, container)

        self.assertTrue(any(container.results), 'Assumed there are results in container')
        for result in container.results:
            self.assertIsInstance(result, dict)

    def test_query_and_continue_when_result_container_of_different_type_than_constructor_function_then_type_error(self):
        class SomeOtherResultContainertype(ResultContainer):
            pass

        query = """
                    SELECT DISTINCT ?author ?p ?o
                    WHERE {
                        ?subject <http://schema.org/author>/rdf:rest*/rdf:first ?author.
                        ?author ?p ?o.
                        } """

        traversal_context = start_traversal('https://scigraph.springernature.com/pub.10.1007/978-3-642-04441-0_57')
        with self.assertRaises(TypeError):
            traversal_context.query_and_continue(query, SomeOtherResultContainertype(), dict)

    def test_query_and_continue_when_non_result_container_provided_then_assertion_error(self):
        query = """
                    SELECT DISTINCT ?author ?p ?o
                    WHERE {
                        ?subject <http://schema.org/author>/rdf:rest*/rdf:first ?author.
                        ?author ?p ?o.
                        } """

        traversal_context = start_traversal('https://scigraph.springernature.com/pub.10.1007/978-3-642-04441-0_57')
        with self.assertRaises(AssertionError):
            traversal_context.query_and_continue(query, None, dict)