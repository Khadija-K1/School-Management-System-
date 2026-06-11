
# ---------------- Database ---------------

students_data = {}
classes = {}
teachers_data = {}

# Admin LogIn Data
admin_data = {
    "name": "usman",
    "password": "123"
}

# --------------- File Handling -----------
import json

# Load data from file:
def load_data():
    global students_data, classes, teachers_data
    try:
        with open ("school_data.json", "r") as file: 
            data = json.load(file)
        students_data = data["students"]
        classes = data["classes"]
        teachers_data = data["teachers"]

    except (FileNotFoundError, json.JSONDecodeError):
        print()

# Data load
load_data()

# Save data to file:
def save_data():
    data = {
        "students" : students_data,
        "classes" : classes,
        "teachers" : teachers_data
    }

    with open ("school_data.json", "w") as file: 
        json.dump(data, file, indent= 5)


# ----------------- Admin Block--------------------- 


# ------------ Class management System Main Menu:
def manage_classes(classes): 
    print("1- Add class")
    print("2- View classes")

    option = input("Choose an option: ")

    if option == "1":
      add_classes(classes)

    elif option == "2": 
        display_classes(classes)

    else: 
        print("Invalid!")


# Add Classes: 
def add_classes(classes): 
   while True:
        enter_class = input("Enter a class: ").strip()
        
        if enter_class in classes: 
           print("class already exists")
        elif enter_class == "":
            print("Invalid!")
        else: 
            print("Class added successfully")
            classes[enter_class] = {
                "subjects" : [],
                "students" : {}
            }
            save_data()
        
        # Do u want to add another class:
        if not ask_yes_no("Do u want to add another class (y/n): "):
            break 


# Display Classes: 
def display_classes(classes): 
    if not classes: 
        print("No classes exists")
        return

    for class_name, class_data in classes.items(): 
        print(f"\n====== Class {class_name} ======")
        if not class_data["subjects"]:
            print(f"Subjects: No subjects assigned.")
        else:
            print(f"Subjects: {', '.join(class_data['subjects'])}")
    
        if not class_data["students"]: 
            print(f"Students: No students enrolled.")
        else:
           print(f"\nStudents: ")
           print("ID   :   Name")
           for student_id, student_name in class_data["students"].items(): 
             print(f"{student_id}   :   {student_name}")


# Displaying only classes names: 
def class_names(classes): 
    print("\nAvailable classes:")
    for class_name, class_data in classes.items(): 
        print(f"{class_name}")


# Assigning Subjects to Classes:
def assign_subjects(classes): 
   if not classes: 
     print("No class exists. Add class first")
     return
 
   # Displaying only classes names:
   class_names(classes)

   enter_class = input("Select class to add subjects: ").strip()

   if enter_class not in classes:
        print("Class not found.") 
        return
                              
   while True:
        enter_subject = input("Enter the subject you want to add: ").strip().lower()

        if enter_subject in classes[enter_class]["subjects"]:
            print("Subject already exists")

        elif enter_subject != "":
            classes[enter_class]["subjects"].append(enter_subject)
            print("Subject successfully added")
            save_data()

        else: 
            print("Invalid")
        
        # Do u want to add another subject (yes/no)
        if not ask_yes_no("Do u want add another subject (y/n): "): 
            break
        

# Add another class/subject --> yes/no?
def ask_yes_no(question): 
   while True:
     add_another = input(question).lower().strip()

     if add_another in ["yes", "y"]: 
         return True

     elif add_another in ["no", "n"]:
         return False
                    
     else:
         print("Enter y/n")


# Deleting Student/Teacher --> Are you sure(y/n): 
def ask_confirm(message):
    while True:
        confirm = input(message).lower().strip()

        if confirm in ["y", "yes"]:
            return True
        elif confirm in ["n", "no"]:
            print("Deletion cancelled")
            return False
        else:
            print("Enter y/n")


# ---------------Validation Systems: 

# ID validation -- Student/Teacher: 
def valid_id(students_data, s_id):
    if s_id in students_data:
        print("ID already exists")
        return False
    if not s_id:
        print("It can't be empty. Enter something")
        return False
    
    return True

