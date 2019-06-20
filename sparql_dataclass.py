import rdflib
from typing import Dict, List, Generic, TypeVar, Type
from __future__ import annotations

rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Serializer,
    'rdflib.plugins.serializers.rdfxml', 'XMLSerializer')
rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Parser,
    'rdflib.plugins.parsers.rdfxml', 'RDFXMLParser')

class SPARQLAccess:
    def __init__(self):
        pass

    def load(self, uri):
        pass

    def query_raw(self, sparql: str) -> List[Dict[str,object]]:
        pass

    T = TypeVar('T')
    def query(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        pass


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