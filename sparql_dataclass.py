from __future__ import annotations
import rdflib
from typing import Dict, List, Generic, TypeVar, Type

rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Serializer,
    'rdflib.plugins.serializers.rdfxml', 'XMLSerializer')
rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Parser,
    'rdflib.plugins.parsers.rdfxml', 'RDFXMLParser')

class SPARQLAccess:
    __graph: rdflib.Graph

    def __init__(self):
        self.__graph = rdflib.Graph()

    def load(self, uri):
        self.__graph.parse(uri)

    def __dict_from_row(query_result):
        return {k:query_result[v].__str__() for (k,v) in query_result.labels.items()}

    def query_raw(self, sparql: str) -> List[Dict[str,object]]:
        results = self.__graph.query(sparql)
        return [SPARQLAccess.__dict_from_row(r) for r in results]

    T = TypeVar('T')
    def query(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        import dataclasses

        assert dataclasses.is_dataclass(dataclass_type), 'Provided type should be dataclass.'

        from marshmallow_dataclass import dataclass as marshable_dataclass
        marshable_dataclass_type = marshable_dataclass(dataclass_type)

        deserialized = [marshable_dataclass_type.Schema().load(r, partial=True) for r in self.query_raw(sparql)]
        return [r for (r, _) in deserialized]

TResult = TypeVar('TQueryResult')
class ResultContainer(Generic[TResult]):
    __results: List[TResult]

    @property
    def results(self) -> List[TResult]:
        pass

class QueryAndTraversalContext:
    def traverse(self, sparql: str, navigation_attributes: List[str]) -> QueryAndTraversalContext:
        pass

    T = TypeVar('T')
    def query(self, dataclass_type: Type[T], sparql: str, result_container: ResultContainer[T]) -> QueryAndTraversalContext:
        pass

    def query_final(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        pass

class __QueryAndTraversalContext(QueryAndTraversalContext):
    def __init__(self, initial_uri: str):
        pass

    def traverse(self, sparql: str, navigation_attributes: List[str]) -> QueryAndTraversalContext:
        pass

    T = TypeVar('T')
    def query(self, dataclass_type: Type[T], sparql: str, result_container: ResultContainer[T]) -> QueryAndTraversalContext:
        pass

    def query_final(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        pass

def start_at_url(url: str) -> QueryAndTraversalContext:
    context = __QueryAndTraversalContext(initial_uri=url)