# Name Validation: 
def valid_name(s_name): 
    if not s_name: 
        print("Name cannot be empty.")
        return False
            
    if not (all(n.isalpha() for n in s_name.split())):
        print("Invalid name! Enter only letters in the name")
        return False
    
    return True

# Password validation -- Empty Password check: 
def valid_pass(s_password):
    if not s_password:
        print("Password can't be empty")
        return False 
    
    return True

# Class Validation: 
def valid_class(s_class):
    if not s_class:
        print("Class can't be empty")
        return False

    if s_class not in classes: 
        print("Class not found.")
        return False 
    
    return True


# -------------Student Management System Menu:

def manage_students(students_data): 
    if not classes: 
        print("No class exists. Add a class first")
        return
    
    while True:
        print("\n1- Add students")
        print("2- View all students")
        print("3- Delete students")
        print("4- Update student info")
        print("5- Exit")

        s_option = input("Choose an option: ").strip()

        if s_option == "1": 
            add_students(students_data)

        elif s_option == "2": 
            display_students(students_data)
                         
        elif s_option == "3": 
            delete_student(students_data)
                        
        elif s_option == "4": 
            update_student(students_data)

        elif s_option == "5": 
            print("Exiting students block...")
            break 
                      
        else: 
            print("Invalid!")


# Admin --> Add Students:
def add_students(students_data): 
    while True:
        s_id = input("\nEnter student's id: ").strip()
        if not valid_id(students_data, s_id):
            continue
 
        s_name = input("Enter student's name: ").strip()
        if not valid_name(s_name):
            continue
              
        s_password = input("Set a password: ").strip()
        if not valid_pass(s_password):
            continue
        
        # displaying only classes names
        class_names(classes)

        s_class = input("\nAssign a class from the above: ")
        if not valid_class(s_class):
            continue
        
        print("Class assigned successfully")
        students_data[s_id] = {
            "name" : s_name, 
            "password" : s_password, 
            "class" : s_class,
        }
        save_data()
                    
        if s_id not in classes[s_class]["students"]:
            classes[s_class]["students"].setdefault(s_id, s_name)
            save_data()

        else: 
            print("ID already exists")

        # Do u want to add another student:        
        if not ask_yes_no("Do u want to add another student (y/n): "): 
            break


# Display Students: 
def display_students(students_data): 
    if not students_data: 
        print("No students found")
        return
 
    print("\n====== Student's Data ======")
    print(f"\n{'ID':<10} {'Name':<15} {'Password':<15} {'Class':<10}")
    print("-" * 55)

    for student_id, student_data in students_data.items():

        print(
        f"{student_id:<10} "
        f"{student_data['name']:<15} "
        f"{student_data['password']:<15}" 
        f"{student_data['class']:<10}"
        )


# Delete student: 
def delete_student(students_data):
    if not students_data:
        print("No students found")
        return
    
    display_students(students_data)
    student_id = input("Which id to delete: ").strip()
    if student_id not in students_data:
        print("ID not found.")
        return
    
    if ask_confirm("Are you sure(y/n): "):
        student_class = students_data[student_id]["class"]
        if student_id in classes[student_class]["students"]:
            del classes[student_class]["students"][student_id]

            # Deleting student ID from student's database
            del students_data[student_id]
            print("ID deleted!")
            save_data()


