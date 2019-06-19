import rdflib
from typing import Dict, List

rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Serializer,
    'rdflib.plugins.serializers.rdfxml', 'XMLSerializer')
rdflib.plugin.register(
    'rdf+xml', rdflib.plugin.Parser,
    'rdflib.plugins.parsers.rdfxml', 'RDFXMLParser')


class SparqlLoadingContext:
    def load_uri_res(self, uri_sparql):
        pass

    def query(self, sparql) -> List[Dict[str, object]]:
        pass


def initial_url(url: str) -> SparqlLoadingContext:
    pass
