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

    def test_query(self):
        from dataclasses import dataclass, field

        @dataclass
        class TestClass:
            aname:str
            other_name:str = field(metadata={'load_from' : 'bname'})

        access = SPARQLAccess()
        access.load('http://bigasterisk.com/foaf.rdf')

        result = access.query("""SELECT DISTINCT ?aname ?bname
               WHERE {
                  ?a foaf:knows ?b .
                  ?a foaf:name ?aname .
                  ?b foaf:name ?bname .
        }""", TestClass)

        self.assertEqual(4, len(result))

        for r in result:
            self.assertIsInstance(r, TestClass)

        self.assertTrue(any(r.aname == 'Drew Perttula' and r.other_name == 'Nathan Wilson' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.other_name == 'Kelsi Perttula' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.other_name == 'David McClosky' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.other_name == 'Henry Story' for r in result))

    def test_query_when_partial_dataclass_match_then_deserialize_into_that(self):
        from dataclasses import dataclass, field

        @dataclass
        class TestClass:
            bname:str
            other:str = None

        access = SPARQLAccess()
        access.load('http://bigasterisk.com/foaf.rdf')

        result = access.query("""SELECT DISTINCT ?aname ?bname
               WHERE {
                  ?a foaf:knows ?b .
                  ?a foaf:name ?aname .
                  ?b foaf:name ?bname .
        }""", TestClass)

        self.assertEqual(4, len(result))

        for r in result:
            self.assertIsInstance(r, TestClass)

        self.assertTrue(any(r.other == None and r.bname == 'Nathan Wilson' for r in result))
        self.assertTrue(any(r.other == None and r.bname == 'Kelsi Perttula' for r in result))
        self.assertTrue(any(r.other == None and r.bname == 'David McClosky' for r in result))
        self.assertTrue(any(r.other == None and r.bname == 'Henry Story' for r in result))

    def test_query_when_dataclasstype_not_dataclass_then_still_works(self):
        class TestClassNonDataClass:
            aname: str
            bname: str

        access = SPARQLAccess()
        access.load('http://bigasterisk.com/foaf.rdf')

        result = access.query("""SELECT DISTINCT ?aname ?bname
                                 WHERE {
                                    ?a foaf:knows ?b .
                                    ?a foaf:name ?aname .
                                    ?b foaf:name ?bname .
                          }""", TestClassNonDataClass)

        self.assertEqual(4, len(result))

        for r in result:
            self.assertIsInstance(r, TestClassNonDataClass)

        self.assertTrue(any(r.aname == 'Drew Perttula' and r.bname == 'Nathan Wilson' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.bname == 'Kelsi Perttula' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.bname == 'David McClosky' for r in result))
        self.assertTrue(any(r.aname == 'Drew Perttula' and r.bname == 'Henry Story' for r in result))

    def test_query_when_no_dataclass_type_then_works_as_raw(self):
        access = SPARQLAccess()
        access.load('http://bigasterisk.com/foaf.rdf')

        result = access.query("""SELECT DISTINCT ?aname ?bname
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