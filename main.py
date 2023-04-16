import sqlite3
from Classes import Users, Manager
import bcrypt
import csv
from datetime import datetime

connection = sqlite3.connect('capstone_tables1.db')
cursor = connection.cursor()

def login():
    
    email = input('\nPlease enter your email:')
    password = input('\nPlease enter your password:')

    query = f'SELECT * FROM Users WHERE email = ?'
    user_info = cursor.execute(query, (email,)).fetchone() # Returns single Tuple (user_id, first, last, etc....)

    user_info_list = []
    for item in user_info:
        user_info_list.append(item)

    user_id = user_info_list[0]
    first_name = user_info_list[1]
    last_name = user_info_list[2]
    phone = user_info_list[3]
    email = user_info_list[4]
    db_password = user_info_list[5]
    active = user_info_list[6]
    date_created = user_info_list[7]
    hire_date = user_info_list[8]
    user_type = user_info_list[9]

    # bytes = user_info_list[5].encode('utf-8')
    # salt = bcrypt.gensalt()
    # hash = bcrypt.hashpw(bytes,salt)


    userbytes = password.encode('utf-8')
    result = bcrypt.checkpw(userbytes,db_password)
    

    if result:
        if user_type == 0:
            return Users(user_id,first_name,last_name,phone,email,db_password,active,date_created,hire_date,user_type)
        else:
            return Manager(user_id,first_name,last_name,phone,email,db_password,active,date_created,hire_date,user_type)
    else:
        print('\nInvalid login credentials. Please try again\n')
        return None

def logout():
    print('\nGoodbye!\n')
    exit()

   
def user_menu(user_obj):

    user_input = input('''
    \n***USER MENU***
    
    Please select from the following options:
    
    1: View Your Information.
    2: Change Your Email Address.
    3: Change Your Name.
    4: Change Your Password.
    5: View Your Competency Scores.
    6: View Your Assessment Scores
    7: Quit (Q))
    
    >>>''')

    if user_input == '1':
        email = user_obj.email
        user_obj.view_user()

    if user_input == '2':
        user_email1 = input('Please enter your new email:')
        user_email2 = input('Please confirm your new email:')
        if user_email1 == user_email2:
            user_obj.email_update(user_email1)
        elif user_email1 != user_email2:
            print("These do not match. Please try again!")

    if user_input == '3':
        user_first = input('Please enter your new first name:')
        user_last = input('Please enter your new last name:')
        user_obj.edit_name(user_first,user_last)

    if user_input == '4':
        user_pwd1 = input('Please enter your new password:')
        user_pwd2 = input('Please confirm your new password:')
        if user_pwd1 == user_pwd2:
            bytes = user_pwd1.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes,salt)
            user_obj.change_password(hash)
        elif user_pwd1 != user_pwd2:
            print('These do not match. Please try again!')

    if user_input == '5':
        user_obj.view_competency(user_obj.user_id)

    if user_input == '6':
        user_obj.view_assess_results(user_obj.user_id)

    if user_input == '7' or user_input.upper() == 'Q':
        logout()

