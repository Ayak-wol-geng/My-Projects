import tkinter as tk
from tkinter.ttk import Combobox, Treeview
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import re
import random
import sqlite3
import os
import win32api
import smtplib
from tkinter.scrolledtext import ScrolledText
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = tk.Tk()
root.geometry('500x600')
root.title('Greenhill Academy Student Management System')

login_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\user (2).png")
login_admin_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\user-gear.png")
login_addstudent_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\add-user (1).png")
locked_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\locked.png")
unlocked_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\unlock (1).png")
add_student_pic_icon=tk.PhotoImage(file=r"C:\Users\hp\Downloads\userprofile.png")

def init_database():
    if os.path.exists('students_accounts.db'):
    
        connection=sqlite3.connect('students_accounts.db')

        cursor=connection.cursor()
        cursor.execute("""SELECT * FROM data
        """)

        connection.commit()
        print(cursor.fetchall())
        connection.close()

        
    else:
        connection=sqlite3.connect('students_accounts.db')

        cursor=connection.cursor()
        cursor.execute("""
        CREATE TABLE data (id_number text, password text, name text, age text, gender text, phone_number text, class text, email text, image blob)""")

        connection.commit()
        connection.close()

def check_id_already_exists(id_number):
    connection=sqlite3.connect('students_accounts.db')

    cursor=connection.cursor()
    cursor.execute(f""" 
    SELECT id_number FROM data WHERE id_number == '{id_number}'

""")
 
    connection.commit()
    response=cursor.fetchall()
    connection.close()
    return response

def check_valid_password(id_number, password):
    connection=sqlite3.connect('students_accounts.db')

    cursor=connection.cursor()
    cursor.execute(f""" 
    SELECT id_number, password FROM data WHERE id_number == '{id_number}' AND password =='{password}'

""")
 
    connection.commit()
    response=cursor.fetchall()
    connection.close()
    return response

