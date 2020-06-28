# Movie Recommendation System based on Graph and Relational Databases

Recommendation systems are found everywhere especially in retail, music and video streaming, entertainment industry. A recommender system which has an internal function takes in information about
the user (can have multiple attributes) and predicts the rating the user would give the product. These systems employ collaborative filtering technique to recommend items to the user. This technique enables users to query based on other user's actions or opinions.

The project analyzes how a recommendation system performs when built on a graph database and compare the retrieval query processing time with that built based on a relational database system.

Two databases for our project - MySQL and Neo4j

Neo4j: ​https://neo4j.com/docs/operations-manual/current/installation/linux/debian/

MySQL:
https://dev.mysql.com/downloads/installer/
https://www.liquidweb.com/kb/install-mysql-windows/

Movielens 10M dataset: https://grouplens.org/datasets/movielens/

#### Load data into database
MySQL: Running the sql-queries.sql file would create table and load the data. Source <path>/sql-queries.sql
Neo4j: Loading of the data into graph database is done through a cypher query given in the script.

Steps:
1. Download the movie lens dataset
2. Import data into Neo4j and MySQL
3. Calculate cosine similarity for every pair of users
4. Find top N similar users with the queried user
5. Iterate over similar users and find union of movies watched by them.
6. Select subset of movies watched by at least M similar users
7. Predicted rating for each movie is calculated by taking a weighted average (weight=similarity) of similar-user given ratings.
8. Select the top P movies to be recommend.

#### Neo4j
After installing neo4j(use the linkmentioned above), run the command ‘sudo service neo4j restart’ in the command line
Open ​http://localhost:7474/browser/​ in any browser to open Neo4j browser.
