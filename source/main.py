import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

import re

import mysql.connector
from datetime import datetime

# this is for copy file
import shutil

# window size define
WIDTH = 800
HEIGHT = 600


class PBU_Hostel_Outgoing:
    # make all initial work for the system
    def __init__(self):
        # make database
        self.database = mysql.connector.connect(
            host='localhost', user='root', password='')
        self.my_cursor = self.database.cursor()

        # create database
        # this will work if database isn't created.
        self.my_cursor.execute(
            "CREATE DATABASE IF NOT EXISTS hostel_outgoing_db")

        self.database = mysql.connector.connect(
            host='localhost', user='root', password='', database='hostel_outgoing_db')
        self.my_cursor = self.database.cursor()

        # creating user table
        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS student (id int(11) NOT NULL AUTO_INCREMENT, name varchar(40), user_name varchar(40), password varchar(40), number_matric varchar(11), gender varchar(10), ic_number varchar(255), hostel_room varchar(40), dob varchar(40), email varchar(40), phone varchar(20), img varchar(255), PRIMARY KEY (id))")
        
        # creating user table
        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS outgoing (id int(11) NOT NULL AUTO_INCREMENT, date_out varchar(40), time_out varchar(40), date_in varchar(40), time_in varchar(40), location varchar(40), user_name varchar(40), PRIMARY KEY (id))")

    # this take user details and save to the database
    def insert_user(self, name, user_name, password, number_matric, gender, ic_number, hostel_room, dob, email, phone, img):

        # add data in table name user
        sql_command = "INSERT INTO student (name, user_name, password, number_matric, gender, ic_number, hostel_room, dob, email, phone, img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            if gender == 1:
                gender = 'male'
            else:
                gender = 'female'
            user = (name, user_name, password, number_matric, gender, ic_number, hostel_room, dob, email, phone, img)
            # print(user)
            self.my_cursor.execute(sql_command, user)  # insert into database
            self.database.commit()  # save to the table
            messagebox.showinfo("Success", "Signup successfully")
            return True
        except:
            messagebox.showerror("Error", "Cannot Signup")
            return False
    
    def insert_outgoing(self, date_out, time_out, date_in, time_in, location, user_name):
         # add data in table name user
        sql_command = "INSERT INTO outgoing (date_out, time_out, date_in, time_in, location, user_name) VALUES (%s, %s, %s, %s, %s, %s)"

        try:

            user = (date_out, time_out, date_in, time_in, location, user_name)
            # print(user)
            self.my_cursor.execute(sql_command, user)  # insert into database
            self.database.commit()  # save to the table
            messagebox.showinfo("Success", "Insert successfully")
            return True
        except:
            messagebox.showerror("Error", "Cannot Insert")
            return False

    # for view user information
    def view_user_outgoing(self, user_name, date_in):
        # take id and show one user
        sql_command = "SELECT * FROM outgoing WHERE user_name = %s and date_in =%s"
        self.my_cursor.execute(sql_command, (user_name, date_in ))
        user = self.my_cursor.fetchall()
        if user:
            return user, True
        else:
            return user, False

     # for view user information
    def view_user(self, number_matric):
        # take id and show one user
        sql_command = "SELECT * FROM student WHERE number_matric = %s"
        self.my_cursor.execute(sql_command, (number_matric, ))
        user = self.my_cursor.fetchall()
        if user:
            return user, True
        else:
            return user, False
    
    def login_user(self, user_name, password):
        # take id and show one user
        sql_command = "SELECT * FROM student WHERE user_name = %s AND password = %s"
        self.my_cursor.execute(sql_command, (user_name, password,))
        user = self.my_cursor.fetchall()
        if user:
            return user, True
        else:
            return user, False
    
    def is_exits_user(self, user_name):
        sql_command = "SELECT * FROM student WHERE user_name = %s"
        self.my_cursor.execute(sql_command, (user_name,))
        user = self.my_cursor.fetchall()
        if user:
            return True
        else:
            return False

    # edit user info
    def edit_user(self, name, password, number_matric, gender, ic_number, hostel_room, dob, email, phone, img):
        if gender == 1:
            gender = 'male'
        else:
            gender = 'female'
            
        sql_command = "UPDATE student set name=%s, password=%s, gender=%s, ic_number=%s, hostel_room=%s, dob=%s, email=%s, phone=%s, img=%s WHERE number_matric=%s"
        update_val = (name,password, gender, ic_number, hostel_room,
                      dob, email, phone, img, number_matric)
        try:
            self.my_cursor.execute(sql_command, update_val)
            self.database.commit()
            messagebox.showinfo("Success", "Update data successfully")
            return True
        except:
            messagebox.showerror("Error", "Cannot Update data")
            return False

    # edit user info outgoing
    def edit_user_outgoingD(self, date_out, time_out, date_in, time_in, location, user_name):
        
        sql_command = "UPDATE outgoing set date_out=%s, time_out=%s, date_in=%s, time_in=%s, location=%s WHERE user_name=%s"
        update_val = (self, date_out, time_out, date_in, time_in, location, user_name)
        try:
            self.my_cursor.execute(sql_command, update_val)
            self.database.commit()
            messagebox.showinfo("Success", "Update data successfully")
            return True
        except:
            messagebox.showerror("Error", "Cannot Update data")
            return False


