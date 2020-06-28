#!/usr/bin/python
import MySQLdb
import sys
import operator
import time

db = MySQLdb.connect(host="localhost",  # your host 
	                 user="root",       # username
    	             passwd="sravanthi123",     # password
        	         db="dbms_project")   # name of the database

def get_total_users():
	cur=db.cursor()
	cur.execute("SELECT Count(DISTINCT userId) FROM dbms_project.movie_user")
	result=cur.fetchone()
	return result[0]

def create_user_tables(no_of_users):
	cur=db.cursor()
	for i in range(1,no_of_users):
		column1 = "user"+str(i)+"rating"
		table1 = "user"+str(i)+"table"
		
		cur.execute("DROP TABLE IF EXISTS "+table1)

		cur.execute("CREATE TABLE IF NOT EXISTS "+table1+" (userid int, movieid int, "+ column1 +" int, timestamp int)")
		insert_query = "insert into "+table1+" SELECT userid, movieid, rating, timestamp FROM dbms_project.movie_user WHERE userId="+str(i)
		cur.execute(insert_query)
	db.commit()


def create_similarity_table(no_of_users):

	cur = db.cursor()
	cur.execute("DROP TABLE IF EXISTS similarity_table")

	cur.execute("SHOW TABLES LIKE 'similarity_table'")
	result = cur.fetchone()

	if result:
		return

	cur.execute("CREATE TABLE IF NOT EXISTS similarity_table (user1 int, user2 int, similarity_index double, primary key(user1, user2))")

	for i in range(1,no_of_users):
		column1 = "user"+str(i)+"rating"
		table1 = "user"+str(i)+"table"

		for j in range(i+1, no_of_users):
			column2 = "user"+str(j)+"rating"
			table2 = "user"+str(j)+"table"

			query = "SELECT sum("+str(column1)+"*"+str(column2)+")/(sqrt(sum("+str(column1)+"*"+str(column1)+"))*sqrt(sum("+str(column2)+"*"+str(column2)+"))) FROM "+str(table1)+", "+str(table2)+" where "+str(table1)+".movieid = "+str(table2)+".movieid"
			cur.execute(query)
			for val in cur.fetchall():
				similarity_index = val[0]
			
			#print(column1, column2, similarity_index)

			if similarity_index is not None:
				insert_query = "insert into similarity_table values("+str(i)+","+str(j)+","+str(similarity_index)+")"
				cur.execute(insert_query)
				insert_query = "insert into similarity_table values("+str(j)+","+str(i)+","+str(similarity_index)+")"
				cur.execute(insert_query)

	db.commit()

def predict_movies(userid=1):
	# Create a Cursor object to execute queries.
	cur = db.cursor()
	print(userid)
	# Select data from table using SQL query.
	cur.execute("SELECT user2,similarity_index from similarity_table where user1="+str(userid)+" order by similarity_index desc, user2 LIMIT 10 ")

	similar_users = []
	similarity_index = []
	sim_users_with_index = {}

	for item in cur.fetchall():
		similar_users.append(item[0])
		similarity_index.append(item[1])
		sim_users_with_index[item[0]] = item[1]

	print("\nSimilar users:\n")
	print(similar_users)

	# print the first and second columns
	movie_cur = db.cursor()
	mapping = {}
	for row in similar_users:
		movie_cur.execute("SELECT movieid from movie_user where userid="+str(row))
		for movie_row in movie_cur.fetchall():
			if movie_row[0] not in mapping.keys():
				mapping[movie_row[0]] = [row]
			else:
				mapping[movie_row[0]].append(row)

	movie_list = []
	#print("\nUnion of movies")
	for key, value in mapping.items():
		#print(key)
		if len(value) >= 4:
			movie_list.append(key)

	print("\nCommon Movie list:\n")
	print(movie_list)

	# movies_to_predict = []
	# movie_ratings = []
	predicted_movies_rating = {}
	for movie in movie_list:
		numerator = 0
		denominator = 0 
		for user in mapping[movie]:
			cur.execute("SELECT rating from movie_user where userid="+str(user)+" and movieid="+str(movie))
			for r in cur.fetchall():
				rating = r[0]
			
			numerator += rating*sim_users_with_index[user]
			denominator += sim_users_with_index[user]
			#print(rating)
		prediction = numerator/denominator
		# movies_to_predict.append(movie)
		# movie_ratings.append(prediction)
		#movies_to_predict.append(prediction)
		predicted_movies_rating[movie] = prediction

	sorted_pred = sorted(predicted_movies_rating.items(), key=operator.itemgetter(1))
	
	print("\nPredicted movies for user "+str(userid))
	#print(sorted_pred)
	for x in list(sorted_pred)[-5:]:
		print(x)

if __name__ == '__main__':
	start_time = time.time()

	num_of_users=get_total_users()
	create_user_tables(num_of_users)
	create_similarity_table(num_of_users)
	predict_movies(1)
	
	#print("--- %s seconds ---" % (time.time() - start_time))

	db.close()
