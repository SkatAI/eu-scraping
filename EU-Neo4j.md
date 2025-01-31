# Neo4j EU

structure

Nodes:

MEPs (Members of European Parliament)
Debates (Sessions)
Political Parties


Relationships:

MEPs BELONGS_TO Party
MEPs SPEAKS_IN Debate
MEPs FOLLOWS Other_MEP (if we want to track who speaks after whom)


Create a new database in Neo4j Desktop with a password


Load JSON data into Python
Clean and transform data:

Extract debate dates from parent URLs
Handle any special characters in names/text
Create unique identifiers for debates


Create nodes for MEPs, Parties, and Debates

Create relationships between nodes

Add properties (like speech text, timestamps)