global db  # this is global for the database
db = PBU_Hostel_Outgoing()


# this class is pages view

# login user
class Login_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        border = tk.LabelFrame(
            self, text='Login', bg='ivory', bd=10, font=("Arial Bold", 20))
        border.pack(fill="both", expand="yes", padx=110, pady=200)

        user_label = tk.Label(border, text="Username", font=(
            "Arial Bold", 15), bg='ivory')
        user_label.place(x=50, y=20)
        username_textField = tk.Entry(border, width=30, bd=5)
        username_textField.place(x=180, y=20)

        password_label = tk.Label(border, text="Password", font=(
            "Arial Bold", 15), bg='ivory')
        password_label.place(x=50, y=80)
        password_textField = tk.Entry(border, width=30, show='*', bd=5)
        password_textField.place(x=180, y=80)

        def verify_user():
            username = username_textField.get()
            password = password_textField.get()
            if username == '':
                messagebox.showwarning("Error", "Please provide username!!")
            elif password == '':
                messagebox.showwarning("Error", "Please provide password!!")
            else:
                user, flag =  db.login_user(username, password)
                if flag:
                    # save user data into text file
                    file= open("user_log.txt","w+")
                    user_data_list = list(user[0])
                    for x in user_data_list:
                        file.write(str(x)+"\n")
                    file.close()
                    
                    # show home page
                    messagebox.showwarning("Success", "Login Successfully!")
                    controller.show_frame(User_home)
                else:
                    messagebox.showinfo(
                        "Error", "Wrong username or password!!")

        login_button = tk.Button(self, text="Login", font=(
            "Arial", 15), fg="#ffffff", background="#0bb345", command=verify_user)
        login_button.place(x=600, y=340)

        back_button = tk.Button(self, text="Back", font=(
            "Arial", 15), fg="#ffffff", background="#d60606", command=lambda: controller.show_frame(Home_page))
        back_button.place(x=160, y=420)

        signup_button = tk.Button(self, text="Don't have account? Singup!", font=(
            "Arial", 15), fg="#ffffff", background="#037ffc", command=lambda: controller.show_frame(Signup_Page))
        signup_button.place(x=370, y=420)

