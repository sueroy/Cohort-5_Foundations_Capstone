import sqlite3
from datetime import datetime
import csv

connection = sqlite3.connect('capstone_tables1.db')
cursor = connection.cursor()

class Users:
    def __init__(self,user_id,first_name,last_name,phone,email,password,active,date_created,hire_date,user_type):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password
        self.active = active
        self.date_created = date_created
        self.hire_date = hire_date
        self.user_type = user_type
    
    def view_user(self):
        print(f"\nUser ID: {self.user_id}")
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Active: {self.active}")
        print(f"Date Created: {self.date_created}")
        print(f"Hire Date: {self.hire_date}")
        print(f"User Type: {self.user_type}\n")
        # query = "SELECT user_id, first_name, last_name, email, phone, date_created, hire_date FROM Users WHERE email = ?"
        # row = cursor.execute(query,(email,))
        # 
        
        # print(f'\n{"ID":^5}{"FIRST NAME":25}{"LAST NAME":25}{"EMAIL":30}{"PHONE":15}{"DATE CREATED":15}{"HIRE DATE"}')
    
        # print(f'{str(user_info_list[0]):^5}{str(user_info_list[1]):25}{str(user_info_list[2]):25}{str(user_info_list[3]):30}{str(user_info_list[4]):15}{str(user_info_list[5]):15}{str(user_info_list[6])}')

    def change_password(self, password):
        self.password = password
        query = 'UPDATE Users SET password = ? WHERE user_id = ?'
        cursor.execute(query, (self.password, self.user_id))
        connection.commit()
        return print(f'\nThe password has been changed.')

    def email_update(self, new_email):
        self.email = new_email
        query = 'UPDATE Users SET email = ? WHERE user_id = ?'
        cursor.execute(query, (self.email, self.user_id))
        connection.commit()
        return print (f'\nThe email has been updated to {self.email}.')
    
    def edit_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        query = 'UPDATE Users SET first_name = ?, last_name = ? WHERE user_id = ?'
        cursor.execute(query, (self.first_name, self.last_name, self.user_id))
        connection.commit()
        return print(f'\nThe name as been updated to {self.first_name} {self.last_name}.')
    
    def view_competency(self, user_id):
        self.user_id = user_id
        query = '''
        SELECT cc.cat_name, cc.category_id, AVG(rca.score) 
        FROM Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE rca.user_id = ?
        AND  cc.category_id = cad.category_id
        AND cad.assessment_id = rca.assessment_id
        GROUP BY cc.category_id
        '''
        rows = cursor.execute(query, (self.user_id,))
        print(f'\n{"COMPETENCY":30}{"COMP ID":^9}{"AVERAGE SCORE":13}')
        for row in rows:
            print(f'{row[0]:30}{row[1]:^9}{row[2]:13.2f}')
    
    def view_assess_results(self, user_id):
        self.user_id = user_id
        query = '''SELECT cc.cat_name, cad.assess_name, rca.result_id, rca.score, rca.date_taken 
        FROM Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE rca.user_id = ? 
        AND  cc.category_id = cad.category_id
        AND cad.assessment_id = rca.assessment_id
        ORDER BY rca.date_taken DESC
        '''
        rows = cursor.execute(query, (self.user_id,))
        print(f'\n{"COMPETENCY":30}{"ASSESSMENT NAME":30}{"RESULT ID":^10}{"SCORE":^7}{"DATE TAKEN":^12}')
        for row in rows:
            print(f'{row[0]:30}{row[1]:30}{row[2]:^10}{row[3]:^7}{row[4]:^12}')
        