# Update student info: 
def update_student(students_data):
    if not students_data:
        print("No students found")
        return

    display_students(students_data)
    student_id = input("\nWhich id do u want to update: ").strip()
    if student_id not in students_data:
        print("ID not found")
        return
    
    while True:
        print("\n1- Name")
        print("2- Password")
        print("3- Class")
        print("4- Exit")

        update_std = input("What do u want to update: ").strip()

        if update_std == "1":
            new_name = input("Enter the new name: ").strip()

            if not valid_name(new_name):
                continue

            students_data[student_id]["name"] = new_name
            print("Name updated successfully")
            save_data()


        elif update_std == "2":
            new_pass = input("Enter the new password: ")

            if not valid_pass(new_pass):
                continue
            
            students_data[student_id]["password"] = new_pass
            print("Password updates successfully")
            save_data()
                    
        elif update_std == "3":
            # showing only classes names:
            class_names(classes)
                    
            # Assigning new class from the avalable classes: 
            new_class = input("Assign a new class from the above: ")
            if new_class in classes:

                # Deleting student_id from old class in class database: 
                old_class = students_data[student_id]["class"]
                if student_id in classes[old_class]["students"]:
                  del classes[old_class]["students"][student_id]
                  save_data()
                
                # Appending student_id in new class's database: 
                classes[new_class]["students"].setdefault(student_id, students_data[student_id]["name"])
                save_data()

                # Assigning new class to student in student's database
                students_data[student_id]["class"] = new_class
                print("Class updated successfully")
                save_data()
            else: 
                print("Class not found")

        elif update_std == "4":
            print("Exiting student update block...")
            break

        else:
            print("Invalid!")
                    


# ----------------Teacher Management System Menu:

# Teacher -- Main Menu:
def manage_teachers(teachers_data): 
    if not classes: 
        print("No class exists. Add a class first")
        return
     
    while True:
        print("\n1- Add teacher")
        print("2- Assign class to teacher")
        print("3- View all teachers")
        print("4- Delete teacher")
        print("5- Update teacher info")
        print("6- Exit")

        t_option = input("Choose an option: ").strip()

        if t_option == "1": 
            # Add teacher
            add_teacher(teachers_data)
    
        elif t_option == "2":
            # assign class + subject
            t_assign_class(teachers_data)

        elif t_option == "3": 
            # View teachers
            print("View teachers")
            display_teachers(teachers_data)
                         
        elif t_option == "4": 
            # delete teacher
            delete_teacher(teachers_data)
                        
        elif t_option == "5": 
            # update teacher 
            update_teacher(teachers_data)

        elif t_option == "6": 
            print("Exiting teachers block...")
            break 
                      
        else: 
            print("Invalid!")


# Add teacher: 
def add_teacher(teachers_data): 
    while True:
        t_id = input("\nEnter teacher's id: ").strip()
        if not valid_id(teachers_data,t_id):
            continue
        
        t_name = input("Enter teacher's name: ").strip()
        if not valid_name(t_name):
            continue
          
        t_password = input("Set a password: ").strip()
        if not valid_pass(t_password):
            continue

        teachers_data[t_id] = {
            "name" : t_name,
            "password" : t_password,
            "assigned_classes" : {}
          }
        print("Teacher created successfully.")
        save_data()
        
        if not ask_yes_no("Do u want to add another teacher (y/n): "): 
            break


# assign/update class + sub for teacher -- specifically for update class & sub later on: 
def assign_class_sub(teachers_data, t_id):
    while True:
        print("\nAvailable classes and subjects")
        for key, value in classes.items():
            print(f"\n==== Class {key} =====")
            print(f"Subjects: {','.join(value['subjects'])}")

        assign_class = input("\nAssign a class: ").strip()
        
        if not valid_class(assign_class):
            continue
          
        if not classes[assign_class]["subjects"]: 
            print("No subjects exist for this class. Add subjects first")
            return
          
        assign_subject = input(f"Assign a subj of classs {assign_class} to the teacher: ").lower()

        if assign_subject in classes[assign_class]["subjects"]: 
            already_assigned = False

            for teacher in teachers_data.values():
                if assign_class in teacher["assigned_classes"]:
                    if assign_subject in teacher["assigned_classes"][assign_class]:
                        print("Subject of this class is reserved(already assigned)")
                        already_assigned = True
                        break

            if not already_assigned:
                teachers_data[t_id]["assigned_classes"].setdefault(assign_class, [])
                if assign_subject not in teachers_data[t_id]["assigned_classes"][assign_class]:
                    teachers_data[t_id]["assigned_classes"][assign_class].append(assign_subject)
                    print("Class & subject successfully assigned.")
                    save_data()
                        
        else: 
            print("Subject doesn't exist in the class")
         

        if not ask_yes_no("Do u want to assign another class: "):
            print("okayyy!")
            break
 

