#!/usr/bin/env python3
import os
import json
import requests
import rdflib
from os.path import join, dirname
from dotenv import load_dotenv, dotenv_values


def neo_to_rdf(__file__: str):
    """
    Summary:
    --------
    Means of serializing a Neo4j Label Property Graph to a W3C validated RDF graph

    Parameters:
    -----------
    __file__ : str.
        .env file via python-dotenv containing db auth and connection information.

    Returns:
    --------
    graph : rdflib.Graph
        RDF serialization (ttl) of a Neo4j LPGraph. 

    """
    dotenv_path = join(dirname(__file__), "../.env")
    load_dotenv(dotenv_path)

    url = os.environ.get("NEO4J_HTTP_URL")

    cypher = """
    MATCH path = (n:NCI)-[r:HAS_AUI]->(x:AUI)-[r1:CHILD_OF*0..]->(y:AUI)-[r2:HAS_CUI]->(z:CUI)-[r3:HAS_STY]->(v:TUI)
    WHERE y.ISPREF = 'Y' AND x.ISPREF = 'Y' AND n.CODE = 'C1909'
    RETURN path LIMIT 125
    """

    payload = {'cypher': cypher, 'format': 'Turtle*'}

    response = requests.post(
        url,
        data=json.dumps(payload),
        auth=(
            os.environ.get("NEO4J_USERNAME"),
            os.environ.get("NEO4J_PASSWORD")
        ),
    )
    response.raise_for_status()  # raise an error on unsuccessful status codes
    graph = rdflib.Graph()
    graph.parse(data=response.text, format="ttl").serialize(
        destination="../output_data/sample_neo4j_to_rdf_serialization.ttl", 
        format='ttl', 
        encoding="utf-8"
        )
    print("complete serialization")
    return graph


if __name__ == "__main__":
    graph = neo_to_rdf(__file__)
