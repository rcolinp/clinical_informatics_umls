#!/usr/bin/env python3
import os
import json
import requests
import rdflib
from os.path import join, dirname
from dotenv import load_dotenv


def neo_to_rdf(__file__: str) -> rdflib.Graph():
    """
    Summary:
    --------
    Accurate means of serializing a Neo4j LPGraph to a W3C validated Turtle (.ttl)

    Parameters:
    -----------
    __file__ : str.
        ../.env file containing database authentication and connection information for use of dotenv.

    Returns:
    --------
    graph : rdflib.Graph
        RDF serialization (ttl) of a Neo4j LPGraph

    """
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    url = os.environ.get("NEO4J_HTTP_URL")

    cypher = """
    MATCH (x:Atom {code: "C1909"})-[r:CHILD_OF*]->(y:Atom) 
    WHERE y.ispref = 'Y' AND x.ispref = 'Y' 
    RETURN x,r,y LIMIT 25
    """

    payload = {'cypher': cypher, 'format': 'Turtle'}

    response = requests.post(url,
                             auth=(os.environ.get("NEO4J_USERNAME"),
                                   os.environ.get("NEO4J_PASSWORD")),
                             data=json.dumps(payload))
    response.raise_for_status()  # raise an error on unsuccessful status codes
    graph = rdflib.Graph()
    graph.parse(data=response.text, format="ttl").serialize(
        # .ttl W3C file extention for Turtle
        destination="../output_data/sample_neo4j_to_rdf_serialization.ttl",
        format='ttl',
        encoding="utf-8"
    )
    print("complete serialization")
    return graph


if __name__ == '__main__':
    graph = neo_to_rdf(__file__)