# View Assigned classes and subjects for teachers:
def already_assigned(teachers_data, t_id):

    if not teachers_data[t_id]["assigned_classes"]: 
        print("No classes/subjects are currently assigned for this teacher.")
        return
   
    print(f"\nAlready assigned:")

    for class_name, subjects in teachers_data[t_id]["assigned_classes"].items(): 
        print(f"Class {class_name}: {','.join(subjects)} ")
              

# Assigning class & sub to teacher -- assign class/sub in first attempt: 
def t_assign_class(teachers_data): 
    if not teachers_data:
        print("No teachers exist. Add teacher's first.")
        return
    
    if not classes:
        print("No classes yet! Add class first")
        return
    
    # Displaying teacher's data -- only id and name
    t_id_name(teachers_data)
    
    t_id = input("Enter teacher's id: ")

    if t_id in teachers_data:
     assign_class_sub(teachers_data, t_id)
    else: 
        print("Id doesn't exist")


# Displaying teachers id and name only: 
def t_id_name(teachers_data):
    print("\nAvailable Teachers: ")
    print("ID    :    Name")
    for key, value in teachers_data.items(): 
         print(f"{key}          {value['name']}")


# Display teacher -- all data: 
def display_teachers(teachers_data): 
    if not teachers_data: 
        print("No teachers found")
        return
    
    print("\n====== Teacher's Data ======")
    print(f"\n{'ID':<10} {'Name':<15} {'Password':<15}")
    print("-" * 45)

    for teacher_id, teacher_data in teachers_data.items():
        print(
        f"{teacher_id:<10}"
        f"{teacher_data['name']:<15}"
        f"{teacher_data['password']:<15}"
        )
        assigned = teacher_data["assigned_classes"]
        
        if not assigned:
            print("\nNo assigned classes and subjects")
        else: 
            print("\nAssigned Classes and Subjects")

            for class_name, subjects in assigned.items():
                print(
                    f"Class {class_name:<5}:  {','.join(subjects)}"
                )
        print(f"\n{'-' * 45}")


# Delete teacher: 
def delete_teacher(teachers_data):
    if not teachers_data:
        print("No teachers found")
        return

    display_teachers(teachers_data)
    teacher_id = input("\nWhich id to delete: ").strip()
    if teacher_id not in teachers_data:
        print("ID not found.")
        return
   
    if ask_confirm("Are you sure(y/n): "): 
        del teachers_data[teacher_id]
        print("Teacher deleted")
        save_data()

# Remove subject from a class: 
def remove_teacher_sub(teachers_data, t_id):

    already_assigned(teachers_data, t_id)

    remove_class = input("Which class do u want to remove: ").strip()
    if remove_class not in teachers_data[t_id]["assigned_classes"]:
        print("class doesn't exist")
        return
     
    remove_sub = input("Enter the subject u want to remove: ").lower()
    if remove_sub not in teachers_data[t_id]["assigned_classes"][remove_class]:
        print("Subject doesn't exist for this class")
        return

    teachers_data[t_id]["assigned_classes"][remove_class].remove(remove_sub)
    print("Subject has been removed successfully from this class")
    save_data()


# Remove entire class: 
def remove_teacher_class(teachers_data, t_id):
     
     already_assigned(teachers_data, t_id)

     all_class = input("Enter the class u want to remove: ").strip()

     if all_class in teachers_data[t_id]["assigned_classes"]:
         del teachers_data[t_id]["assigned_classes"][all_class]
         print("Class and It's subjects are deleted successfully")
         save_data()
     else: 
         print("class doesn't exist")


