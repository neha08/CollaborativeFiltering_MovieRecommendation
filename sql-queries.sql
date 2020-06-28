CREATE TABLE movie_user (userid INT, movieid INT, rating INT, timestamp INT);

LOAD DATA LOCAL INFILE '/home/sravanthi/Documents/Dbms/project/movielens-10m_rating/convertcsv_use.csv' INTO TABLE movie_user FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (userid, movieid, rating, timestamp);