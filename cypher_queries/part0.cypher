// Delete orphan nodes s/p database creation & import of data (i.e. s/p -> ./bin/neo4j-admin import ...)
MATCH (orphans) WHERE size((orphans)--())=0 DELETE orphans;