# Update teacher info: 
def update_teacher(teachers_data):
    if not teachers_data:
        print("No teachers found")
        return
    
    t_id_name(teachers_data)

    t_id = input("\nWhich id do u want to update: ").strip()

    if t_id not in teachers_data:
        print("ID not found")
        return

    while True:
        print("\n1- Name")
        print("2- Password")
        print("3- Update Class & Subject")
        print("4- Remove Subject")
        print("5- Remove entire class including all subjects")
        print("6- Exit")
            
        update_t = input("What do u want to update: ").strip()

        if update_t == "1":
            new_name = input("Enter the new name: ")
            teachers_data[t_id]["name"] = new_name
            print("Name updated successfully")
            save_data()

        elif update_t == "2":
            new_pass = input("Enter the new password: ")
            teachers_data[t_id]["password"] = new_pass
            print("Password updates successfully")
            save_data()
                
        # assigning new class + sub
        elif update_t == "3":
            # showing alredy assigned classes + subects for better UX.
            already_assigned(teachers_data, t_id)
            print("--")
        
            # assigning/updating new class + sub of that class
            assign_class_sub(teachers_data, t_id)
                
        # removing sub from a class
        elif update_t == "4": 
            remove_teacher_sub(teachers_data, t_id)
                
        # remove entire class
        elif update_t == "5": 
            remove_teacher_class(teachers_data, t_id)

        elif update_t == "6": 
            print("Exiting teacher update block...")
            break 
        else: 
            print("Invalid!")
    


# ------------ Admin Log In Menu ----------------
def admin_login(admin_data):

    admin_name = input("Enter your name: ").strip()
    admin_pass = input("Enter your password: ").strip()

    if (admin_name == admin_data["name"]) and (admin_pass == admin_data["password"]):

        while True:
            print("\n1- Manage classes")
            print("2- Assign subjects to classes")
            print("3- Manage students")
            print("4- Manage teachers")
            print("5- Exit")

            choice = input("Choose an option: ").strip()

            # Manage classes
            if choice == "1": 
                manage_classes(classes)

            # Assign subjects to classes
            elif choice == "2": 
                assign_subjects(classes)

            # Managing students
            elif choice == "3": 
                # chnage password for student wala option??
                manage_students(students_data)
                
            # Manage teachers:
            elif choice == "4":
                manage_teachers(teachers_data)        
                                 
            elif choice == "5": 
                print("Exiting admin block...")
                break

            else:
                print("Invalid! Choose from the options available")
    
    else: 
        print("Incorrrect username or password")



# ----------------- Teacher LogIn --------------------

# Password update: 
def t_pass_update(teachers_data, t_id):
     old_pass = input('Enter your old password: ').strip()

     if old_pass == teachers_data[t_id]["password"]:
         new_pass = input("Choose a new password: ").strip()

         teachers_data[t_id]["password"] = new_pass
         save_data()
         print("Password has changed successsfully")

     else: 
         print("Incorrect password")


# Choose class + sub to assign grades:
def choose_class_sub(teachers_data, t_id):

     class_name = input("\nChoose a class: ").strip()

     if class_name not in teachers_data[t_id]["assigned_classes"]:
        print("Class not assigned")
        return None, None
               
     assigned_subjects = teachers_data[t_id]["assigned_classes"][class_name]
     print(f"Subjects: {','.join(assigned_subjects)}")


     subject = input("Choose a sub from that class: ").strip().lower()

     if subject not in teachers_data[t_id]["assigned_classes"][class_name]:
         print("Invalid subject")
         return None, None
     
     return class_name, subject


# Assign grades, marks: 
def assign_marks(class_name, subject, teachers_data, t_id): 

    s_id = input("Enter student id: ").strip()
    if s_id in classes[class_name]["students"]:
         s_marks = input("Enter student's marks: ")

         students_data[s_id].setdefault("marks", {})
         
         if subject not in students_data[s_id]["marks"]:
            students_data[s_id]["marks"][subject] = {"sub_marks" : s_marks, "Teacher" : teachers_data[t_id]["name"]}
            save_data()
         
            print("Marks has assigned sucessfully")

         else:
            students_data[s_id]["marks"][subject]["sub_marks"] = s_marks
            save_data()
         
            print("Marks has updated sucessfully")
             

    else:
          print("Id doesn't exist")



