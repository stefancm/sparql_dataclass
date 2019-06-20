from sparql_dataclass import SPARQLAccess
from unittest import TestCase


class TestSPARQLAccess(TestCase):
    def test_query_raw(self):
        access = SPARQLAccess()
        access.load('http://bigasterisk.com/foaf.rdf')

        result = access.query_raw(
            """SELECT DISTINCT ?aname ?bname
               WHERE {
                  ?a foaf:knows ?b .
                  ?a foaf:name ?aname .
                  ?b foaf:name ?bname .
        }""")

        self.assertEqual(4, len(result))
        for r in result:
            self.assertIsInstance(r, dict)

        for r in result:
            self.assertTrue('aname' in r)
            self.assertTrue('bname' in r)

        self.assertTrue(any(r['aname'] == 'Drew Perttula' and r['bname'] == 'Nathan Wilson' for r in result))
        self.assertTrue(any(r['aname'] == 'Drew Perttula' and r['bname'] == 'Kelsi Perttula' for r in result))
        self.assertTrue(any(r['aname'] == 'Drew Perttula' and r['bname'] == 'David McClosky' for r in result))
        self.assertTrue(any(r['aname'] == 'Drew Perttula' and r['bname'] == 'Henry Story' for r in result))
