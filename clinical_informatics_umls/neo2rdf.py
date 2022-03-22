#!/usr/bin/env python3
import json
import os

import rdflib
import requests
from dotenv import load_dotenv


def neo_to_rdf(dot: str):
    """
    Summary:
    --------
    Means of serializing a Neo4j Label Property Graph to a W3C validated RDF graph

    Parameters:
    -----------
    dotenv_file : str.
        .env file via python-dotenv containing database authentication information
        and uts apikey.

    Returns:
    --------
    graph : rdflib.Graph
        RDF serialization (ttl) of a Neo4j LPGraph.

    """

    load_dotenv(dot)

    url = os.getenv("NEO4J_HTTP_URL")

    cypher = "MATCH (x:Code)-[r0:HAS_AUI]->(y:Atom)-[r1:HAS_CUI]->(z:Concept)<-[r2:HAS_CUI]-(v:Atom)<-[r3:HAS_AUI]-(k:Code) RETURN * LIMIT 100"

    payload = {"cypher": cypher, "format": "Turtle*"}

    response = requests.post(
        url,
        auth=(
            os.getenv("NEO4J_USERNAME"),
            os.getenv("NEO4J_PASSWORD"),
        ),
        data=json.dumps(payload),
    )
    response.raise_for_status()  # raise an error on unsuccessful status codes
    graph = rdflib.Graph()
    graph.parse(data=response.text, format="turtle").serialize(
        destination="../output_data/sample_neo4j_to_rdf_serialization.ttl",
        format="ttl",
        encoding="utf-8",
    )
    print("complete serialization")

    return graph


if __name__ == "__main__":
    neo_to_rdf(dot="../.env")
