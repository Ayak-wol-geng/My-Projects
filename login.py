from tkinter import*
from tkinter import messagebox
import sqlite3 as k

class register:
    def __init__(self,root):
        self.root=root
        self.root.title=title('Registration form')
        self.root.geometry('500x400')
        self.root.configure('light blue')
        
        Label(self.root,text='Name',font=('Calibri',16)).pack()
        self.name_entry=Entry(self.root,font=('Calibri',16))
        self.name_entry.pack()


        Label(self.root,text='Age',font=('Calibri',16)).pack()
        self.age_entry=Entry(self.root,font=('Calibri',16))
        self.age_entry.pack()

        Label(self.root,text='Email',font=('Calibri',16)).pack()
        self.email_entry=Entry(self.root,font=('Calibri',16))
        self.email_entry.pack()

        Button(self.root,text='Register',font=('Calibri',16),command self.insert_data).pack()
        Button(self.root,text='Login',font=('Calibri',16),command self.login).pack()

        def insert_data():
            name=self.name_entry.get()
            age=self.age_entry.get()
            email=self.email_entry.get()

        def login():
            self.root.destroy()
            Login()
            


class login:
    def __init__(self,root):
        self.root=root
        self.root.title=title('Registration form')
        self.root.geometry('500x400')
        self.root.configure('light blue')
        
        Label(self.root,text='Name',font=('Calibri'),16).pack()
        self.name_entry=Entry(self.root,font=('Calibri'),16)
        self.name_entry.pack()


        Label(self.root,text='Email',font=('Calibri'),16).pack()
        self.email_entry=Entry(self.root,font=('Calibri'),16)
        self.email_entry.pack()

        Button(self.root,text='Register',font=('Calibri'),16),command self.insert_data.pack()
        Button(self.root,text='Login',font=('Calibri'),16),command self.login.pack()
        self.root.mainloop()

    def register(self):
        pass
if __name__=='main':
    root=Tk()
    Register(root)
    root.mainloop()

        
