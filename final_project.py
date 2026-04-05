def get_student_id():
    """
    Prompt the user until they enter a valid student id.

    Parameters:
    no parameters

    Returns:
    - int: The integer entered by the user
    """

    while True:
        student_id = input("Please enter student id: ")
        if student_id.isdigit() and len(student_id) == 8:
            return student_id
        print("ERROR: Student ID must be exactly 8 digits.")

def get_student_email():
    """
    Prompt the user until they enter a valid email address.

    Parameters:
    no parameters

    Returns:
    - str: The string entered by the user
    """

    while True:
        email = input("Please enter student's email address: ")

        if "@" not in email or "." not in email:
            print("ERROR: Email must contain both '@' and '.'.")
            continue

        parts = email.split("@")

        if len(parts) != 2:
            print("Error: Email must contain only one '@'.")
            continue

        username = parts[0]
        domain = parts[1]

        if username == "":
            print("ERROR: Email must have username before '@'.")
            continue

        if domain == "":
            print("ERROR: Email must have domain after '@'.")
            continue

        return email
    
def validate_string_input(prompt):
    """
    Prompt the user until they enter a valid alphabet input.

    Parameters:
    - prompt (str): The message displayed to the user

    Returns:
    - str: The string entered by the user
    """

    while True:
        text = input(prompt).strip()
        if text == "":
            print("ERROR: This field cannot be empty.")
            continue
        
        contain_number = False
        for characters in text:
            if characters.isdigit():
                contain_number = True
                break
        
        if contain_number:
            print("ERROR: Name cannot contain numbers.")
            continue
        
        return text

def validate_integer_input(prompt):
    """
    Prompt the user until they enter a valid integer input.

    Parameters:
    - prompt (str): The message displayed to the user

    Returns:
    - int: The number entered by the user
    """

    while True:
        number = input(prompt).strip()
        if number == "":
            print("ERROR: This field cannot be empty.")
            continue
        
        contain_alphabet = False
        for characters in number:
            if characters.isalpha():
                contain_alphabet = True
                break
        
        if contain_alphabet:
            print("ERROR: This field cannot contain alphabet.")
            continue
        
        #check for decimal
        if float(number) - float(number)//1 != 0:
            print("ERROR: Please enter an integer.")
            continue
    
        return int(number)

def validate_float_input(prompt):
    """
    Prompt the user until they enter a valid float input.

    Parameters:
    - prompt (str): The message displayed to the user

    Returns:
    - float: The number entered by the user
    """

    while True:
        number = input(prompt).strip()
        
        if number == "":
            print("ERROR: This field cannot be empty.")
            continue
        
        try:
            value = float(number)
            return value
        
        except ValueError:
            print("Please enter a valid number (no alphabet allowed).")
    
