import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import ttk
import mysql.connector

class registration:
    def __init__(self,top):
        self.top = top
        self.top.title("STUDENT FRAME")
        self.top.geometry("400x600+0+0")
        self.top.config(bg = "gray")

        ###--------creating input frame-----
        frame1 = Frame(self.top,bg = "skyblue",bd = 10,relief = GROOVE)
        frame1.place(x = 0,y = 0,width = 400,height = 350)
        headlabel = Label(frame1, text="STUDENT FORM", font=("arial bold", 20), bg="skyblue")
        headlabel.grid(row=0, columnspan=2, pady=10, padx=60)

        roll = Label(frame1, text="Roll No.", font=("times new roman", 13), bg="skyblue")
        roll.grid(row=1, column=0, columnspan=1, pady=5, padx=20, sticky="w")
        self.rollentry = Entry(frame1, font=("times new roman", 13), bd=5, relief=GROOVE)
        self.rollentry.grid(row=1, column=1, columnspan=1, pady=10, padx=0, sticky="w")

        name = Label(frame1, text="Name", font=("times new roman", 13), bg="skyblue")
        name.grid(row=2, column=0, columnspan=1, pady=5, padx=20, sticky="w")
        self.nameentry = Entry(frame1, font=("times new roman", 13), bd=5, relief=GROOVE)
        self.nameentry.grid(row=2, column=1, columnspan=1, pady=10, padx=0, sticky="w")

        gender = Label(frame1, text="Gender", font=("times new roman", 13), bg="skyblue")
        gender.grid(row=3, column=0, columnspan=1, pady=5, padx=20, sticky="w")
        self.gendercombobox = ttk.Combobox(frame1, height=1, width=18, state="readonly", font=("times new roman", 13))
        self.gendercombobox["values"] = ('male', 'female', 'others')
        self.gendercombobox.grid(row=3, column=1, columnspan=1, pady=5, padx=0, sticky="w")

        address = Label(frame1, text="address", font=("times new roman", 13), bg="skyblue")
        address.grid(row=4, column=0, columnspan=1, pady=5, padx=20, sticky="w")
        self.text = Text(frame1,height = 3,width = 20,font = ("times new roman",13))
        self.text.grid(row=4, column=1, columnspan=1, pady=5, padx=2, sticky="w")

        buttonframe = Frame(frame1,bg = "skyblue",bd = 5,relief = GROOVE)
        buttonframe.place(x = 20,y = 265,width = 350,height = 60)
        b1 = Button(buttonframe, text="Add", font=("times new roman", 8),width = 7,command = self.add)
        b1.grid(row=0, column=0, pady=13, padx=15, sticky="w")
        b2 = Button(buttonframe, text="Update", font=("times new roman", 8), width=7,command = self.update)
        b2.grid(row=0, column=1, pady=13, padx=15, sticky="w")
        b3 = Button(buttonframe, text="Delete", font=("times new roman", 8), width=7,command = self.delete)
        b3.grid(row=0, column=2, pady=13, padx=15, sticky="w")
        b4 = Button(buttonframe, text="New", font=("times new roman", 8), width=7,command = self.new)
        b4.grid(row=0, column=3, pady=13, padx=15, sticky="w")


        frame2 = Frame(self.top, bg="skyblue", bd=10, relief=GROOVE)
        frame2.place(x=0, y=350, width=400, height=250)

        scroll_x = Scrollbar(frame2,orient = HORIZONTAL)
        scroll_Y = Scrollbar(frame2, orient=VERTICAL)
        self.visibelframe = ttk.Treeview(frame2,column=("roll","name","gender","address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_Y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_Y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.visibelframe.xview)
        scroll_Y.config(command=self.visibelframe.yview)
        self.visibelframe.heading("roll",text ="Roll N0.")
        self.visibelframe.heading("name", text="Name")
        self.visibelframe.heading("gender", text=" Gender")
        self.visibelframe.heading("address", text="Address")
        self.visibelframe["show"]='headings'
        self.visibelframe.column("roll",width = 50)
        self.visibelframe.column("name", width=50)
        self.visibelframe.column("gender", width=50)
        self.visibelframe.column("address", width=100)
        self.visibelframe.pack(fill = BOTH,expand = 1)
        self.visibelframe.bind('<ButtonRelease-1>',self.get_cursor)
        self.fetchdata()

    def add(self):
        d1 = self.rollentry.get()
        d2 = self.nameentry.get()
        d3 = self.gendercombobox.get()
        d4 = self.text.get("1.0", END)
        cnx = mysql.connector.connect(username = "root",passwd = "1431",host = "localhost",database = "student")
        cursor = cnx.cursor()
        sql = "insert into student_details values (%s,%s,%s,%s)"
        val = (d1,d2,d3,d4)
        cursor.execute(sql,val)
        cnx.commit()
        self.fetchdata()
        self.new()
        cnx.close()
        messagebox.showinfo(message="Done")

    def new(self):
        self.rollentry.delete(0,"end")
        self.nameentry.delete(0,"end")
        self.gendercombobox.set("")
        self.text.delete("1.0",END)
        messagebox.showinfo(message="Enter Data")
    def get_cursor(self,eve):
        row_values = self.visibelframe.focus()
        content = self.visibelframe.item(row_values)
        row = content['values']
        #self.rollentry.set(row[0])
        #self.nameentry.set(row[1])
        self.gendercombobox.set(row[2])
        self.text.delete("1.0", END)
        self.text.insert(END,row[3])

    def update(self):
        d1 = self.rollentry.get()
        d2 = self.nameentry.get()
        d3 = self.gendercombobox.get()
        d4 = self.text.get("1.0", END)
        cnx = mysql.connector.connect(username="root", passwd="1431", host="localhost", database="student")
        cursor = cnx.cursor()
        sql = "update student_details set name = %s,gender = %s,address = %s where roll_no = %s;"
        val = (d2, d3, d4,d1)
        cursor.execute(sql, val)
        cnx.commit()
        self.fetchdata()
        cnx.close()
        messagebox.showinfo(message="Done")

    def delete(self):
        d1 = self.rollentry.get()
        cnx = mysql.connector.connect(username="root", passwd="1431", host="localhost", database="student")
        cursor = cnx.cursor()
        sql = "delete from student_details where roll_no = %s;"
        val = (d1,)
        cursor.execute(sql, val)
        cnx.commit()
        self.fetchdata()
        cnx.close()
        messagebox.showinfo(message="Done")

    def fetchdata(self):
        cnx = mysql.connector.connect(username="root", passwd="1431", host="localhost", database="student")
        cursor = cnx.cursor()
        cursor.execute("select * from student_details")
        rows = cursor.fetchall()
        if len(rows)!=0:
            self.visibelframe.delete(*self.visibelframe.get_children())
            for row in rows:
                self.visibelframe.insert('',END,values = row)
                cnx.commit()
            cnx.close()



top = Tk()
obj = registration(top)
top.mainloop()