def manager_menu(man_obj):
    user_input = input('''
    \n***MANAGER MENU***

    Please select from the following options:
    
    1:  User Menu.
    2:  Search For a User.
    3:  VIEW.
    4:  ADD.
    5:  EDIT.
    6:  DELETE an Assessment Result.
    7:  ACTIVATION/DEACTIVATION.
    8:  EXPORT CSV User Competency Report.
    9:  EXPORT PDF User Competency Report.
    10: EXPORT CSV All Competencies for All Users Report.
    11: IMPORT Assessment Results.
    12: Quit (Q)
    
    >>>''')

    if user_input == '1':
        user_menu(man_obj)
        

    if user_input == '2':
        user = man_obj.user_search()
        # if user:
        #     user.view_user()

    if user_input == '3':
        user_input1 = input('''
        \n*** VIEW MENU***
        
        Please choose from the following menu:
        
        1: View all Users.
        2. View a Competency Report for ALL Users.
        3. View a Competency Report for an Individual User.
        4. View a List of Assessments for an Individual User.
        ENTER to Quit

        >>>
        ''')
        if user_input1 == '1':
            man_obj.view_all_users()
        if user_input1 == '2':
            man_obj.view_comp_all_users()
        if user_input1 == '3':
            man_obj.view_comp_level_user()
        if user_input1 == '4':
            man_obj.view_assess_list_user()

    if user_input == '4':
        user_input1 = input('''
        \n*** ADD MENU ***
        
        Please choose from the following menu:

        1: Add a NEW User.
        2: Add a NEW Competency.
        3: Add a NEW Assessment.
        4. Add a NEW Assessment Result for a User.
        ENTER to Quit.

        >>>
        ''')
        if user_input1 == '1':
            print('\nPlease enter the following information:\n')
            first_name =input("First name: ")
            last_name =input("Last name: ")
            phone = input("Phone Number: ")
            email = input("Email: ")
            while not email:
                email = input("Email is required: ")
            password = input("Password: ")
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes,salt)
            password = hash
            while not password:
                password = input("Password is required: ")
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            date_created = datetime.now().date()
            hire_date = input('Please enter the hire date YYYY-MM-DD: ')
            user_type = int(input('Please enter 0 for User and 1 for Mananger: '))

            man_obj.add_user(first_name,last_name, phone, email, password, active, date_created, hire_date, user_type)

        if user_input1 == '2':
            print('\nPlease enter the following information:\n')
            cat_name =input("Competency name: ")
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.add_new_competency(cat_name,active)
            
        if user_input1 == '3':
            man_obj.view_all_categories()
            print('\nPlease enter the following information:\n')
            assess_name =input("Assessment name: ")
            date_created = datetime.now().date()
            category_id = int(input("Please enter the Competency ID from the above list: "))
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.add_new_assessment(assess_name,date_created,category_id,active)
            
        if user_input1 == '4':
            man_obj.view_all_assessments()
            assess_id =input("\nPlease enter the Assessment ID from the Assessment list: ")
            man_obj.user_search()
            user_id = int(input('\nPlease enter the User ID from the above list: '))
            score = int(input("""Score Rubric:
            0 - No competency - Needs Training and Direction
            1 - Basic Competency - Needs Ongoing Support
            2 - Intermediate Competency - Needs Occasional Support
            3 - Advanced Competency - Completes Task Independently
            4 - Expert Competency - Can Effectively pass on this knowledge and can initiate optimizations
            
            Please enter the score (0-4): """))
            date_taken = input("Please enter the date taken (YYYY-MM-DD): ")
            man_obj.view_managers()
            manager = int(input("\nPlease enter the Manager ID: "))
            man_obj.add_new_result(user_id,assess_id,score,date_taken,manager)        
   
    if user_input == '5':
        user_input1 = input('''
        \n*** EDIT MENU ***
        
        Please choose from the following menu:

        1: EDIT a User.
        2: EDIT a Competency.
        3: EDIT a Assessment.
        4. EDIT an Assessment Result.
        ENTER to Quit.

        >>>
        ''')
        if user_input1 == '1':
            user_obj = man_obj.user_search()
            print("""
            \nPlease note that ALL fields are required for the update, if the information has not changed, please enter the previous information.
            Please enter the following information:\n""")
            first_name = input('Please enter the first name: ')
            last_name = input('Please enter the last name: ')
            phone = input("Please enter the phone number: ")
            email = input("Please enter the email address: ")
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.edit_user(user_obj,first_name,last_name,phone,email,active)
            
        if user_input1 == '2':
            man_obj.view_all_categories()
            print('\nPlease enter the following information:\n')
            category_id = int(input('Please enter the Competency ID: '))
            cat_name = input("Please enter the Competency name: ")
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.edit_competency(category_id, cat_name, active)

        if user_input1 == '3':
            man_obj.view_all_assessments()
            print('\nPlease enter the following information:\n')
            assessment_id = int(input('Please enter the Assessment ID: '))
            assess_name = input("Please enter the Assessment name: ")
            active = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.edit_assessment(assessment_id, assess_name, active)

        if user_input1 == '4':
            man_obj.view_all_results_user()
            print('\nPlease enter the following information:\n')
            result_id = int(input('Please enter the Result ID: '))
            score = int(input("Please enter the score (0-4): "))
            date_taken = input('Please enter the date taken: ')
            man_obj.edit_result(result_id,score,date_taken)

    if user_input == '6':
        print("\nPlease note that deletion is PERMANENT and CANNOT be reversed - please ensure the result you are deleting is the correct one.")
        man_obj.view_all_results_user()
        result_id = input('\nWhich Result ID would you like to delete: ')
        man_obj.delete_result(result_id)

    if user_input == '7':
        act_input = input('''
       *** ACTIVATION / DEACTIVATION MENU ***

        Please select an option to change:

        1: User
        2: Competency
        3: Assessment
        4: Manager
        ENTER to Quit.

        >>>
        ''')
        if act_input == '1':
            man_obj.view_all_users()
            act_user = int(input('\nPlease enter the User ID: '))
            act_deact = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.user_activation(act_user,act_deact)
        if act_input == '2':
            man_obj.view_all_categories()
            act_comp = int(input('\nPlease enter the Competency ID: '))
            act_deact = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.comp_activation(act_comp,act_deact)
        if act_input == '3':
            man_obj.view_all_assessments()
            act_assess = int(input('\nPlease enter the Assessment ID: '))
            act_deact = int(input('Please enter 1 for active and 0 for inactive: '))
            man_obj.assess_activation(act_assess,act_deact)
        if act_input == '4':
            man_obj.view_all_users()
            act_man = int(input('\nPlease enter the User ID: '))
            act_deact = int(input('Please enter 1 for manager and 0 for user: '))
            man_obj.manager_activation(act_man,act_deact)

    if user_input == '8':
        print('\nPlease search for the User you would like to export the User Competency Report for.\n')
        user_obj = man_obj.user_search()
        man_obj.export_csv_user_comp(user_obj)

    if user_input == '9':
        print('\nPlease search for the User you would like to export the User Competency Report for.\n')
        user_obj = man_obj.user_search()
        man_obj.export_csv_user_comp(user_obj)
        man_obj.pdf_conv_user_comp()

    if user_input == '10':
        man_obj.export_csv_alluser_results()

    if user_input == '11':
        man_obj.import_csv_assess_results()

    if user_input == '12' or user_input.upper() == 'Q':
        logout()




print("\n\n***WELCOME TO INFINITY CODE'S COMPETENCY TRACKER***\n")
while True:
    user = login()
    if user is None:
        continue
    else:
        break

while True:
    if user.user_type == 1:
        manager_menu(user)

    elif user.user_type == 0:
        user_menu(user)

    menu_input = input('\nPress Enter to view the menu again OR press Q to quit: ')
    if menu_input.lower() == 'q':
        print('Goodbye!')
        break
    else:
        continue
