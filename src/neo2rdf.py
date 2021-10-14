# !/bin/bash/env/python
import os
import json
import requests
import rdflib
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.environ.get("NEO4J_HTTP_URL")

cypher = """
MATCH (sty:SemanticType {sty: 'Neoplastic Process'})<-[rel1:HAS_STY]-(cui:Concept)-[rel2:HAS_SOURCE_CODE]->(sct:SNOMEDCT_US)-[rel3:HAS_UMLS_AUI]->
(aui:Atom)-[rel4:HAS_CUI]->(cui2:Concept)-[rel5:HAS_STY]->(sty:SemanticType)-[rel6]-(sty2:SemanticType)
RETURN sty, rel1, cui, rel2, sct, rel3, aui, rel4, cui2, rel5, rel6, sty2 LIMIT 1
"""

payload = {'cypher': cypher, 'format': 'Turtle'}

response = requests.post(url,
                         auth=(os.environ.get("NEO4J_USERNAME"),
                               os.environ.get("NEO4J_PASSWORD")),
                         data=json.dumps(payload))
response.raise_for_status()  # raise an error on unsuccessful status codes

g = rdflib.Graph()
g.parse(data=response.text, format="turtle").serialize(
    destination="sample_neo4j_to_rdf_serialization.ttl", #.ttl W3C file extention for Turtle
    format='ttl',
    encoding="utf-8"
)
print("complete serialization")

################################################################
# Requires clean-up, documentation & additional work
################################################################