def add_data(id_number, password, name, age, gender, phone_number, student_class, email, pic_data):
    connection=sqlite3.connect('students_accounts.db')

    cursor=connection.cursor()
    cursor.execute(""" INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_number, password, name, age, gender, phone_number, student_class, email, pic_data))
 
    connection.commit()
    connection.close()


def confirmation_box(message):
    answer=tk.BooleanVar()
    answer.set(False)
    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()
    confirmation_box_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    
    message_label=tk.Label(confirmation_box_fm, text=message, font=('bold',15))
    message_label.pack(pady=20)

    cancel_btn=tk.Button(confirmation_box_fm, text='Cancel', font=('bold',15), bd=0, bg='#273b7a', fg='white', command=lambda:action(False))
    cancel_btn.place(x=50, y=160)

    yes_btn=tk.Button(confirmation_box_fm, text='YES', font=('bold',15), bd=0, bg='#273b7a', fg='white', command=lambda:action(True))
    yes_btn.place(x=190, y=160, width=80)

    confirmation_box_fm.place(x=100, y=120, width=320, height=220)
    
    root.wait_window(confirmation_box_fm)
    return answer.get()

def message_box(message):
    message_box_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)

    close_btn=tk.Button(message_box_fm, text='X', bd=0, font=('bold',13),fg='#273b7a', command=lambda: message_box_fm.destroy())
    close_btn.place(x=290, y=5)

    message_label=tk.Label(message_box_fm, text=message, font=('bold',13))
    message_label.pack(pady=30)

    message_box_fm.place(x=100, y=120, width=320, height=200)
    
def draw_student_card(student_pic_path, student_data):
    Labels="""
ID Number:
Name:
Gender:
Age:
Class:
Contact:
Email:

"""

    student_card=Image.open(r"C:\Users\hp\Downloads\Images\Images\student_card_frame.png")
    pic=Image.open(student_pic_path).resize((100,100))

    student_card.paste(pic, (15,25))
    draw=ImageDraw.Draw(student_card)

    heading_font=ImageFont.truetype('bahnschrift', 18)
    label_font=ImageFont.truetype('arial', 15)
    data_font=ImageFont.truetype('bahnschrift', 13)

    draw.text(xy=(150, 60), text='GreenHill\nAcademy', fill=(0,0,0), font=heading_font)
    draw.multiline_text(xy=(15, 120), text=Labels, fill=(0,0,0), font=label_font, spacing=6)

    draw.multiline_text(xy=(95, 120), text=student_data, fill=(0,0,0), font=data_font, spacing=10)

    return student_card

def student_card_page(student_card_obj):

    def save_student_card():
        path=askdirectory()
        if path:
            print(path)
            student_card_obj.save(f'{path}/student_card.png')

    def print_student_card():
        path=askdirectory()
        if path:
            print(path)
            student_card_obj.save(f'{path}/student_card.png')
            win32api.ShellExecute(0, 'print', f'{path}/student_card.png', None, '.',0)

    def close_page():
        student_card_page_fm.destroy()
        root.update()
        student_login()

    student_card_img=ImageTk.PhotoImage(student_card_obj)
    student_card_page_fm=tk.Frame(root,  highlightbackground='#273b7a', highlightthickness=3)
    heading_lb=tk.Label(student_card_page_fm, text='STUDENT CARD', bg='#273b7a', fg='white', font=('bold',18))
    heading_lb.place(x=0, y=0, width=400)

    close_btn=tk.Button(student_card_page_fm, text='X', bg='#273b7a', fg='white', font=('bold', 13), bd=0, command=close_page)
    close_btn.place(x=370, y=0)

    student_card_lb=tk.Label(student_card_page_fm, image=student_card_img)
    student_card_lb.place(x=50, y=50)

    student_card_lb.image=student_card_img

    save_student_card_btn=tk.Button(student_card_page_fm, text='Save Student Card', bg='#273b7a', fg='white', font=('bold',15), bd=1, command=save_student_card)
    save_student_card_btn.place(x=50, y=375)

    print_save_student_card_btn=tk.Button(student_card_page_fm, text='🖨️', bg='#273b7a', fg='white', font=('bold',15), bd=1, command=print_student_card)
    print_save_student_card_btn.place(x=270, y=370)


    student_card_page_fm.place(x=50, y=30, width=400, height=450)

def welcome_page():
    def forward_to_student_page():
        welcome_page_fm.destroy()
        root.update()
        student_login()

    def forward_to_admin_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()


    welcome_page_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    heading_label= tk.Label(welcome_page_fm,text='Welcome To Greenhill Academy\n Management System', bg='#273b7a', fg='white', font=('Bold',18))
    heading_label.place(x=0, y=0, width=400)

    student_login_button=tk.Button(welcome_page_fm, text='Login', bg='#273b7a', fg='white', font=('Aerial',15), bd=0, command=forward_to_student_page)
    student_login_button.place(x=120, y=125, width=200)

    student_login_img=tk.Button(welcome_page_fm, image=login_icon, bd=0, command=forward_to_student_page)
    student_login_img.place(x=90, y=110)

    admin_login_button=tk.Button(welcome_page_fm, text='Admin Login', bg='#273b7a', fg='white', font=('Aerial',15), bd=0, command=forward_to_admin_page)
    admin_login_button.place(x=120, y=225, width=200)

    admin_login_img=tk.Button(welcome_page_fm, image=login_admin_icon, bd=0, command=forward_to_admin_page)
    admin_login_img.place(x=90, y=200)

    add_login_button=tk.Button(welcome_page_fm, text='Create Account', bg='#273b7a', fg='white', font=('Aerial',15), bd=0, command=forward_to_add_account_page)
    add_login_button.place(x=120, y=325, width=200)

    add_login_img=tk.Button(welcome_page_fm, image=login_addstudent_icon, bd=0, command=forward_to_add_account_page)
    add_login_img.place(x=90, y=300)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)



def sendmail_to_student(email, message, subject):
    my_email_address='ayakwol2@gmail.com'
    my_email_password='Godlovesme@22'
    smtp_server='smtp.gmail.com'
    smtp_port=587
    username=my_email_address
    password=my_email_password
    msg=MIMEMultipart()

    msg['Subject']=subject
    msg['From']=username
    msg['To']=email
    msg.attach(MIMEText(_text=message, _subtype='html'))
    smtp_connection=smtplib.SMTP(host=smtp_server, port=smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)
    smtp_connection.sendmail(from_addr=username, to_addrs=email, msg=msg.as_string())
    smtp_connection.quit()

def forget_password_page():

    def recover_password():
        if check_id_already_exists(id_number=student_id_entry.get()):
            print('correct ID')

            connection=sqlite3.connect('students_accounts.db')
            cursor=connection.cursor()

            cursor.execute(f""" SELECT password FROM data WHERE id_number = '{student_id_entry.get()}' """)

            connection.commit()
            recovered_password=cursor.fetchall()[0][0]
            print('recovered password:', recovered_password)

            cursor.execute(f"""
            SELECT email FROM data WHERE id_number == '{student_id_entry.get()}'
            """)

            connection.commit()
            student_email=cursor.fetchall()[0][0]
            print('email address:', student_email)
            
            connection.close()
            confirmation=confirmation_box(message=f"""We will send\nYour password\nVia your email address:\n{student_email}\nDo you want to continue?""")
            print(confirmation)

        else:
            print('incorrect ID')
            message_box(message='Invalid ID number')

    forget_password_page_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    heading_lb=tk.Label(forget_password_page_fm, text='⚠️ Forgetting Password', font=('bold',15), bg='#273b7a', fg='white')
    heading_lb.place(x=0, y=0, width=350)
    close_btn=tk.Button(forget_password_page_fm, text='X', font=('bold',13), bg='#273b7a', fg='white',bd=0, command=lambda: forget_password_page_fm.destroy())
    close_btn.place(x=320, y=0)

    student_id_lb=tk.Label(forget_password_page_fm, text='Enter student ID Number', font=('bold',13))
    student_id_lb.place(x=70, y=40)

    student_id_entry=tk.Entry(forget_password_page_fm, font=('bold',15), justify=tk.CENTER)
    student_id_entry.place(x=70, y=70, width=180)

    infor_lb=tk.Label(forget_password_page_fm, text='***You can receive \nyour old password \nvia email***', justify=tk.LEFT)
    infor_lb.place(x=75, y=110)
    next_btn=tk.Button(forget_password_page_fm, text='NEXT', font=('bold',13), bg='#273b7a', fg='white', command=recover_password)
    next_btn.place(x=130, y=200, width=80)

    forget_password_page_fm.place(x=75, y=120, width=350, height=250)

def fetch_student_data(query, params=()):
    connection=sqlite3.connect('students_accounts.db')
    cursor=connection.cursor()

    cursor.execute(query, params)

    connection.commit()
    response=cursor.fetchall()
    connection.close()
    return response


def student_dashboard(student_id):

    get_student_details=fetch_student_data("""
    SELECT name, age, gender, "class", phone_number, email FROM data WHERE id_number =?
""", (student_id,))
    
    get_student_pic=fetch_student_data("""
    SELECT image FROM data WHERE id_number =?
""", (student_id,))
    
    student_pic=BytesIO(get_student_pic [0][0])
    
    def logout():
        confirm=confirmation_box(message='Do you want to\nLogout your account?')
        if confirm:
            dashboard_fm.destroy()
            welcome_page()
            root.update()

    def switch(indicator, page):
        home_btn_indicator.config(bg='#c3c3c3')
        card_btn_indicator.config(bg='#c3c3c3')
        security_btn_indicator.config(bg='#c3c3c3')
        edit_btn_indicator.config(bg='#c3c3c3')
        delete_btn_indicator.config(bg='#c3c3c3')

        indicator.config(bg='#273b7a')

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()

        page()

    dashboard_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    options_fm=tk.Frame(dashboard_fm, highlightbackground='#273b7a', highlightthickness=2, bg='#c3c3c3')

    home_btn=tk.Button(options_fm, text='Home', font=('bold',13), fg='#273b7a', bg='#c3c3c3', command=lambda:switch(indicator=home_btn_indicator, page=home_page))
    home_btn.place(x=10, y=50)

    home_btn_indicator=tk.Label(options_fm, bg='#273b7a')
    home_btn_indicator.place(x=5, y=48, width=3, height=40)

    student_card_btn=tk.Button(options_fm, text='Card', font=('bold',13), fg='#273b7a', bg='#c3c3c3', command=lambda:switch(indicator=card_btn_indicator, page=card_page))
    student_card_btn.place(x=10, y=100)

    card_btn_indicator=tk.Label(options_fm, bg='#c3c3c3')
    card_btn_indicator.place(x=5, y=98, width=3, height=40)

    security_btn=tk.Button(options_fm, text='Security', font=('bold',13), fg='#273b7a', bg='#c3c3c3', command=lambda:switch(indicator=security_btn_indicator, page=security_page))
    security_btn.place(x=10, y=150)

    security_btn_indicator=tk.Label(options_fm, bg='#c3c3c3')
    security_btn_indicator.place(x=5, y=148, width=3, height=40)

    edit_data_btn=tk.Button(options_fm, text='Edit', font=('bold',13), fg='#273b7a', bg='#c3c3c3', command=lambda:switch(indicator=edit_btn_indicator, page=edit_data_page))
    edit_data_btn.place(x=10, y=200)

    edit_btn_indicator=tk.Label(options_fm, bg='#c3c3c3')
    edit_btn_indicator.place(x=5, y=198, width=3, height=40)

    delete_data_btn=tk.Button(options_fm, text='Delete', font=('bold',13), fg='#273b7a', bg='#c3c3c3', command=lambda:switch(indicator=delete_btn_indicator, page=delete_account_page))
    delete_data_btn.place(x=10, y=250)

    delete_btn_indicator=tk.Label(options_fm, bg='#c3c3c3')
    delete_btn_indicator.place(x=5, y=250, width=3, height=40)

    logout_btn=tk.Button(options_fm, text='Logout', font=('bold',13), fg='#273b7a', bg='#c3c3c3', justify=tk.LEFT, command=logout)
    logout_btn.place(x=10, y=300)

    #logout_btn_indicator=tk.Label(options_fm, bg='#273b7a')
    #logout_btn_indicator.place(x=5, y=248, width=3, height=40)

    options_fm.place(x=0, y=0, width=120, height=575)

    def home_page():

        student_pic_image_obj=Image.open(student_pic)
        size=100
        mask=Image.new(mode='L', size=(size, size))
        
        draw_circle=ImageDraw.Draw(im=mask)
        draw_circle.ellipse(xy=(0, 0, size, size), fill=255, outline=True)

        output=ImageOps.fit(image=student_pic_image_obj, size=mask.size, centering=(1,1))
        output.putalpha(mask)

        student_picture=ImageTk.PhotoImage(output)


        home_page_fm=tk.Frame(pages_fm)

        student_pic_lb=tk.Label(home_page_fm, image=student_picture)
        student_pic_lb.image=student_picture
        
        student_pic_lb.place(x=10, y=10)

        hi_lb=tk.Label(home_page_fm, text=f'Hi {get_student_details[0][0]}', font=('bold',15))
        hi_lb.place(x=130, y=50)

        student_details=f"""
        Student ID: {student_id}\n
        Name: {get_student_details[0][0]}\n
        Age: {get_student_details[0][1]}\n
        Gender: {get_student_details[0][2]}\n
        Class: {get_student_details[0][3]}\n
        Contact: {get_student_details[0][4]}\n
        Email: {get_student_details[0][5]}
        """

        student_details_lb=tk.Label(home_page_fm, text=student_details, font=('bold',13), justify=tk.LEFT)
        student_details_lb.place(x=20, y=130)

        home_page_fm.pack(fill=tk.BOTH, expand=True)


    def card_page():

        student_details=f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""

        student_card_image_obj=draw_student_card(student_pic_path=student_pic, student_data=student_details)
   
        def save_student_card():
            path=askdirectory()
            if path:
                print(path)
                student_card_image_obj.save(f'{path}/student_card.png')

        def print_student_card():
            path=askdirectory()
            if path:
                print(path)
                student_card_image_obj.save(f'{path}/student_card.png')
                win32api.ShellExecute(0, 'print', f'{path}/student_card.png', None, '.',0)

        def close_page():
            card_page_fm.destroy()
            root.update()
            student_login()

        student_card_img=ImageTk.PhotoImage(student_card_image_obj)
        

        card_page_fm=tk.Frame(pages_fm)

        card_lb=tk.Label(card_page_fm, image=student_card_img)
        card_lb.image=student_card_img
        card_lb.place(x=20, y=50)

        save_student_card_btn=tk.Button(card_page_fm, text='Save Student Card', font=('bold', 15), bd=1, fg='white', bg='#273b7a', command=save_student_card)
        save_student_card_btn.place(x=40, y=400)

        print_student_card_btn=tk.Button(card_page_fm, text='🖨️', font=('bold', 15), bd=1, fg='white', bg='#273b7a', command=print_student_card)
        print_student_card_btn.place(x=240, y=400)


        card_page_fm.pack(fill=tk.BOTH, expand=True)


    def security_page():

        def show_hide_password():

            if current_password_entry['show']=='*':
                current_password_entry.config(show='')
                show_hide_btn.config(image=unlocked_icon)

            else:
                current_password_entry.config(show='*')
                show_hide_btn.config(image=locked_icon)

        def set_password():
            if new_password_entry.get()!='':
                confirm=confirmation_box(message='Do you want to change\n Your password')
                if confirm:
                    connection=sqlite3.connect('students_accounts.db')
                    cursor=connection.cursor()
                    cursor.execute(f"UPDATE data SET password='{new_password_entry.get()}' WHERE id_number=?", (student_id,))
                    connection.commit()
                    connection.close()
                    message_box(message='Password changed successfully')

                    current_password_entry.config(state=tk.NORMAL)
                    current_password_entry.delete(0, tk.END)
                    current_password_entry.insert(0, new_password_entry.get())
                    current_password_entry.config(state='readonly')

                    new_password_entry.delete(0, tk.END)

            else:

                message_box(message='Enter new password')

        security_page_fm=tk.Frame(pages_fm)

        current_password_lb=tk.Label(security_page_fm, text='Your current password', font=('bold', 12))
        current_password_lb.place(x=80, y=30)

        current_password_entry=tk.Entry(security_page_fm, font=('bold', 15), justify=tk.CENTER, show='*')
        current_password_entry.place(x=50, y=80)

        student_current_password=fetch_student_data("SELECT password FROM data WHERE id_number=?",(student_id,))
        current_password_entry.insert(tk.END, student_current_password[0][0])
        current_password_entry.config(state='readonly')

        show_hide_btn=tk.Button(security_page_fm, image=locked_icon, bd=0,command=show_hide_password)
        show_hide_btn.place(x=280, y=70)

        change_password_lb=tk.Label(security_page_fm, text='Change Password', font=('bold', 15), bg='red', fg='white')
        change_password_lb.place(x=30, y=210, width=290)

        new_password_lb=tk.Label(security_page_fm, text='Set new Password', font=('bold', 12))
        new_password_lb.place(x=100, y=280)
        new_password_entry=tk.Entry(security_page_fm, font=('bold', 15), justify=tk.CENTER)
        new_password_entry.place(x=60, y=330)

        change_password_btn=tk.Button(security_page_fm, text='SET Password', font=('bold',12), bg='#273b7a', fg='white', command=set_password)
        change_password_btn.place(x=110, y=380)

        security_page_fm.pack(fill=tk.BOTH, expand=True)


    def edit_data_page():
        edit_page_fm=tk.Frame(pages_fm)

        pic_path=tk.StringVar()
        pic_path.set('')

        def open_pic():
            path=askopenfilename()

            if path:
                img=ImageTk.PhotoImage(Image.open(path).resize((100,100)))
                pic_path.set(path)
                add_pc_btn.config(image=img)
                add_pc_btn.image=img

        def remove_highlight_warning(entry):
            if entry['highlightbackground']!='gray':
                if entry.get()!='':
                    entry.config(highlightcolor='#273b7a', highlightbackground='gray')

        def check_invalid_email(email):
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            match=re.match(pattern=pattern, string=email)
            return match


        def check_inputs():
            nonlocal get_student_details, get_student_pic, student_pic

            if student_name_entry.get()=='':
                student_name_entry.config(highlightcolor='red', highlightbackground='red')
                student_name_entry.focus()
                message_box(message='Student full name is required')

            elif student_age_entry.get()=='':
                student_age_entry.config(highlightcolor='red', highlightbackground='red')
                student_age_entry.focus()
                message_box(message='Student age is required')
            
            elif student_contact_entry.get()=='':
                student_contact_entry.config(highlightcolor='red', highlightbackground='red')
                student_contact_entry.focus()
                message_box(message='Student contact number is required')

            elif student_email_entry.get()=='':
                student_email_entry.config(highlightcolor='red', highlightbackground='red')
                student_email_entry.focus()
                message_box(message='Student email address is required')

            elif not check_invalid_email(email=student_email_entry.get().lower()):
                student_email_entry.config(highlightcolor='red', highlightbackground='red')
                student_email_entry.focus()
                message_box(message='Please enter a valid\nEmail address')

            else:
                if pic_path.get()!='':
                    new_student_pic=Image.open(pic_path.get()).resize((100,100))
                    new_student_pic.save('temp_pic.png')
                    with open('temp_pic.png','rb')as readd_new_pic:
                        new_picture_binary=readd_new_pic.read()
                        readd_new_pic.close()
                    
                    connection=sqlite3.connect('students_accounts.db')
                    cursor=connection.cursor()
                    
                    cursor.execute(f"UPDATE data SET image=? WHERE id_number=?",(new_picture_binary, student_id))

                    connection.commit()
                    connection.close()
                    message_box(message='Data successfully updated')

                name=student_name_entry.get()
                age=student_age_entry.get()
                selected_class=select_class_btn.get()
                contact_number=student_contact_entry.get()
                email_address=student_email_entry.get()

                connection=sqlite3.connect('students_accounts.db')
                cursor=connection.cursor()
                    
                cursor.execute(f"""UPDATE data SET name='{name}', age='{age}', class='{selected_class}', phone_number='{contact_number}', email='{email_address}' WHERE id_number='{student_id}' """)
                connection.commit()
                connection.close()

                get_student_details=fetch_student_data("""
                SELECT name, age, gender, "class", phone_number, email FROM data WHERE id_number =?
                """, (student_id,))
    
                get_student_pic=fetch_student_data("""
                SELECT image FROM data WHERE id_number =?
                """, (student_id,))
    
                student_pic=BytesIO(get_student_pic [0][0])

                message_box(message='Data successfully updated')
                
        student_current_pic=ImageTk.PhotoImage(Image.open(student_pic))

        add_pic_section_fm=tk.Frame(edit_page_fm, highlightbackground='#273b7a', highlightthickness=2)
        add_pc_btn= tk.Button(add_pic_section_fm, image=student_current_pic, command=open_pic)

        add_pc_btn.image=student_current_pic
        add_pc_btn.pack()

        add_pic_section_fm.place(x=5, y=5, width=105, height=105)

        student_name_label=tk.Label(edit_page_fm, text='Student Full Name', font=('bold',12))
        student_name_label.place(x=5, y=130)

        student_name_entry=tk.Entry(edit_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
        student_name_entry.place(x=5, y=160, width=180)
        student_name_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_name_entry))

        student_name_entry.insert(tk.END, get_student_details[0][0])

        student_age_lb=tk.Label(edit_page_fm, text='Student Age', font=('bold',12))
        student_age_lb.place(x=5, y=210)

        student_age_entry=tk.Entry(edit_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
        student_age_entry.place(x=5, y=235, width=180)
        student_age_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_age_entry))

        student_age_entry.insert(tk.END, get_student_details[0][1])

        student_contact_lb=tk.Label(edit_page_fm, text='Student Contact Number', font=('bold',12))
        student_contact_lb.place(x=5, y=285)

        student_contact_entry=tk.Entry(edit_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
        student_contact_entry.place(x=5, y=310, width=180)
        student_contact_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_contact_entry))

        student_contact_entry.insert(tk.END, get_student_details[0][4])

        student_class_lb=tk.Label(edit_page_fm, text='Student Class', font=('bold',12))
        student_class_lb.place(x=5, y=360)

        select_class_btn=Combobox(edit_page_fm, font=('bold',15), state='readonly', values=class_list)
        select_class_btn.place(x=5, y=390, width=180, height=30)

        select_class_btn.set(get_student_details[0][3])

        student_email_lb=tk.Label(edit_page_fm, text='Student Email Address', font=('bold',12))
        student_email_lb.place(x=5, y=440)

        student_email_entry=tk.Entry(edit_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
        student_email_entry.place(x=5, y=470, width=180)
        student_email_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_email_entry))

        student_email_entry.insert(tk.END, get_student_details[0][5])

        update_data_btn=tk.Button(edit_page_fm, text='UPDATE', font=('bold',14), fg='white', bg='#273b7a', bd=0, command=check_inputs)
        update_data_btn.place(x=220, y=470, width=80)

        edit_page_fm.pack(fill=tk.BOTH, expand=True)


    def delete_account_page():

        def confirm_delete_account():
            confirm=confirmation_box(message='Do you want to delete\nYour Account?')

            if confirm:
                connection=sqlite3.connect('students_accounts.db')
                cursor=connection.cursor()

                cursor.execute(f""" DELETE FROM data WHERE id_number == '{student_id}'""")

                connection.commit()
                connection.close()

                dashboard_fm.destroy()
                welcome_page()
                root.update
                message_box(message='Account deleted successfully')

        delete_account_page_fm=tk.Frame(pages_fm)
    
        delete_account_lb=tk.Label(delete_account_page_fm, text='⚠️Delete Account', bg='red', fg='white', font=('bold', 15))
        delete_account_lb.place(x=30, y=100, width=290)
        delete_account_btn=tk.Button(delete_account_page_fm, text='DELETE Account', bg='red', fg='white', font=('bold', 13), command=confirm_delete_account)
        delete_account_btn.place(x=110, y=200)


        delete_account_page_fm.pack(fill=tk.BOTH, expand=True)

    pages_fm=tk.Frame(dashboard_fm)
    pages_fm.place(x=122, y=5, width=350, height=550)

    home_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=480, height=580)

def student_login():
    def show_hide_password():

        if password_entry['show']=='*':
            password_entry.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            password_entry.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def forward_to_forget_password():
        forget_password_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground']!='gray':
            if entry.get()!='':
                entry.config(highlightcolor='#273b7a', highlightbackground='gray')
    
    #Check why the ID isnt working even with the correct ID
    def login_account():
        verify_id_number=check_id_already_exists(id_number=id_number_entry.get())

        if verify_id_number:
            print('ID is correct')
            verify_password=check_valid_password(id_number=id_number_entry.get(), password=password_entry.get())

            if verify_password:
                id_number=id_number_entry.get()
                student_login_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()
            else:
                print('Incorrect password')
                password_entry.config(highlightcolor='red', highlightbackground='red')
                message_box(message='Please enter a valid password')

        else:
            print('ID is incorrect')
            id_number_entry.config(highlightcolor='red', highlightbackground='red')
            message_box(message='Please enter a valid student ID')

    student_login_page_fm=tk.Frame(root,  highlightbackground='#273b7a', highlightthickness=3)
    heading_label=tk.Label(student_login_page_fm, text='Student Login Page', bg='#273b7a',fg='white', font=('bold',18))
    heading_label.place(x=0, y=0, width=400)

    back_button=tk.Button(student_login_page_fm, text='←', font=('bold',20), fg='#273b7a', bd=0, command=forward_to_welcome)
    back_button.place(x=5, y=40)

    student_icon_lable=tk.Label(student_login_page_fm, image=login_addstudent_icon)
    student_icon_lable.place(x=150, y=40)

    id_number_label=tk.Label(student_login_page_fm, text='Enter Student ID Number',font=('Bold',15),fg='#273b7a')
    id_number_label.place(x=80, y=140)

    id_number_entry=tk.Entry(student_login_page_fm, font=('bold',15), justify=tk.CENTER,highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2 )
    id_number_entry.place(x=80, y=190)

    id_number_entry.bind('<KeyRelease>', lambda e:remove_highlight_warning(entry=id_number_entry))
    password_label=tk.Label(student_login_page_fm, text='Enter Student Password', font=('bold',15), fg='#273b7a')
    password_label.place(x=80, y=240)

    password_entry=tk.Entry(student_login_page_fm, font=('bold',15), justify=tk.CENTER, highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2, show='*')
    password_entry.place(x=80, y=290)
    password_entry.bind('<KeyRelease>', lambda e:remove_highlight_warning(entry=password_entry))

    show_hide_btn=tk.Button(student_login_page_fm, image=locked_icon, bd=0,command=show_hide_password)
    show_hide_btn.place(x=310, y=290)

    login_button=tk.Button(student_login_page_fm, text='Login', font=('bold',15),bg='#273b7a', fg='white', command=login_account)
    login_button.place(x=95, y=340, width=200, height=40)

    forget_password_btn=tk.Button(student_login_page_fm, text='⚠️\nForget Password', fg='#273b7a', bd=0, command=forward_to_forget_password)
    forget_password_btn.place(x=150, y=390)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400, height=450)

def admin_dashboard():

    def switch(indicator, page):

        home_btn_indicator.config(bg='#c3c3c3')
        find_student_btn_indicator.config(bg='#c3c3c3')
        announce_btn_indicator.config(bg='#c3c3c3')

        indicator.config(bg='#273b7a')
        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()

        page()

    dashboard_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    options_fm=tk.Frame(dashboard_fm, highlightbackground='#273b7a', highlightthickness=2, bg='#c3c3c3')
    
    home_btn=tk.Button(options_fm, text='Home', font=('bold', 15), fg='#273b7a', bg='#c3c3c3', bd=0, command=lambda:switch(indicator=home_btn_indicator, page=home_page))
    home_btn.place(x=10, y=50)
    home_btn_indicator=tk.Label(options_fm, text='', bg='#273b7a')
    home_btn_indicator.place(x=5, y=48, width=3, height=30)

    find_student_btn=tk.Button(options_fm, text='Find\nStudent', font=('bold', 15), fg='#273b7a', bg='#c3c3c3', bd=0, justify=tk.LEFT, command=lambda:switch(indicator=find_student_btn_indicator, page=find_student_page))
    find_student_btn.place(x=10, y=100)
    find_student_btn_indicator=tk.Label(options_fm, text='', bg='#c3c3c3')
    find_student_btn_indicator.place(x=5, y=108, width=3, height=40)
    
    announce_btn=tk.Button(options_fm, text='Announce\n-Ment📢', font=('bold', 15), fg='#273b7a', bg='#c3c3c3', bd=0, justify=tk.LEFT, command=lambda:switch(indicator=announce_btn_indicator, page=announcement_page))
    announce_btn.place(x=10, y=170)
    announce_btn_indicator=tk.Label(options_fm, text='', bg='#c3c3c3')
    announce_btn_indicator.place(x=5, y=180, width=3, height=40)

    def logout():
        confirm=confirmation_box(message='Do you want to\n Logout')

        if confirm:
            dashboard_fm.destroy()
            welcome_page()
            root.update()

    logout_btn=tk.Button(options_fm, text='Logout', font=('bold', 15), fg='#273b7a', bg='#c3c3c3', bd=0, justify=tk.LEFT, command=logout)
    logout_btn.place(x=10, y=240)

    options_fm.place(x=0, y=0, width=120, height=575)

    def home_page():
        home_page_fm=tk.Frame(pages_fm)

        admin_icon_lb=tk.Label(home_page_fm, image=login_admin_icon)
        admin_icon_lb.image=login_admin_icon
        admin_icon_lb.place(x=10, y=10)

        hi_lb=tk.Label(home_page_fm, text='Hi Admin', font=('bold', 15))
        hi_lb.place(x=120, y=40)

        class_list_lb=tk.Label(home_page_fm, text='Number of students by class', font=('bold', 13), bg='#273b7a', fg='white')
        class_list_lb.place(x=20, y=130)

        #fetch_student_data(query="SELECT COUNT (*) FROM data WHERE class == 'S.5' ")

        student_numbers_lb=tk.Label(home_page_fm, text='', font=('bold', 13), justify=tk.LEFT)
        student_numbers_lb.place(x=20, y=170)

        for i in class_list:
            result=fetch_student_data(query=f"SELECT COUNT (*) FROM data WHERE class=='{i}' ")
            student_numbers_lb['text'] += f"{i} Class:    {result[0][0]}\n\n"
            print(i,result)

        home_page_fm.pack(fill=tk.BOTH, expand=True)

    def find_student_page():
        def find_student():
            found_data=''
            if find_by_option.get()=='id':
                found_data=fetch_student_data(query=f"""SELECT id_number, name, class, gender FROM data WHERE id_number=='{search_input.get()}' """)
                print(found_data)
            
            elif find_by_option.get()=='name':
                found_data=fetch_student_data(query=f"""SELECT id_number, name, class, gender FROM data WHERE name LIKE '%{search_input.get()}%'""")
                print(found_data)

            elif find_by_option.get()=='class':
                found_data=fetch_student_data(query=f"""SELECT id_number, name, class, gender FROM data WHERE class== '{search_input.get()}'""")
                print(found_data)

            elif find_by_option.get()=='gender':
                found_data=fetch_student_data(query=f"""SELECT id_number, name, class, gender FROM data WHERE gender== '{search_input.get()}'""")
                print(found_data)

            if found_data:

                for item in record_table.get_children():
                    record_table.delete(item)

                for details in found_data:
                    
                    record_table.insert(parent='', index='end', values=details)

            else:
                for item in record_table.get_children():
                    record_table.delete(item)

        def generate_student_card():
            selection=record_table.selection()
            selected_id=record_table.item(item=selection, option='values')[0]
            get_student_details=fetch_student_data("""
    SELECT name, age, gender, "class", phone_number, email FROM data WHERE id_number =?
""", (selected_id,))
    
            get_student_pic=fetch_student_data("""
    SELECT image FROM data WHERE id_number =?
""", (selected_id,))
    
            student_pic=BytesIO(get_student_pic [0][0])
            
            student_details=f"""
{selected_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""

            student_card_image_obj=draw_student_card(student_pic_path=student_pic, student_data=student_details)

            student_card_page(student_card_obj=student_card_image_obj)

        def clear_result():
            find_by_option.set('id')

            search_input.delete(0, tk.END)

            for item in record_table.get_children():
                record_table.delete(item)

            generate_student_card_btn.config(state=tk.DISABLED)

        search_filters=['id', 'name', 'class', 'gender']
        find_student_page_fm=tk.Frame(pages_fm)

        find_student_lb=tk.Label(find_student_page_fm, text='Find Student Record', font=('bold', 13), fg='white', bg='#273b7a')
        find_student_lb.place(x=20, y=10, width=300)

        find_by_lb=tk.Label(find_student_page_fm, text='Find By:', font=('bold', 12))
        find_by_lb.place(x=15, y=50)

        find_by_option=Combobox(find_student_page_fm, font=('bold', 12), state='readonly', values=search_filters)
        find_by_option.place(x=80, y=50, width=80)
        find_by_option.set('id')

        search_input=tk.Entry(find_student_page_fm, font=('bold', 12))
        search_input.place(x=20, y=90)

        record_table_lb=tk.Label(find_student_page_fm, text='Record Table', font=('bold', 13), bg='#273b7a', fg='white')
        record_table_lb.place(x=20, y=160, width=300)
        search_input.bind('<KeyRelease>', lambda e: find_student())

        record_table=Treeview(find_student_page_fm)
        record_table.place(x=0, y=200, width=350)
        record_table.bind('<<TreeviewSelect>>', lambda e: generate_student_card_btn.config(state=tk.NORMAL))

        record_table['columns']=('id', 'name', 'class', 'gender')

        record_table.column('#0', stretch=tk.NO, width=0)

        record_table.heading('id', text='ID NUMBER', anchor=tk.W)
        record_table.column('id', width=50, anchor=tk.W)

        record_table.heading('name', text='STUDENT NAME', anchor=tk.W)
        record_table.column('name', width=90, anchor=tk.W)

        record_table.heading('class', text='CLASS', anchor=tk.W)
        record_table.column('class', width=40, anchor=tk.W)

        record_table.heading('gender', text='GENDER', anchor=tk.W)
        record_table.column('gender', width=40, anchor=tk.W)

        generate_student_card_btn=tk.Button(find_student_page_fm, text='Generate Student Card', font=('bold', 13), bg='#273b7a', fg='white', state=tk.DISABLED, command=generate_student_card)
        generate_student_card_btn.place(x=160, y=450)

        clear_btn=tk.Button(find_student_page_fm, text='CLEAR', font=('bold', 13), bg='#273b7a', fg='white', command=clear_result)
        clear_btn.place(x=10, y=450)

        find_student_page_fm.pack(fill=tk.BOTH, expand=True)

    def announcement_page():

        selected_classes=[]

        def add_class(name): 

            if selected_classes.count(name):
               selected_classes.remove(name)

            else:
                selected_classes.append(name)
            print(selected_classes)

        def collect_emails():

            fetched_emails=[]

            for _class in selected_classes:
                emails=fetch_student_data(f"SELECT email FROM data WHERE class == '{_class}' ")
                for email_address in emails:
                    fetched_emails.append(*email_address)

            thread=threading.Thread(target=send_announcement, args=[fetched_emails])
            thread.start()

        def send_announcement(email_addresses):
            box_fm=tk.Frame(root, highlightbackground='#273ba7', highlightthickness=3)

            heading_lb=tk.Label(box_fm, text='Sending Email', font=('bold', 15), bg='#273ba7', fg='white')
            heading_lb.place(x=0, y=0, width=300)

            sending_lb=tk.Label(box_fm, font=('bold', 12), justify=tk.LEFT)
            sending_lb.pack(pady=50)

            box_fm.place(x=100, y=120, width=300, height=200)

            subject=announcement_subject.get()
            message=f"<h3 style='white-space: pre_wrap;' >{announcement_message.get('0.1', tk.END)}</h3>"
            sent_count=0

            for email in email_addresses:
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")     
                sendmail_to_student(email=email, subject=subject, message=message)   
                sent_count +=1
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")

            box_fm.destroy()
            message_box(message='Announcement sent successfully')

        announcement_page_fm=tk.Frame(pages_fm)

        subject_lb=tk.Label(announcement_page_fm, text='Enter Announcement Subject', font=('bold', 12))
        subject_lb.place(x=10, y=10)

        announcement_subject=tk.Entry(announcement_page_fm, font=('bold', 12))
        announcement_subject.place(x=10, y=40, width=210, height=25)

        announcement_message=ScrolledText(announcement_page_fm, font=('bold', 12))
        announcement_message.place(x=10, y=100, width=300, height=200)

        class_list_lb=tk.Label(announcement_page_fm, text='Select Classes to Announce', font=('bold', 12))
        class_list_lb.place(x=10, y=320)

        y_position=350

        for grade in class_list:
            class_check_btn=tk.Checkbutton(announcement_page_fm, text=f'Class {grade}', command=lambda grade=grade: add_class(name=grade))
            class_check_btn.place(x=10, y=y_position)
            y_position += 25

        send_announcement_btn=tk.Button(announcement_page_fm, text='Send Announcement', font=('bold', 12), bg='#273ba7', fg='white', command=collect_emails)
        send_announcement_btn.place(x=180, y=520)

        announcement_page_fm.pack(fill=tk.BOTH, expand=True)

    pages_fm=tk.Frame(dashboard_fm)
    pages_fm.place(x=122, y=5, width=350, height=550)
    
    home_page()
    #find_student_page()
    #announcement_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=480, height=580)

def admin_login_page():
    def show_hide_password():

        if password_entry['show']=='*':
            password_entry.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            password_entry.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    def login_account():
        if admin_user_entry.get()=='admin':
            if password_entry.get()=='admin':
                admin_login_page_fm.destroy()
                root.update()
                admin_dashboard()
            else:
                message_box(message='Wrong password')
        else:
            message_box(message='Wrong username')

    admin_login_page_fm=tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)
    heading_label=tk.Label(admin_login_page_fm, text='Admin Login Page', font=('bold',15), bg='#273b7a', fg='white')
    heading_label.place(x=0, y=0, width=400)

    back_button=tk.Button(admin_login_page_fm, text='←', font=('bold',20), fg='#273b7a', bd=0, command=forward_to_welcome)
    back_button.place(x=5, y=40)

    admin_icon_label=tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_label.place(x=150, y=40)

    student_icon_lable=tk.Label(admin_login_page_fm, image=login_addstudent_icon)
    student_icon_lable.place(x=150, y=40)

    admin_user_label=tk.Label(admin_login_page_fm, text='Enter Admin Username',font=('Bold',15),fg='#273b7a')
    admin_user_label.place(x=80, y=140)

    admin_user_entry=tk.Entry(admin_login_page_fm, font=('bold',15), justify=tk.CENTER,highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2 )
    admin_user_entry.place(x=80, y=190)

    password_label=tk.Label(admin_login_page_fm, text='Enter Admin Password', font=('bold',15), fg='#273b7a')
    password_label.place(x=80, y=240)

    password_entry=tk.Entry(admin_login_page_fm, font=('bold',15), justify=tk.CENTER, highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2, show='*')
    password_entry.place(x=80, y=290)

    show_hide_btn=tk.Button(admin_login_page_fm, image=locked_icon, bd=0,command=show_hide_password)
    show_hide_btn.place(x=310, y=290)

    login_button=tk.Button(admin_login_page_fm, text='Login', font=('bold',15),bg='#273b7a', fg='white', command=login_account)
    login_button.place(x=95, y=340, width=200, height=40)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height=430)

