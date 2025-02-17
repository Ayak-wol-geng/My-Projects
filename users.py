from tkinter import*
from tkinter import messagebox
import sqlite3 as user

def insertdata():
    name=name_entry.get()
    email=email_entry.get()
    username=username_entry.get()
    password=password_entry.get()
    confirm_password=confirm_password_entry.get()

    if not name or not email or not username or not password or not confirm_password:
        messagebox.showerror("Error", "Please fill in the required fields!")
        return

    if not username.isalpha() or not name.isalpha() :
        messagebox.showerror("Invalid Input", "Please enter the username again.")
        return

    
    if '@' not in email or '.' not in email or email.count('@') != 1:
        messagebox.showerror("Invalid Input", "Please enter a valid email address.")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    connection=user.connect('user.db')
    x=connection.cursor()
    x.execute('create table if not exists users(id integer primary key,name text, email text,username text, password text)')
    x.execute('insert into users(name,email,username,password) values (?,?,?,?)',(name,email,username,password))
    connection.commit()
    messagebox.showinfo('success','inserted successfully')
    print('Registered')
    x.execute('select * from users')
    print(x.fetchall())
    connection.commit()
def lognow():
    app.destroy()
    app2=Tk()
    app2.title('Login')
    app2.geometry('500x400')
    app2.configure(bg='pink')

    
    Label(app2, text='Username', font=('Calibri', 16)).place(x=10, y=40)
    username_entry2 = Entry(app2, font=('Calibri', 16))
    username_entry2.place(x=150, y=40)

    Label(app2, text='Password', font=('Calibri', 16)).place(x=10, y=100)
    password_entry2 = Entry(app2, font=('Calibri', 16), show='*')
    password_entry2.place(x=150, y=100)


    #Button(app2, text='Login', font=('Calibri', 16)).place(x=180, y=150)
    Button(app2,text='Login',font=('Calibri',16),command=welcome).place(x=180,y=150)


def welcome():
    app2.destroy()
    app3=Tk()
    app3.title('Welcome')
    app3.geometry('500x400')
    app3.configure(bg='pink')

    #Button(app,text='Welcome',font=('Calibri',16),command=welcome).place(x=150,y=150)

    app3.mainloop()

    app2.mainloop()



def navigate():
    insertdata()
    lognow()
    #welcome()

app=Tk()
app.title('Register page')
app.geometry('500x400')
app.configure(bg='pink')
Label(app,text='Name',font=('Calibri',16)).place(x=10,y=40)
name_entry=Entry(app,font=('Calibri',16))
name_entry.place(x=150,y=40)

Label(app,text='Email',font=('Calibri',16)).place(x=10,y=100)
email_entry=Entry(app,font=('Calibri',16))
email_entry.place(x=150,y=100)

Label(app,text='Username',font=('Calibri',16)).place(x=10,y=160)
username_entry=Entry(app,font=('Calibri',16))
username_entry.place(x=150,y=160)

Label(app,text='Password',font=('Calibri',16)).place(x=10,y=200)
password_entry=Entry(app,font=('Calibri',16),show='*')
password_entry.place(x=150,y=200)

Label(app,text='Confirm Password',font=('Calibri',16)).place(x=10,y=240)
confirm_password_entry=Entry(app,font=('Calibri',16),show='*')
confirm_password_entry.place(x=150,y=240)

Button(app,text='Register',font=('Calibri',16),command=navigate).place(x=180,y=280)
#Button(app,text='Login',font=('Calibri',16),command=lognow).place(x=150,y=150)




app.mainloop()

 
