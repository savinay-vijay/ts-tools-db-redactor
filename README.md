# ts-tools-db-redactor
A Database Redactor for MongoDB Support databases. 

The script is a POC of a database redactor to redact sensitive customer information while keeping the non-senstive information intact for the MongoDB development and testing team.

The script connects to MFLIX database on an Atlas Cluster and fetches first 5 records from "movies" collection. It then redacts the "countries" and "rating" fields with an MD5 Hash and provides the new redacted documents in JSON.
