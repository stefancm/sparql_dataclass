from __future__ import annotations
import rdflib
from typing import Dict, List, Generic, TypeVar, Type
from abc import ABCMeta, abstractmethod

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

TResult = TypeVar('TResult')
class ResultContainer(Generic[TResult], metaclass=ABCMeta):
    def __init__(self):
        if not isinstance(self,_ResultContainerImplementation):
            raise TypeError('Cannot inherit from ResultContainer.')

    @property
    @abstractmethod
    def results(self) -> List[TResult]:
        pass

class _ResultContainerImplementation(ResultContainer[TResult]):
    __results: List[TResult]

    __result_type: Type[TResult]
    __is_set = False

    def __init__(self, result_type: Type[TResult]):
        self.__result_type = result_type

    def set(self, results: List[TResult]):
        assert all(isinstance(x, self.__result_type) for x in results), f'All elements should be of the result type {self.__result_type} for which the result container was created.'
        self.__results = results

        self.__is_set = True

    @property
    def results(self):
        assert self.__is_set, 'Results have not yet been set.'

        return self.__results

def result_container(result_type: Type[TResult]) -> ResultContainer[TResult]:
    import dataclasses
    assert dataclasses.is_dataclass(result_type), 'Provided result type should be dataclass. Cannot create result container for non-dataclass type.'

    return _ResultContainerImplementation(result_type)

class TraversalContext:
    def traverse(self, sparql: str, navigation_attributes: List[str]) -> TraversalContext:
        pass

    T = TypeVar('T')
    def query_and_continue(self, dataclass_type: Type[T], sparql: str, result_container: ResultContainer[T]) -> TraversalContext:
        pass

    def query(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        pass

class __TraversalContext(TraversalContext):
    def __init__(self, initial_uri: str):
        pass

    def traverse(self, sparql: str, navigation_attributes: List[str]) -> TraversalContext:
        pass

    T = TypeVar('T')
    def query_and_continue(self, dataclass_type: Type[T], sparql: str, result_container: ResultContainer[T]) -> TraversalContext:
        pass

    def query(self, dataclass_type: Type[T], sparql: str) -> List[T]:
        pass

def start_traversal(url: str) -> TraversalContext:
    context = __TraversalContext(initial_uri=url)