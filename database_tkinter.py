from tkinter import *
from tkinter import messagebox
import sqlite3 as k

def insertdata():
    name=name_entry.get()
    age=age_entry.get()
    email=email_entry.get()
    connection=k.connect('home.db')
    x=connection.cursor()
    x.execute('create table if not exists staff (id integer primary key autoincrement,name text,age int,email text)')
    x.execute('insert into staff(name,age,email) values (?,?,?)',(name,age,email))
    connection.commit()
    messagebox.showinfo('success','Inserted successfully')
    print('Registered')
    x.execute('select * from staff ')
    print(x.fetchall())
    connection.commit()
def lognow():
    app.destroy()
    app2=Tk()
    app2.title('Login')
    app2.geometry('700x600')
    app2.configure(bg='pink')

    
app=Tk()
app.title('Register Page')
app.geometry('500x400')
app.configure(bg='grey')
Label(app,text='Name',font=('Calibri',16)).pack()
name_entry=Entry(app,font=('Calibri',16))
name_entry.pack()
Label(app,text='Age',font=('Calibri',16)).pack()
age_entry=Entry(app,font=('Calibri',16))
age_entry.pack()
Label(app,text='Email',font=('Calibri',16)).pack()
email_entry=Entry(app,font=('Calibri',16))
email_entry.pack()
Button(app,text='Register',font=('Calibri',16),command=insertdata).pack()
Button(app,text='Login',font=('Calibri',16),command=lognow).pack()


app.mainloop()