student_gender=tk.StringVar()
class_list=['S1','S2','S3','S4','S5','S6']

def add_account_page():
    pic_path=tk.StringVar()
    pic_path.set('')

    def open_pic():
        path=askopenfilename()

        if path:
            img=ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            pic_path.set(path)
            add_pc_btn.config(image=img)
            add_pc_btn.image=img

    def forward_to_welcome_page():
        ans=confirmation_box(message='Do you want to leave\nRegistration form?')
        if ans:
            add_account_page_fm.destroy()
            root.update()
            welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground']!='gray':
            if entry.get()!='':
                entry.config(highlightcolor='#273b7a', highlightbackground='gray')

    def check_invalid_email(email):
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        match=re.match(pattern=pattern, string=email)
        return match

    def generate_id_number():
        generate_id=''
        for r in range(6):
            generate_id +=str(random.randint(0,9))

        if not check_id_already_exists(id_number=generate_id):
            print('id_number:', generate_id)
            student_id.config(state=tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(tk.END, generate_id)
            student_id.config(state='readonly')
        
        else:
            generate_id_number()
         

    def check_input_validation():
        if student_name_entry.get()=='':
            student_name_entry.config(highlightcolor='red', highlightbackground='red')
            student_name_entry.focus()
            message_box(message='Student fullname is required')

        elif student_age_entry.get()=='':
            student_age_entry.config(highlightcolor='red', highlightbackground='red')
            student_age_entry.focus()
            message_box(message='Student age is required')

        elif student_contact_entry.get()=='':
            student_contact_entry.config(highlightcolor='red', highlightbackground='red')
            student_contact_entry.focus()
            message_box(message='Contact number is required')

        elif select_class_btn.get()=='':
            select_class_btn.focus()
            message_box(message='Please select the class!')

        elif student_email_entry.get()=='':
            student_email_entry.config(highlightcolor='red', highlightbackground='red')
            student_email_entry.focus()
            message_box(message='Email address is required')

        elif not check_invalid_email(email=student_email_entry.get().lower()):
            student_email_entry.config(highlightcolor='red', highlightbackground='red')
            student_email_entry.focus()
            message_box(message='Please enter a valid\nEmail address')

        elif account_password_entry.get()=='':
            account_password_entry.config(highlightcolor='red', highlightbackground='red')
            account_password_entry.focus()
            message_box(message='Please enter the account password')

        else:
            #pic_path=b''
            if pic_path.get() !='':
                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png', 'rb')
                pic_data=read_data.read()
                read_data.close()

            else:
                read_data = open(r"C:\Users\hp\Downloads\userprofile.png", 'rb')
                pic_data=read_data.read()
                read_data.close()
                pic_path.set(r"C:\Users\hp\Downloads\userprofile.png")

            add_data(id_number=student_id.get(), password=account_password_entry.get(), name=student_name_entry.get(), age=student_age_entry.get(), gender=student_gender.get(), phone_number=student_contact_entry.get(), student_class=select_class_btn.get(),email=student_email_entry.get(), pic_data=pic_data)
            
            data=f"""
{student_id.get()}
{student_name_entry.get()}
{student_gender.get()}
{student_age_entry.get()}
{select_class_btn.get()}
{student_contact_entry.get()}
{student_email_entry.get()}
"""
            get_student_card=draw_student_card(student_pic_path=pic_path.get(), student_data=data)
            student_card_page(student_card_obj=get_student_card)
            add_account_page_fm.destroy()
            message_box('Account successfully created')
    
    add_account_page_fm= tk.Frame(root, highlightbackground='#273b7a', highlightthickness=3)

    add_pic_section_fm=tk.Frame(add_account_page_fm, highlightbackground='#273b7a', highlightthickness=2)
    add_pc_btn= tk.Button(add_pic_section_fm, image=add_student_pic_icon, command=open_pic)
    add_pc_btn.pack()
    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    student_name_label=tk.Label(add_account_page_fm, text='Enter Full Name', font=('bold',12))
    student_name_label.place(x=5, y=130)

    student_name_entry=tk.Entry(add_account_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
    student_name_entry.place(x=5, y=160, width=180)
    student_name_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_name_entry))

    student_gender_label=tk.Label(add_account_page_fm, text='Select Gender', font=('bold',12))
    student_gender_label.place(x=5, y=210)

    male_gender_btn=tk.Radiobutton(add_account_page_fm, text='Male', font=('bold',12), variable=student_gender, value='male')
    male_gender_btn.place(x=5, y=235)

    female_gender_btn=tk.Radiobutton(add_account_page_fm, text='Female', font=('bold',12), variable=student_gender, value='female')
    female_gender_btn.place(x=75, y=235)
    student_gender.set('male')

    student_age_lb=tk.Label(add_account_page_fm, text='Enter Age', font=('bold',12))
    student_age_lb.place(x=5, y=275)

    student_age_entry=tk.Entry(add_account_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
    student_age_entry.place(x=5, y=305, width=180)
    student_age_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_age_entry))

    student_contact_lb=tk.Label(add_account_page_fm, text='Enter Contact Number', font=('bold',12))
    student_contact_lb.place(x=5, y=360)

    student_contact_entry=tk.Entry(add_account_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
    student_contact_entry.place(x=5, y=390, width=180)
    student_contact_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_contact_entry))

    student_class_lb=tk.Label(add_account_page_fm, text='Select Student Class', font=('bold',12))
    student_class_lb.place(x=5, y=445)

    select_class_btn=Combobox(add_account_page_fm, font=('bold',15), state='readonly', values=class_list)
    select_class_btn.place(x=5, y=475, width=180, height=30)

    student_id_lb=tk.Label(add_account_page_fm, text='Student ID Number:',font=('bold',12))
    student_id_lb.place(x=240, y=35)

    student_id=tk.Entry(add_account_page_fm, font=('bold',18), bd=0)
    student_id.place(x=380, y=35, width=80)

    #student_id.insert(tk.END, '110000')
    student_id.config(state='readonly')
    generate_id_number()

    id_info_lb=tk.Label(add_account_page_fm, text='***Automatically Generated ID Number \n! Remeber using this ID Number \nStudent will login account.***',justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    student_email_lb=tk.Label(add_account_page_fm, text='Enter Email Address', font=('bold',12))
    student_email_lb.place(x=240, y=130)

    student_email_entry=tk.Entry(add_account_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
    student_email_entry.place(x=240, y=160, width=180)
    student_email_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_email_entry))

    email_info_lb=tk.Label(add_account_page_fm, text='***Via Email Address Student\n Can Recover Account\n ! Incase forgettting password***', justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)

    account_password_lb=tk.Label(add_account_page_fm, text='Create Account Password', font=('bold',12))
    account_password_lb.place(x=240, y=275)

    account_password_entry=tk.Entry(add_account_page_fm, font=('bold',15), highlightcolor='#273b7a', highlightbackground='gray', highlightthickness=2)
    account_password_entry.place(x=240, y=307, width=180)
    account_password_entry.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=account_password_entry))

    account_password_info=tk.Label(add_account_page_fm, text='***Via Student create password\n And provided Student ID Number\n Student can login account.***',justify=tk.LEFT)
    account_password_info.place(x=240, y=345)

    home_btn=tk.Button(add_account_page_fm, text='HOME', font=('bold',15),bg='green', fg='white', bd=0, command=forward_to_welcome_page)
    home_btn.place(x=240, y=420)

    submit_btn=tk.Button(add_account_page_fm, text='SUBMIT', font=('bold',15),bg='#273b7a', fg='white', bd=0, command=check_input_validation)
    submit_btn.place(x=360, y=420)


    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=480, height=580)
     
init_database()
#admin_dashboard()
welcome_page()
#student_dashboard(student_id=181143)
#student_login()
root.mainloop()