class Manager(Users):
        
    def view_all_users(self):
        rows = cursor.execute("SELECT user_id, first_name, last_name, email, active FROM Users").fetchall()

        print(f'\n{"ID":^5}{"FIRST NAME":25}{"LAST NAME":25}{"EMAIL":30}{"ACTIVE"}')
    
        for row in rows:
            print(f'{row[0]:^5}{row[1]:25}{row[2]:25}{row[3]:30}{row[4]:^6}')

    def view_managers(self):
        rows = cursor.execute("SELECT user_id, first_name, last_name FROM Users WHERE user_type = 1").fetchall()

        print(f'\n{"ID":^5}{"FIRST NAME":25}{"LAST NAME":25}')
    
        for row in rows:
            print(f'{row[0]:^5}{row[1]:25}{row[2]:25}')
    
    def user_search(self):
        user_input = input('\nPlease enter a First name or a Last name:\n\n')
        row_names = cursor.execute("SELECT * FROM users WHERE first_name LIKE ? OR last_name LIKE ?",(f'%{user_input}%',f'%{user_input}%',)).fetchall()
    
        if row_names:
            print(f'\n\n{"ID":^5}{"FIRST NAME":20}{"LAST NAME":20}{"EMAIL"}')
            
            for row in row_names:
                print(f'{row[0]:^5}{row[1]:20}{row[2]:20}{row[4]}')

            edit_user = input('\nPlease enter the User ID you wish to view: ')
            row = cursor.execute("SELECT * FROM users WHERE user_id = ?",(edit_user,)).fetchone()
            
            user_id = row[0]
            first_name = row[1]
            last_name = row[2]
            phone = row[3]
            email = row[4]
            password = row[5]
            active = row[6]
            date_created = row[7]
            hire_date = row[8]
            user_type = row[9]

            print(f'\n{"ID":^5}{"FIRST NAME":25}{"LAST NAME":25}{"PHONE":15}{"EMAIL":30}{"DATE CREATED":15}{"HIRE DATE"}')
        
            print(f'{str(row[0]):^5}{str(row[1]):25}{str(row[2]):25}{str(row[3]):15}{str(row[4]):30}{str(row[7]):15}{str(row[8])}')

            user = Users(user_id,first_name,last_name,phone,email,password,active,date_created,hire_date,user_type)
            return user
        
        else:
            input("\nNo Matching Results. Press enter to continue.")
            return None
    
    def view_comp_all_users(self):
        query = '''
        SELECT cc.cat_name, cc.category_id, u.user_id, u.first_name, u.last_name, AVG(rca.score), cad.assess_name, rca.date_taken 
        FROM Users u, Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE u.user_id = rca.user_id AND cc.category_id = cad.category_id AND cad.assessment_id = rca.assessment_id
        GROUP BY u.user_id, cc.category_id 
        ORDER BY u.user_id
        '''
        rows = cursor.execute(query).fetchall()
        print(f'\n{"COMPETENCY NAME":30}{"COMPETENCY ID":^15}{"USER ID":^7}{"FIRST NAME":20}{"LAST NAME":20}{"AVERAGE SCORE":^15}{"LAST DATE TAKEN"}')
        for row in rows:
            print(f'{row[0]:30}{row[1]:^15}{row[2]:^7}{row[3]:20}{row[4]:20}{row[5]:^15.2f}{row[7]}')

    def view_comp_level_user(self):
        edit_user = self.user_search()
        
        query = '''
        SELECT u.user_id, u.first_name, u.last_name, u.email, cc.cat_name, cc.category_id, AVG(rca.score) 
        FROM Users u, Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE u.user_id = ? AND cc.category_id = cad.category_id AND cad.assessment_id = rca.assessment_id
        GROUP BY cc.cat_name 
        ORDER BY rca.date_taken DESC
        '''
        rows = cursor.execute(query, (edit_user.user_id,)).fetchall()
        print(f"\n{'USER ID':^7}{'FIRST NAME':15}{'LAST NAME':15}{'EMAIL':30}{'COMPETENCY':30}{'CATEGORY ID':^13}{'AVERAGE SCORE':^15}")
        for row in rows:
            print(f"{row[0]:^7}{row[1]:15}{row[2]:15}{row[3]:30}{row[4]:30}{row[5]:^13}{row[6]:^15.2f}")

    def view_assess_list_user(self):
        edit_user = self.user_search()
       
        query = '''
        SELECT u.user_id, u.first_name, u.last_name, cad.assessment_id, cad.assess_name, rca.score, rca.date_taken FROM Users u, Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE u.user_id = ? AND cc.category_id = cad.category_id AND cad.assessment_id = rca.assessment_id
        GROUP BY cad.assessment_id 
        ORDER BY rca.date_taken DESC
        '''
        rows = cursor.execute(query, (edit_user.user_id,)).fetchall()
        print(f"\n{'USER ID':^8}{'FIRST NAME':15}{'LAST NAME':15}{'ASSESS ID':^13}{'ASSESSMENT NAME':30}{'AVERAGE SCORE':^15}{'DATE TAKEN'}")
        for row in rows:
            print(f"{row[0]:^8}{row[1]:15}{row[2]:15}{row[3]:^13}{row[4]:30}{row[5]:^15.2f}{row[6]}")

    def view_all_results_user(self):
        edit_user = self.user_search()
       
        query = '''
        SELECT u.user_id, u.first_name, u.last_name, cad.assess_name, rca.result_id, rca.score, rca.date_taken 
        FROM Users u, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE u.user_id = ? AND cad.assessment_id = rca.assessment_id AND u.user_id = rca.user_id
        GROUP BY rca.result_id
        '''
        rows = cursor.execute(query, (edit_user.user_id,)).fetchall()
        print(f"\n{'USER ID':^8}{'FIRST NAME':15}{'LAST NAME':15}{'ASSESSMENT NAME':25}{'RESULT ID:':^10}{'SCORE':^5}{'DATE TAKEN'}")
        
        for row in rows:
            print(f"{row[0]:^8}{row[1]:15}{row[2]:15}{row[3]:25}{row[4]:^10}{row[5]:^5.2f}{row[6]}")

    def view_all_categories(self):
        rows = cursor.execute('SELECT * FROM Competency_Cat').fetchall()
        print(f'\n{"CATEGORY ID":^13}{"CATEGORY NAME":^35}{"ACTIVE"}')

        for row in rows:
            print(f'{row[0]:^13}{row[1]:^35}{row[2]}')

    def view_all_assessments(self):
        rows = cursor.execute('SELECT * FROM Comp_Assessment_Data').fetchall()
        print(f'\n{"ASSESSMENT ID":^15}{"ASSESSMENT NAME":^30}{"DATE CREATED":^13}{"CATEGORY ID":^13}{"ACTIVE"}')

        for row in rows:
            print(f'{row[0]:^15}{row[1]:^30}{row[2]:^13}{row[3]:^13}{row[4]}')
   
    def add_user(self,first_name,last_name, phone, email, password, active, date_created, hire_date, user_type):
        query = 'INSERT INTO Users (first_name,last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES(?,?,?,?,?,?,?,?,?)'
        cursor.execute(query, (first_name,last_name, phone, email, password, active, date_created, hire_date, user_type))
        connection.commit()
        print(f'\nThis user has been added to the database.')

    def add_new_competency(self,cat_name, active):
        query = 'INSERT INTO Competency_Cat (cat_name, active) VALUES(?,?)'
        cursor.execute(query, (cat_name, active))
        connection.commit()
        print(f'\nThis Competency has been added.')

    def add_new_assessment(self,assess_name, date_created, category_id, active):
        query = 'INSERT INTO Comp_Assessment_Data (assess_name, date_created, category_id, active) VALUES(?,?,?,?)'
        cursor.execute(query, (assess_name, date_created, category_id, active))
        connection.commit()
        print(f'\nThis Assessment has been added.')
    
    def add_new_result(self,user_id,assess_id,score,date_taken,manager):
        query = 'INSERT INTO Results_Comp_Assess (user_id, assessment_id, score, date_taken, manager) VALUES(?,?,?,?,?)'
        cursor.execute(query, (user_id,assess_id,score,date_taken,manager))
        connection.commit()
        print(f'\nThis Result has been added.')

    def edit_user(self,user_obj,first_name,last_name,phone,email,active):
        query = 'UPDATE Users SET first_name = ?, last_name = ?, phone = ?, email = ?, active = ?  WHERE user_id = ?'
        cursor.execute(query, (first_name,last_name,phone,email,active,user_obj.user_id))
        connection.commit()
        print(f'\nThis user has been updated.')

    def edit_competency(self, category_id, cat_name, active):
        query = 'UPDATE Competency_Cat SET cat_name = ?, active = ?  WHERE category_id = ?'
        cursor.execute(query, (cat_name, active, category_id))
        connection.commit()
        print(f'\n{cat_name} has been updated.')

    def edit_assessment(self, assessment_id, assess_name, active):
        query = 'UPDATE Comp_Assessment_Data SET assess_name = ?, active = ?  WHERE assessment_id = ?'
        cursor.execute(query, (assess_name, active, assessment_id))
        connection.commit()
        print(f'\nAssessment ID : {assessment_id} has been updated.')

    def edit_result(self,result_id,score,date_taken):
        query = 'UPDATE Results_Comp_Assess SET score = ?, date_taken = ?  WHERE result_id = ?'
        cursor.execute(query, (score, date_taken,result_id))
        connection.commit()
        print(f'\nResult Id: {result_id} has been updated.')

    def delete_result(self,result_id):        
        query = 'DELETE FROM Results_Comp_Assess WHERE result_id = ?'
        cursor.execute(query, (result_id,))
        connection.commit()
        print(f'\nResult Id {result_id} has been deleted.')
         
    def export_csv_user_comp(self, user_obj):
        fields = ['User ID', 'First Name', 'Last Name', 'Email', 'Competency', 'Competency ID', 'Average Score']
        query = ('''
        SELECT u.user_id, u.first_name, u.last_name, u.email, cc.cat_name, cc.category_id, AVG(rca.score)
        FROM Users u, Competency_Cat cc, Comp_Assessment_Data cad, Results_Comp_Assess rca 
        WHERE u.user_id = ? AND u.user_id = rca.user_id AND cc.category_id = cad.category_id AND cad.assessment_id = rca.assessment_id
        GROUP BY cc.cat_name
        ORDER BY cc.category_id 
        ''')
        rows = cursor.execute(query, (user_obj.user_id,)).fetchall()
        
        with open('user_competency.csv', 'w') as user_comp:
            wrt = csv.writer(user_comp)
            wrt.writerow(fields)
            wrt.writerows(rows)
        
        print(f'\nYour report has been exported to user_competency.csv')   

    def export_csv_alluser_results(self):
        fields = ['Competency', 'Competency ID', 'User ID', 'First Name', 'Last Name', 'Average Score', 'Assessment Name', 'Assessment ID', 'Date Taken']
        query = ('''
        SELECT cc.cat_name, cc.category_id, u.user_id, u.first_name, u.last_name, AVG(rca.score), cad.assess_name, cad.assessment_id, rca.date_taken 
        FROM Competency_Cat  AS cc
        LEFT JOIN Comp_Assessment_Data  AS cad
        ON cc.category_id = cad.category_id
        LEFT JOIN Results_Comp_Assess AS rca
        ON cad.assessment_id = rca.assessment_id
        LEFT JOIN Users AS u
        ON u.user_id = rca.user_id
        GROUP BY cc.category_id, u.user_id
        ''')

        rows = cursor.execute(query).fetchall()
                
        with open('all_user_results.csv', 'w') as all_results:
            wrt = csv.writer(all_results)
            wrt.writerow(fields)
            wrt.writerows(rows)
        print(f'\nYour report has been exported to all_user_results.csv')
        
    def import_csv_assess_results(self):
        
        data_list = []

        with open('results_import.csv', 'r') as results:
            csv_reader = csv.reader(results)
            fields = next(csv_reader)
            for row in csv_reader:
                data_list.append(row)
                       
        query = 'INSERT INTO Results_Comp_Assess (user_id, assessment_id, score, date_taken) VALUES (?,?,?,?)'
        
        for row in data_list:
            cursor.execute(query, (int(row[0]), int(row[1]), int(row[2]), row[3], ))
            connection.commit()
        print("\nYour database has been successfully updated.")

    def user_activation(self,act_user,act_deact):
        query = 'UPDATE Users SET active = ?  WHERE user_id = ?'
        cursor.execute(query, (act_deact, act_user))
        connection.commit()
        if act_deact == 0:
            print(f'\nUser ID: {act_user} has been deactivated.')
        elif act_deact == 1:
            print(f'\nUser ID: {act_user} has been activated.')

    def comp_activation(self,act_comp,act_deact):
        query = 'UPDATE Competency_Cat SET active = ?  WHERE category_id = ?'
        cursor.execute(query, (act_deact, act_comp))
        connection.commit()
        if act_deact == 0:
            print(f'\nCompetency ID: {act_comp} has been deactivated.')
        elif act_deact == 1:
            print(f'\nCompetency ID: {act_comp} has been activated.')

    def assess_activation(self,act_assess,act_deact):
        query = 'UPDATE Comp_Assessment_Data SET active = ?  WHERE assessment_id = ?'
        cursor.execute(query, (act_deact, act_assess))
        connection.commit()
        if act_deact == 0:
            print(f'\nCompetency ID: {act_assess} has been deactivated.')
        elif act_deact == 1:
            print(f'\nCompetency ID: {act_assess} has been activated.')

    def manager_activation(self,act_man,act_deact):
        query = 'UPDATE Users SET user_type = ?  WHERE user_id = ?'
        cursor.execute(query, (act_deact, act_man))
        connection.commit()
        if act_deact == 1:
            print(f'\nUser ID: {act_man} has been set as a Manager.')
        elif act_deact == 0:
            print(f'\nUser ID: {act_man} has been set as a User.')
            