class Signup_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        canvas.create_rectangle(80, 2, 620, 550,
                                outline="#fb0", fill="ivory")
        canvas.place(x=20, y=20)

        name_label = tk.Label(self, text="Singup ", font=(
            "Arial Bold", 25), bg='ivory')
        name_label.place(x=180, y=24)

        x_pos = 120
        y_pos = 80

        # # image add here
        load = Image.open("img\profile.png")
        photo = ImageTk.PhotoImage(load.resize((120, 140), Image.ANTIALIAS,))
        label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
        label.image = photo
        label.place(x=490, y=80)

        self.image_path = ""
        def choose_photo():
            use_name = user_name_textField.get()
            if use_name == '':
                messagebox.showwarning("Error", "To upload image provide username!!")
            elif db.is_exits_user(use_name):
                messagebox.showwarning("Error", "Username already exits!!/user differnt one!")
            else:
                filepath = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
                savepath = "student_img/"+use_name + ".jpg"
                self.image_path = savepath
                shutil.copy(filepath, savepath)

                # load the upload image
                load = Image.open(savepath)
                photo = ImageTk.PhotoImage(load.resize((120, 140), Image.ANTIALIAS,))
                label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
                label.image = photo
                label.place(x=490, y=80)


        choose_button = tk.Button(self, text="upload photo", font=(
            "Arial", 15), fg="#ffffff", background="#0bb345", command=choose_photo)
        choose_button.place(x=486, y=240)

        # name
        name_label = tk.Label(self, text="Full Name: ", font=(
            "Arial Bold", 15), bg='ivory')
        name_label.place(x=x_pos, y=y_pos)
        name_textField = tk.Entry(self, width=30, bd=5)
        name_textField.place(x=x_pos+150, y=y_pos)

        # user_name
        user_name_label = tk.Label(self, text="Username: ", font=(
            "Arial Bold", 15), bg='ivory')
        user_name_label.place(x=x_pos, y=y_pos+40)
        user_name_textField = tk.Entry(self, width=30, bd=5)
        user_name_textField.place(x=x_pos+150, y=y_pos+40)

        # password
        password_label = tk.Label(self, text="Password", font=(
            "Arial Bold", 15), bg='ivory')
        password_label.place(x=x_pos, y=y_pos+80)
        password_textField = tk.Entry(self, width=30, show='*', bd=5)
        password_textField.place(x=x_pos+150, y=y_pos+80)

        # confirm_password
        confirm_password_label = tk.Label(self, text="Confirm Pass.", font=(
            "Arial Bold", 15), bg='ivory')
        confirm_password_label.place(x=x_pos, y=y_pos+120)
        confirm_password_textField = tk.Entry(self, width=30, show='*', bd=5)
        confirm_password_textField.place(x=x_pos+150, y=y_pos+120)

        # number_matric
        number_matric_label = tk.Label(self, text="Marix Num: ", font=(
            "Arial Bold", 15), bg='ivory')
        number_matric_label.place(x=x_pos, y=y_pos+160)
        number_matric_textField = tk.Entry(self, width=30, bd=5)
        number_matric_textField.place(x=x_pos+150, y=y_pos+160)

        # gender
        gender_label = tk.Label(self, text="Gender: ", font=(
            "Arial Bold", 15), bg='ivory')
        gender_label.place(x=x_pos, y=y_pos+200)

        gender_var = IntVar()
        gender_var.set(1)

        r1 = Radiobutton(self, text="Male", variable=gender_var,
                         value=1, font=("Arial", 13), bg='ivory')
        r2 = Radiobutton(self, text="Female", variable=gender_var,
                         value=2, font=("Arial", 13), bg='ivory')

        r1.place(x=x_pos+150, y=y_pos+200)
        r2.place(x=x_pos+230, y=y_pos+200)

        # icnumber
        icnumber_label = tk.Label(self, text="IC Number: ", font=(
            "Arial Bold", 15), bg='ivory')
        icnumber_label.place(x=x_pos, y=y_pos+240)
        icnumber_textField = tk.Entry(self, width=30, bd=5)
        icnumber_textField.place(x=x_pos+150, y=y_pos+240)

        # room_no
        room_no_label = tk.Label(self, text="Room No: ", font=(
            "Arial Bold", 15), bg='ivory')
        room_no_label.place(x=x_pos, y=y_pos+280)
        room_no_textField = tk.Entry(self, width=30, bd=5)
        room_no_textField.place(x=x_pos+150, y=y_pos+280)

        # dob
        dob_label = tk.Label(self, text="Birth Date: ", font=(
            "Arial Bold", 15), bg='ivory')
        dob_label.place(x=x_pos, y=y_pos+320)
        dob_textField = tk.Entry(self, width=30, bd=5)
        dob_textField.place(x=x_pos+150, y=y_pos+320)

        # email
        email_label = tk.Label(self, text="Email: ", font=(
            "Arial Bold", 15), bg='ivory')
        email_label.place(x=x_pos, y=y_pos+360)
        email_textField = tk.Entry(self, width=30, bd=5)
        email_textField.place(x=x_pos+150, y=y_pos+360)

        # phone
        phone_label = tk.Label(self, text="Phone: ", font=(
            "Arial Bold", 15), bg='ivory')
        phone_label.place(x=x_pos, y=y_pos+400)
        phone_textField = tk.Entry(self, width=30, bd=5)
        phone_textField.place(x=x_pos+150, y=y_pos+400)

        def insert_user():
            # get all the field info
            name = name_textField.get()
            use_name = user_name_textField.get()
            password = password_textField.get()
            confirm_password = confirm_password_textField.get()
            number_matric = number_matric_textField.get()
            gender = gender_var.get()
            icnumber = icnumber_textField.get()
            room_no = room_no_textField.get()
            dob = dob_textField.get()
            email = email_textField.get()
            phone = phone_textField.get()

            # for email validation
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

            # checking all the data is provided or not
            if name == '':
                messagebox.showwarning("Error", "Please provide name!!")
            elif use_name == '':
                messagebox.showwarning("Error", "Please provide username!!")
            elif password == '':
                messagebox.showwarning("Error", "Please provide password!!")
            elif confirm_password == '':
                messagebox.showwarning("Error", "Confirm your password!!")
            elif password != confirm_password:
                messagebox.showwarning("Warnning", "Password doesn't match!!\nConfirm your password?")
            elif number_matric == '':
                messagebox.showwarning("Error", "Please provide Matrix number!!")
            elif gender == '':
                messagebox.showwarning("Error", "Please select gender!!")
            elif icnumber == '':
                messagebox.showwarning("Error", "Please provide IC Number!!")
            elif room_no == '':
                messagebox.showwarning("Error", "Please provide room!!")
            elif dob == '':
                messagebox.showwarning(
                    "Error", "Please provide Date of Birth!!")
            elif email == '':
                messagebox.showwarning(
                    "Error", "Please provide Email!!")
            elif not re.fullmatch(regex, email):
                messagebox.showwarning("Warnning", "Provide a valid email.!!!")
            elif phone == '':
                messagebox.showwarning("Error", "Please provide Phone number!!")
            elif self.image_path == '':
                messagebox.showwarning("Error", "Please provide your image!!")

            else:
                # print(dt_first_dose, dt_second_dose)
                # print(datetime.strptime(dt_first_dose, "%d/%m/%y"))
                if db.is_exits_user(use_name):
                    messagebox.showwarning("Error", "Username already exits!!/user differnt one!")
                else:
                    flag = db.insert_user(name, use_name, password, number_matric, gender, icnumber, room_no, dob, email, phone, self.image_path)
                    if flag:
                        controller.show_frame(Login_Page)

        insert_button = tk.Button(self, text="Insert", font=(
            "Arial", 15), fg="#ffffff", background="#0bb345", command=insert_user)
        insert_button.place(x=x_pos+300, y=y_pos+440)

        back_button = tk.Button(self, text="Login", font=(
            "Arial", 15), fg="#ffffff", background="#d60606", command=lambda: controller.show_frame(Login_Page))
        back_button.place(x=x_pos+40, y=y_pos+440)