while True:
    print(f" 1) Add a new student \n 2) Add a new course \n 3) Record student marks \n 4) Display individual student performance \n 5) Display course performance summary \n 6) Exit")
    selection = input("Please enter your selection (1-6): ")

    #check if the selection is a number
    if not selection.isdigit():
        print("ERROR: Please enter a number between 1 and 6")
        continue
    
    #enter student detais (ID, Name, Email) into students.txt file
    if int(selection) == 1:
        with open('students.txt','a') as students_detail:

            student_id = get_student_id()
            student_name = validate_string_input("Please enter student name: ")
            email = get_student_email()
            profile = str(student_id) + "," + student_name + "," + email +"\n"

            students_detail.write(profile)

    #enter course details (ID, name) into the courses.txt file
    elif int(selection) == 2:
        with open('courses.txt','a') as courses:

            course_id = validate_integer_input("Please enter the course ID: ")
            course_name = validate_string_input("Please enter the full course name (e.g., 'Mathematics', not 'Math'): ")

            courses.write(str(course_id) + ", " + course_name + "\n")

    #enter student's grade (Student ID, Course Name, Marks, Letter Grade) into the grades.txt file
    elif int(selection) == 3:
        student_id = get_student_id()

        #check if the student ID arleady exist in the database
        exist = False
        with open('students.txt','r') as records:
            for record in records:
                parts = record.strip().split(",")
                if parts[0] == str(student_id):
                    exist = True
                    break
                
        if not exist:
            print("ERROR: Student ID not found. Please register the student first.")
            continue

        with open('grades.txt','a') as grades:
            number_of_subjects = validate_integer_input("Please enter the number of subjects enrolled by the student: ")
            count = 0
            subject_score = []

            #allow user to enter the subject details for a specific number of times specified
            while number_of_subjects > count:

                course_name = validate_string_input("Please enter the full course name (e.g., 'Mathematics', not 'Math'): ")
                exist = False
                with open('courses.txt','r') as records:
                    for record in records:
                        parts = record.strip().split(",")
                        if parts[1].strip().lower() == course_name.strip().lower():
                            exist = True
                            break

                if not exist:
                    print("ERROR: Course name is not found. Please register the course first.")
                    break
                            
                while True:
                    marks = validate_float_input("Please enter student's score: ")
                    if 0 <= marks <= 100:
                        break 
                    else:
                        print("ERROR: Marks must be between 0 and 100.")

                if marks >= 90:
                    letter_grade = "A*"
                elif marks >= 80:
                    letter_grade = "A"
                elif marks >= 70:
                    letter_grade = "B"
                elif marks >= 60:
                    letter_grade = "C"
                elif marks >= 50:
                    letter_grade = "D"
                elif marks < 50:
                    letter_grade = "F"

                count+=1
                subject_score.append((course_name, marks, letter_grade))

            if count == number_of_subjects:
                grades.write( "\n" + str(student_id) + " , " + str(subject_score)[1:-1])

    #read and print the student's academic performance specified by the user with student ID
    elif int(selection) == 4:

        student_id = get_student_id()
        found = False
        
        with open('grades.txt','r') as grades:
            records = grades.readlines()    

            #loop through the records of students' academic detail and check if the specified student ID is in the record 
            for record in records:
                if record.startswith(str(student_id)):
                    with open('students.txt','r') as students_detail:
                        records = students_detail.readlines()

                        #loop through the students profile records and check if the specified student ID exists
                        for student_profile in records:
                            if student_profile.startswith(str(student_id)):
                                print(f"Student Profile: {student_profile.strip()}")
                                print(f"Academic Performance: {record[10:].strip()}")
                                found = True

            #inform user if the specified student ID is not in the records
            if not found:
                print("No record found for this student id")
    
    #show students' peformance of a specific subject with average, highest and lowest marks.
    elif int(selection) == 5:
        with open('courses.txt','r') as courses:
            records = courses.readlines()
            course_name = validate_string_input("Please enter the course name: ")
            found = False

            #loop through the courses recorded in the courses.txt and look for the course ID for the course specified by the user
            for record in records:
                record = record.strip().split(",")
                if course_name.strip().lower() == record[1].strip().lower():
                    found = True
                    course_id = record[0]
                    
                    print(f"                             Course ID: {course_id}  Course Name: {course_name}")
                    print("____________________________________________________________________________________________")
                    with open('grades.txt','r') as grades_file:

                        score_list = []
                        record_list = []
                        total_score = 0
                        accumulator = 0
                        
                        #loop through the grade details of student recorded in grades.txt file
                        for record in grades_file:
                            record = record.strip()  
                            
                            #separate the student id from the records
                            parts = record.split(', (')
                            student_id = parts[0].strip()
                            course_parts = parts[1:]
                            
                            #process each courses
                            for course_info in course_parts:
                                course_info = course_info.strip()
                                if course_info.endswith(')'):
                                    course_info = course_info[:-1]
                                elif course_info.endswith("),"):
                                    course_info = course_info[:-2]
                                
                                #split course data
                                course_data = []

                                parts = course_info.split(",")

                                #clean the data extracted by removing those unnecesary symbols
                                for item in parts:
                                    cleaned_data = item.strip().strip("'")
                                    course_data.append(cleaned_data)
                                
                                #check if each students' grade record consist of course name, score and letter grade
                                if len(course_data) == 3:
                                    course, score, letter_grade = course_data
                                    score = float(score)

                                    #check if the subject matches the entered course name
                                    if course.strip().lower() == course_name.strip().lower():
                                        record_list.append((student_id, score, letter_grade))
                                        score_list.append(score)
                                        total_score += score
                                        accumulator += 1

                        #display results
                        counter = 0
                        score_list.sort()
                        for record in record_list:
                            counter += 1
                            print(f"{counter}. {record}")
                        print(f"Average Score: {total_score/accumulator:.2f}")
                        print(f"Highest Score: {score_list[-1]}")
                        print(f"Lowest Score: {score_list[0]}")

            #inform user if the course does not exist in the courses.txt file
            if not found:
                print(f"No record found for this course: {course_name}")

    #halt the program
    elif int(selection) == 6:
        print("Program Halt")
        break
    
    #Prompt the user for a valid selection
    else:
        print("Please enter a valid selection.")
        continue