# Show students of a particular class/subject:
def show_students(class_name):
    print(f"\nStudents in Class {class_name}")
    print("ID    :    Name")

    for student_id, student_name in classes[class_name]["students"].items():
        print(f"{student_id}    :    {student_name}")
    

# View student's marks: 
def view_students_marks(students_data, subject, class_name):
    print("\nStudent's Marks")
    print(f"{'ID':<5} {'Name':<10} {'Marks':<5}")

    student_data = classes[class_name]["students"]

    if not student_data:
         print("Student's doesn't exist")
         return
    

    for student_id, student_name in student_data.items():   
        marks = students_data[student_id].get("marks", {})

        subject_data = marks.get(subject, {})
        student_marks = subject_data.get("sub_marks", "Not assigned")
        
        print(f"{student_id:<5} {student_name:<10} {student_marks:<5}")



# ----------------- Teacher Main Menu:
def teacher_logIn(teachers_data): 
    if not teachers_data: 
        print("Can't login right now.")
        return
 
    t_id = input("Enter your ID: ").strip()
    t_pass = input("Enter your password: ").strip()

    if (t_id in teachers_data) and (teachers_data[t_id]["password"] == t_pass):

     while True:
        print("\n1- View assigned classes & subjects")
        print("2- Assign/Update marks")
        print("3- View Student's marks")
        print("4- Change password")
        print("5- LogOut")

        select = input("\nChoose an option: ").strip()

        if select == "1": 
            already_assigned(teachers_data, t_id)

        elif select == "2":
            already_assigned(teachers_data, t_id)
            class_name, subject = choose_class_sub(teachers_data, t_id)

            if class_name is None: 
                print("Select clas & sub first")
                continue

            show_students(class_name)
            assign_marks(class_name, subject, teachers_data, t_id)

        elif select == "3": 
            already_assigned(teachers_data, t_id)
            class_name, subject = choose_class_sub(teachers_data, t_id)

            if class_name is None: 
                print("Select class & subject first.")
                continue

            view_students_marks(students_data, subject, class_name)
           
        elif select == "4": 
            t_pass_update(teachers_data, t_id)

        elif select == "5": 
            print("Exiting teacher logIn block....")
            break

        else: 
            print("Invalid")
    
    else: 
        print('Incorrect username or password')



# ----------------------- Student LogIn System -----------------

def student_logIN(students_data):
    if not students_data:
        print("Can't log in right now.")
        return
    s_id = input("Enter your student id: ")
    s_pass = input("Enter your password: ")

    if (s_id in students_data) and s_pass == students_data[s_id]["password"]:
        print(f"\n{'ID':<5} {'Name':<10} {'class':<5}")

        s_name = students_data[s_id]["name"]
        s_class = students_data[s_id]["class"]

        print(f"{s_id:<5} {s_name:<10} {s_class:<5} ")

        print("\nYour Marks:")
        print(f"\n{'Subjects':<8} {'Marks':<5} {'Teacher':<10}")
         
        s_subjects = students_data[s_id].get("marks", {})

        if not s_subjects:
            print("No marks available")
            return


        for subject, sub_data in s_subjects.items():
             print(f"{subject:<8} {sub_data['sub_marks']:<5} {sub_data['Teacher']:<10}")

    else: 
        print("Incorrect id or password")


#  ----------------Main Menu --> School Management System ---------------------

print("===========================")
print("Sschool Management System")
print("===========================")

while True:
    print("\n1- Admin")
    print("2- Teacher")
    print("3- Student")
    print("4- Exit")

    logIn = input("\nChoose an option from the above: ").strip()
    
    # Admin LogIn:
    if logIn == "1":
        admin_login(admin_data)

    # Teacher LogIn
    elif logIn == "2": 
        teacher_logIn(teachers_data)
    
    # Student LogIn
    elif logIn == "3": 
        student_logIN(students_data)
    
    # Exiting Main Menu:
    elif logIn == "4": 
        # Saving all the data in json file:
        save_data()
        print("Exiting main block...")
        break 

    else: 
        print("Invalid. Choose from the options available")

print("Program ended")