class Home_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(self, width=WIDTH, height=HEIGHT)

        x_pos = 150
        y_pos = 20

        label = Label(self, text="Welcome to PBU Hostel Outing System",
                    font=("Helvetica", 18), pady=10)
        label.place(x=x_pos+40, y=y_pos)
        # # image add here
        load = Image.open("img\hostel.png")
        photo = ImageTk.PhotoImage(load.resize((250, 250), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=x_pos+120, y=y_pos+80)


        x_pos = 230
        y_pos = 40
        login = tk.Button(self, text="Login", padx=15, pady=10, font=(
            "Arial", 13), fg="#ffffff", background="#9403fc", command=lambda: controller.show_frame(Login_Page))
        login.place(x=x_pos+40, y=y_pos+340)

        signup = tk.Button(self, text="Signup", padx=10, pady=10, font=(
            "Arial", 13), fg="#ffffff", background="#037ffc", command=lambda: controller.show_frame(Signup_Page))
        signup.place(x=x_pos+200, y=y_pos+340)


class User_home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = Canvas(self, width=WIDTH, height=HEIGHT)

        x_pos = 150
        y_pos = 20
        
        def show_user():
            user = []
            # get user data from text file
            file= open("user_log.txt","r")
            user_data_list = file.readlines()
            for x in user_data_list:
                user.append(x)
            file.close()
            

            name = user[1][:-1]
            user_name = user[2][:-1]
            gender = user[5][:-1]
            ic_number = user[6][:-1]
            room_no = user[7][:-1]
            dob = user[8][:-1]
            email = user[9][:-1]
            phone = user[10][:-1]
            matric_number = user[4][:-1]
            image_path = user[11][:-1]



            canvas = Canvas(self, width=WIDTH, height=HEIGHT)
            canvas.create_rectangle(80, 2, 700, 450,
                                    outline="#fb0", fill="ivory")
            canvas.place(x=10, y=80)

            canvas.create_line(120, 55, 665, 55)

            label = tk.Label(self, text="User Details", font=(
                "Arial Bold", 15), bg='ivory')
            label.place(x=350, y=100)

            x_pos = 180
            y_pos = 165
            h_pos = 30

            # profile image
            load = Image.open(image_path)
            photo = ImageTk.PhotoImage(load.resize((120, 140), Image.ANTIALIAS,))
            label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
            label.image = photo
            label.place(x=490, y=y_pos)
            # name
            name_label = tk.Label(self, text="Name:\t\t"+name, font=(
                "Arial", 13), bg='ivory')
            name_label.place(x=x_pos, y=y_pos)

            # username
            username_label = tk.Label(self, text="Username:\t"+str(user_name), font=(
                "Arial ", 13), bg='ivory')
            username_label.place(x=x_pos, y=y_pos+h_pos)

            # gender
            gender_label = tk.Label(self, text="Gender:\t\t"+gender, font=(
                "Arial", 13), bg='ivory')
            gender_label.place(x=x_pos, y=y_pos+(h_pos*2))

            # ic
            ic_label = tk.Label(self, text="IC Number:\t"+ic_number, font=(
                "Arial", 13), bg='ivory')
            ic_label.place(x=x_pos, y=y_pos+(h_pos*3))

            # room_no
            room_no_label = tk.Label(self, text="Room No:\t"+room_no, font=(
                "Arial", 13), bg='ivory')
            room_no_label.place(x=x_pos, y=y_pos+(h_pos*4))

            # dob
            dob_label = tk.Label(self, text="Birth Date:\t"+dob, font=(
                "Arial", 13), bg='ivory')
            dob_label.place(x=x_pos, y=y_pos+(h_pos*5))

            # email
            email_label = tk.Label(self, text="Email:\t\t"+email, font=(
                "Arial", 13), bg='ivory')
            email_label.place(x=x_pos, y=y_pos+(h_pos*6))

            # phone
            phone = tk.Label(self, text="Phone:\t\t"+phone, font=(
                "Arial", 13), bg='ivory')
            phone.place(x=x_pos, y=y_pos+(h_pos*7))

            matric_number_label  = tk.Label(self, text="Matric Num:\t"+matric_number, font=(
                "Arial", 13), bg='ivory')
            matric_number_label.place(x=x_pos, y=y_pos+(h_pos*8))

        def logout_user():
            # delete file
            import os
            if os.path.exists("user_log.txt"):
                os.remove("user_log.txt")
            controller.show_frame(Exit_Page)


        def update_user():
            user = []
            # get user data from text file
            file= open("user_log.txt","r")
            user_data_list = file.readlines()
            for x in user_data_list:
                user.append(x)
            file.close()
            

            name = user[1][:-1]
            self.user_name = user[2][:-1]
            password = user[3][:-1]
            gender = user[5][:-1]
            ic_number = user[6][:-1]
            room_no = user[7][:-1]
            dob = user[8][:-1]
            email = user[9][:-1]
            phone = user[10][:-1]
            matric_number = user[4][:-1]
            self.image = user[11][:-1]

            canvas = Canvas(self, width=WIDTH, height=HEIGHT)
            canvas.create_rectangle(80, 2, 700, 450,
                                    outline="#fb0", fill="ivory")
            canvas.place(x=10, y=80)

            canvas.create_line(120, 55, 665, 55)



            # # image add here
            load = Image.open(self.image)
            photo = ImageTk.PhotoImage(load.resize((120, 140), Image.ANTIALIAS,))
            label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
            label.image = photo
            label.place(x=540, y=160)

            def choose_photo():
                filepath = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
                if filepath != '':
                    savepath = "student_img/"+self.user_name + ".jpg"
                    self.image = savepath
                    shutil.copy(filepath, savepath)

                    # load the upload image
                    load = Image.open(savepath)
                    photo = ImageTk.PhotoImage(load.resize((120, 140), Image.ANTIALIAS,))
                    label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
                    label.image = photo
                    label.place(x=540, y=160)

            choose_button = tk.Button(self, text="upload photo", font=(
                "Arial", 15), fg="#ffffff", background="#0bb345", command=choose_photo)
            choose_button.place(x=536, y=310)

            name_label = tk.Label(self, text=str("User: "+self.user_name+" , Matric:" + matric_number), font=(
                "Arial Bold", 14), bg='ivory')
            name_label.place(x=180, y=90)

            x_pos = 170
            y_pos = 165
            # name
            name_label = tk.Label(self, text="Name: ", font=(
                "Arial", 15), bg='ivory')
            name_label.place(x=x_pos, y=y_pos)
            name_textField = tk.Entry(self, width=30, bd=5)
            name_textField.place(x=x_pos+150, y=y_pos)
            name_textField.insert(0, name)

            # password
            password_label = tk.Label(self, text="Passwrod: ", font=(
                "Arial", 15), bg='ivory')
            password_label.place(x=x_pos, y=y_pos+40)
            password_textField = tk.Entry(self, width=30, show='*', bd=5)
            password_textField.place(x=x_pos+150, y=y_pos+40)
            password_textField.insert(0, str(password))

            # gender
            gender_label = tk.Label(self, text="Gender: ", font=(
                "Arial", 15), bg='ivory')
            gender_label.place(x=x_pos, y=y_pos+80)
            gender_var = IntVar()
            if gender == "male":
                gender_var.set(1)
            else:
                gender_var.set(2)

            r1 = Radiobutton(self, text="Male", variable=gender_var,
                                value=1, font=("Arial", 13), bg='ivory')
            r2 = Radiobutton(self, text="Female", variable=gender_var,
                                value=2, font=("Arial", 13), bg='ivory')

            r1.place(x=x_pos+140, y=y_pos+85)
            r2.place(x=x_pos+230, y=y_pos+85)

            # ic number
            ic_number_label = tk.Label(self, text="IC Number: ", font=(
                "Arial", 15), bg='ivory')
            ic_number_label.place(x=x_pos, y=y_pos+120)
            ic_number_textField = tk.Entry(self, width=30, bd=5)
            ic_number_textField.place(x=x_pos+150, y=y_pos+120)
            ic_number_textField.insert(0, ic_number)

            # room_no
            room_no_label = tk.Label(self, text="Room No: ", font=(
                "Arial", 15), bg='ivory')
            room_no_label.place(x=x_pos, y=y_pos+160)
            room_no_textField = tk.Entry(
                self, width=30, bd=5)
            room_no_textField.place(x=x_pos+150, y=y_pos+160)
            room_no_textField.insert(0, room_no)

            # dob
            dob_lable = tk.Label(self, text="Brith Date: ", font=(
                "Arial", 15), bg='ivory')
            dob_lable.place(x=x_pos, y=y_pos+200)
            dob_textField = tk.Entry(
                self, width=30, bd=5)
            dob_textField.place(
                x=x_pos+150, y=y_pos+200)
            dob_textField.insert(0, dob)

            # email
            email_label = tk.Label(self, text="Email: ", font=(
                "Arial", 15), bg='ivory')
            email_label.place(x=x_pos, y=y_pos+240)
            email_textField = tk.Entry(
                self, width=30, bd=5)
            email_textField.place(
                x=x_pos+150, y=y_pos+240)
            email_textField.insert(0, email)

             # phone
            phone_label = tk.Label(self, text="Phone: ", font=(
                "Arial", 15), bg='ivory')
            phone_label.place(x=x_pos, y=y_pos+280)
            phone_textField = tk.Entry(
                self, width=30, bd=5)
            phone_textField.place(
                x=x_pos+150, y=y_pos+280)
            phone_textField.insert(0, phone)

            def insert_user():
                response = messagebox.askyesno(
                    "Update", "Once you update you loose prevoius data.\nDo you want to update this?")

                if response:
                    name = name_textField.get()
                    password = password_textField.get()
                    gender = gender_var.get()
                    ic_num = ic_number_textField.get()
                    room_no = room_no_textField.get()
                    dob = dob_textField.get()
                    email = email_textField.get()
                    phone = phone_textField.get()

                    # for email validation
                    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

                    if name == '':
                        messagebox.showwarning(
                            "Error", "Please provide name!!")
                    elif password == '':
                        messagebox.showwarning(
                            "Error", "Please provide password!!")
                    elif gender == '':
                        messagebox.showwarning(
                            "Error", "Please select gender!!")
                    elif ic_num == '':
                        messagebox.showwarning(
                            "Error", "Please provide IC Number!!")
                    elif room_no == '':
                        messagebox.showwarning(
                            "Error", "Please provide room no!!")
                    elif dob == '':
                        messagebox.showwarning(
                            "Error", "Please provide date of birth!!")
                    elif email == '':
                        messagebox.showwarning(
                            "Error", "Please provide email!!")
                    elif not re.fullmatch(regex, email):
                        messagebox.showwarning("Warnning", "Provide a valid email.!!!")
                    elif phone == '':
                        messagebox.showwarning(
                            "Error", "Please provide phone!!")

                    else:
                        # print(dt_first_dose, dt_second_dose)
                        # print(datetime.strptime(dt_first_dose, "%d/%m/%y"))

                        flag = db.edit_user(name, password, matric_number, gender, ic_num, room_no, dob, email, phone, self.image)
                        if flag:
                            controller.show_frame(Edit_data_Page)

            insert_button = tk.Button(self, text="Update", font=(
                "Arial", 15), fg="#ffffff", background="#0bb345", command=insert_user)
            insert_button.place(x=x_pos+300, y=y_pos+320)



        view_user = tk.Button(self, text="View Data", font=(
            "Arial", 13), fg="#ffffff", background="#9403fc", command=show_user)
        view_user.place(x=x_pos+40, y=y_pos)

        edit_user = tk.Button(self, text="Edit Data", font=(
            "Arial", 13), fg="#ffffff", background="#037ffc", command=update_user)
        edit_user.place(x=x_pos+200, y=y_pos)

        logout_button = tk.Button(self, text="Logout", font=(
            "Arial", 13), fg="#ffffff", background="#d60606", command=logout_user)
        logout_button.place(x=x_pos+400, y=y_pos)


class Edit_data_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Update data Successfully",
                      font=("Helvetica", 18), pady=10)
        label.pack()
        label = Label(self, text="Thanks For Using",
                      font=("Helvetica", 18), pady=10)
        label.pack()

        # line
        canvas = Canvas(self, width=600,  height=30)
        canvas.pack()
        canvas.create_line(120, 10, 480, 10)
        canvas.create_line(80, 15, 520, 15)
        canvas.create_line(10, 20, 590, 20)

        # image for thanks giving
         # # image add here
        load = Image.open("img\hostel.png")
        photo = ImageTk.PhotoImage(load.resize((250, 250), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.pack()
       


class Exit_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         # label
        label = Label(self, text="Thanks For Using",
                      font=("Helvetica", 18), pady=10)
        label.pack()

        # line
        canvas = Canvas(self, width=600,  height=30)
        canvas.pack()
        canvas.create_line(120, 10, 480, 10)
        canvas.create_line(80, 15, 520, 15)
        canvas.create_line(10, 20, 590, 20)

        # image for thanks giving
         # # image add here
        load = Image.open("img\hostel.png")
        photo = ImageTk.PhotoImage(load.resize((250, 250), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.pack()



# main application page
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.user_data = []

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=HEIGHT)
        window.grid_columnconfigure(0, minsize=WIDTH)

        self.frames = {}
        pages = (Login_Page, Signup_Page, Home_page, User_home, Exit_Page, Edit_data_Page)

        for F in pages:
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home_page)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("PBU Hostel Outing System")  # add title
        self.iconbitmap('img\hostel.ico')  # add icon


app = Application()
app.maxsize(WIDTH, HEIGHT)
app.mainloop()
