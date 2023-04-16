import sqlite3
import csv
from datetime import datetime
import bcrypt


# def create_schema(cursor):
#     with open('schema.sql') as my_queries:
#         queries = my_queries.read()
    
#     cursor.executescript(queries)

connection = sqlite3.connect('capstone_tables1.db')
cursor = connection.cursor()

# result = create_schema(cursor)

# user_list = []
# with open('capstone_user_data.csv', 'r', encoding = 'utf-8-sig') as csvfile:
#     csv_dict_reader = csv.DictReader(csvfile)
#     for row in csv_dict_reader:
#         user_list.append(row)
#     # print(user_list)

# query = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES (?,?,?,?,?,?,?,?,?)'

# for row in user_list:
#     cursor.execute(query, (row['first_name'], row['last_name'], row['phone'], row['email'], row['password'], row['active'], row['date_created'], row['hire_date'], row['user_type']))

#     connection.commit()

# category_list = []
# with open('capstone_comp_cat_data.csv', 'r', encoding = 'utf-8-sig') as csvfile:
#     csv_dict_reader = csv.DictReader(csvfile)
#     for row in csv_dict_reader:
#         category_list.append(row)
#     # print(category_list)

# query = 'INSERT INTO Competency_Cat (cat_name, active) VALUES (?,?)'

# for row in category_list:
#     # print(row['active'], row['user_type'])
#     cursor.execute(query, (row['cat_name'], row['active']))

#     connection.commit()

# assessment_list = []
# with open('capstone_assessment_name_data.csv', 'r', encoding = 'utf-8-sig') as csvfile:
#     csv_dict_reader = csv.DictReader(csvfile)
#     for row in csv_dict_reader:
#         assessment_list.append(row)
#     # print(assessment_list)

# query = 'INSERT INTO Comp_Assessment_Data (assess_name, date_created, category_id, active) VALUES (?,?,?,?)'

# for row in assessment_list:
#     # print(row['active'], row['user_type'])
#     cursor.execute(query, (row['assess_name'], row['date_created'], row['category_id'],row['active']))

#     connection.commit()

# results_list = []
# with open('capstone_results_data.csv', 'r', encoding = 'utf-8-sig') as csvfile:
#     csv_dict_reader = csv.DictReader(csvfile)
#     for row in csv_dict_reader:
#         results_list.append(row)
#     print(results_list)

# query = 'INSERT INTO Results_Comp_Assess (user_id, assessment_id, score, date_taken, manager) VALUES (?,?,?,?,?)'

# for row in results_list:
#     # print(row['date_taken'], row['user_type'])
#     cursor.execute(query, (row['user_id'], row['assessment_id'], row['score'], row['date_taken'], row['manager']))

#     connection.commit()

# passwood encryption
query = 'SELECT password, user_id FROM Users'
rows = cursor.execute(query).fetchall()

pwd_list = []
for tuple in rows:
    bytes = tuple[0].encode('utf-8')

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes,salt)
    query1 = 'UPDATE Users SET password = ? where user_id = ?'
    cursor.execute(query1, (hash, tuple[1]))
    connection.commit()

