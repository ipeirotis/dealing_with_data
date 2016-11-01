* When discussing unnormalized databases, show the actual normalized database with the orders, not just the schema
* Explain how it fixes the insertion, deletion, and update anomalies

* When discussing cardinalities, we need to separate the min-max cardinality from the one-to-one, one-to-many, many-to-many.

* With the Employee-Jobs-Department example, do a brief introduction of keys to implement relations, and of the bridge table.
* Show the tables with the actual contents to illustrate how the relationships are implemented

* We can have two 1hr15min lectures on modeling. We can compress the ER diagram discussion and cover ER design and translation into tables (foreign keys for 1-1, 1-many; bridge tables for many-many). Then in the second lecture we do the Water Utility Database discussion, together with MySQL workbench, and CREATE TABLE queries.

* Most probably we will need longer for the SELECT statements than a single session. Right now, we get into the SELECT/WHERE queries for IMDB, but do not have time for LIKE, IS NULL.  

* To teach GROUP BY, makes sense to first show the same query with ORDER BY, and then explain that we collapse each of the "groups" using COUNT/AVG/MIN/MAX/etc.
