from tkinter import *
from tkinter.ttk import Separator
from tkinter import messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Saini#12345",
    database="hospital_management_system"
)
c = conn.cursor()

# Create table if it does not exist
c.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    location VARCHAR(255),
    phone VARCHAR(15)
)
""")

# Tkinter window
class Application:
    def __init__(self, window):
        self.window = window
        self.v = IntVar()
        c.execute("SELECT * FROM appointments")
        self.alldata = c.fetchall()

        self.main = Frame(window, width=450, height=400, bg="lightblue")
        self.showdetailsframe = Frame(self.window)
        self.updateframe = Frame(self.window)
        self.deleteframe = Frame(self.window)

    def startpage(self):
        self.heading = Label(self.main, text="Hospital Management System", font=('Centaur 20 bold'), fg='black', bg="grey", relief=SUNKEN)
        self.heading.place(x=30, y=20)

        # Labels and Entries
        Label(self.main, text="Patients Name", font=('arial 12 bold'), bg="lightblue").place(x=0, y=110)
        self.name_ent = Entry(self.main, width=30)
        self.name_ent.place(x=140, y=115)

        Label(self.main, text="Age", font=('arial 12 bold'), bg="lightblue").place(x=0, y=155)
        self.age_ent = Entry(self.main, width=30)
        self.age_ent.place(x=140, y=160)

        Label(self.main, text="Gender", font=('arial 12 bold'), bg="lightblue").place(x=0, y=210)
        Radiobutton(self.main, text="Male", padx=20, font="ariel 10 bold", variable=self.v, value=1, bg="lightblue").place(x=130, y=210)
        Radiobutton(self.main, text="Female", padx=20, font="ariel 10 bold", variable=self.v, value=2, bg="lightblue").place(x=220, y=210)

        Label(self.main, text="Location", font=('arial 12 bold'), bg="lightblue").place(x=0, y=255)
        self.location_ent = Entry(self.main, width=30)
        self.location_ent.place(x=140, y=258)

        Label(self.main, text="Contact Number", font=('arial 12 bold'), bg="lightblue").place(x=0, y=300)
        self.phone_ent = Entry(self.main, width=30)
        self.phone_ent.place(x=140, y=310)

        self.submit = Button(self.main, text="Add Appointment", font="aried 12 bold", width=15, height=2, bg='lightgreen', command=self.add_appointment)
        self.submit.place(x=150, y=340)

        sql2 = "SELECT COUNT(id) FROM appointments"
        c.execute(sql2)
        self.final_id = c.fetchone()[0]

        self.logs = Label(self.main, text="Total\nAppointments", font=('arial 10 bold'), fg='black', bg="lightblue")
        self.logs.place(x=340, y=320)
        Label(self.main, text=" " + str(self.final_id), width=8, height=1, relief=SUNKEN).place(x=360, y=360)

        self.main.pack()

    def add_appointment(self):
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        if self.v.get() == 1:
            self.val3 = "Male"
        elif self.v.get() == 2:
            self.val3 = "Female"
        else:
            self.val3 = "Not Specified"
        self.val4 = self.location_ent.get()
        self.val5 = self.phone_ent.get()

        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            sql = "INSERT INTO appointments (name, age, gender, location, phone) VALUES (%s, %s, %s, %s, %s)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5))
            conn.commit()
            messagebox.showinfo("Success", "\n Appointment for " + str(self.val1) + " has been created")
            self.main.destroy()
            self.__init__(self.window)
            self.startpage()

    def homee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        self.startpage()
        self.main.pack()

    def showdetails(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)
        count1 = 0
        count2 = 0
        clmnname = ['App no', 'name', 'age', 'gender', 'location', 'contact no']
        for i in range(len(clmnname)):
            Label(self.showdetailsframe, text=clmnname[i], font="ariel 12 bold").grid(row=0, column=i * 2)
            Separator(self.showdetailsframe, orient=VERTICAL).grid(row=0, column=i * 2 + 1, sticky='ns')

        for i in range(len(self.alldata)):
            for j in range(6):
                Label(self.showdetailsframe, text=self.alldata[i][j], font="ariel 10").grid(row=count1 + 2, column=count2 * 2)
                Separator(self.showdetailsframe, orient=VERTICAL).grid(row=count1 + 2, column=count2 * 2 + 1, sticky='ns')
                count2 += 1
            count2 = 0
            count1 += 1
        self.showdetailsframe.pack()

    def updatee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)

        self.id = Label(self.updateframe, text="Search Appointment Number To Update", font=('arial 12 bold'), fg="red")
        self.id.place(x=0, y=12)
        self.idnet = Entry(self.updateframe, width=10)
        self.idnet.place(x=320, y=18)
        self.search = Button(self.updateframe, text="Search", font="aried 12 bold", width=10, height=1, bg='lightgreen', command=self.update1)
        self.search.place(x=160, y=50)
        self.updateframe.pack(fill='both', expand=True)

    def update1(self):
        self.input = self.idnet.get()
        sql = "SELECT * FROM appointments WHERE id LIKE %s"
        c.execute(sql, (self.input,))
        self.row = c.fetchone()
        if self.row:
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.phone = self.row[5]

            self.uname = Label(self.updateframe, text="Patient's Name", font=('arial 14 bold'))
            self.uname.place(x=0, y=140)
            self.uage = Label(self.updateframe, text="Age", font=('arial 14 bold'))
            self.uage.place(x=0, y=180)
            self.ugender = Label(self.updateframe, text="Gender", font=('arial 14 bold'))
            self.ugender.place(x=0, y=220)
            self.ulocation = Label(self.updateframe, text="Location", font=('arial 14 bold'))
            self.ulocation.place(x=0, y=260)
            self.uphone = Label(self.updateframe, text="Phone Number", font=('arial 14 bold'))
            self.uphone.place(x=0, y=300)

            self.ent1 = Entry(self.updateframe, width=30)
            self.ent1.place(x=180, y=140)
            self.ent1.insert(END, str(self.name1))

            self.ent2 = Entry(self.updateframe, width=30)
            self.ent2.place(x=180, y=180)
            self.ent2.insert(END, str(self.age))

            self.ent3 = Entry(self.updateframe, width=30)
            self.ent3.place(x=180, y=220)
            self.ent3.insert(END, str(self.gender))

            self.ent4 = Entry(self.updateframe, width=30)
            self.ent4.place(x=180, y=260)
            self.ent4.insert(END, str(self.location))

            self.ent5 = Entry(self.updateframe, width=30)
            self.ent5.place(x=180, y=300)
            self.ent5.insert(END, str(self.phone))

            self.update = Button(self.updateframe, text="Update Appointment", font="aried 12 bold", width=15, height=2, bg='lightgreen', command=self.update2)
            self.update.place(x=220, y=340)
        else:
            messagebox.showerror("Error", "Appointment Not Found")
        self.updateframe.pack(fill='both', expand=True)

    def update2(self):
        self.val1 = self.ent1.get()
        self.val2 = self.ent2.get()
        self.val3 = self.ent3.get()
        self.val4 = self.ent4.get()
        self.val5 = self.ent5.get()

        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            sql = "UPDATE appointments SET name = %s, age = %s, gender = %s, location = %s, phone = %s WHERE id = %s"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5, self.input))
            conn.commit()
            messagebox.showinfo("Updated", "Successfully Updated")
            self.updateframe.destroy()
            self.homee()

    def deletee(self):
        self.main.destroy()
        self.showdetailsframe.destroy()
        self.updateframe.destroy()
        self.deleteframe.destroy()
        self.__init__(self.window)

        self.delid = Label(self.deleteframe, text="Search Appointment Number To Delete", font=('arial 12 bold'), fg="red")
        self.delid.place(x=0, y=12)
        self.delidnet = Entry(self.deleteframe, width=10)
        self.delidnet.place(x=320, y=18)
        self.delsearch = Button(self.deleteframe, text="Search", font="aried 12 bold", width=10, height=1, bg='lightgreen', command=self.delete1)
        self.delsearch.place(x=160, y=50)
        self.deleteframe.pack(fill='both', expand=True)

    def delete1(self):
        self.idd = self.delidnet.get()
        sql = "SELECT * FROM appointments WHERE id LIKE %s"
        c.execute(sql, (self.idd,))
        self.row = c.fetchone()
        if self.row:
            self.name = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.phone = self.row[5]

            self.dname = Label(self.deleteframe, text="Patient's Name", font=('arial 14 bold'))
            self.dname.place(x=0, y=140)
            self.dage = Label(self.deleteframe, text="Age", font=('arial 14 bold'))
            self.dage.place(x=0, y=180)
            self.dgender = Label(self.deleteframe, text="Gender", font=('arial 14 bold'))
            self.dgender.place(x=0, y=220)
            self.dlocation = Label(self.deleteframe, text="Location", font=('arial 14 bold'))
            self.dlocation.place(x=0, y=260)
            self.dphone = Label(self.deleteframe, text="Phone Number", font=('arial 14 bold'))
            self.dphone.place(x=0, y=300)

            self.dent1 = Entry(self.deleteframe, width=30)
            self.dent1.place(x=180, y=140)
            self.dent1.insert(END, str(self.name))
            self.dent1.configure(state='disabled')

            self.dent2 = Entry(self.deleteframe, width=30)
            self.dent2.place(x=180, y=180)
            self.dent2.insert(END, str(self.age))
            self.dent2.configure(state='disabled')

            self.dent3 = Entry(self.deleteframe, width=30)
            self.dent3.place(x=180, y=220)
            self.dent3.insert(END, str(self.gender))
            self.dent3.configure(state='disabled')

            self.dent4 = Entry(self.deleteframe, width=30)
            self.dent4.place(x=180, y=260)
            self.dent4.insert(END, str(self.location))
            self.dent4.configure(state='disabled')

            self.dent5 = Entry(self.deleteframe, width=30)
            self.dent5.place(x=180, y=300)
            self.dent5.insert(END, str(self.phone))
            self.dent5.configure(state='disabled')

            self.delete2 = Button(self.deleteframe, text="Delete Appointment", font="aried 12 bold", width=15, height=2, bg='lightgreen', command=self.delete2)
            self.delete2.place(x=220, y=340)
        else:
            messagebox.showerror("Error", "Appointment Not Found")
        self.deleteframe.pack(fill='both', expand=True)

    def delete2(self):
        sql = "DELETE FROM appointments WHERE id LIKE %s"
        c.execute(sql, (self.idd,))
        conn.commit()
        messagebox.showinfo("Deleted", "Appointment has been Deleted")
        self.deleteframe.destroy()
        self.homee()


window = Tk()
app = Application(window)
app.startpage()

# Menu Bar
menubar = Menu(window)
home = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=home)
home.add_command(label="Home", command=app.homee)
home.add_command(label="Add Appointment", command=app.startpage)
home.add_command(label="Show Appointments", command=app.showdetails)
home.add_command(label="Update Appointment", command=app.updatee)
home.add_command(label="Delete Appointment", command=app.deletee)
home.add_separator()
home.add_command(label="Exit", command=window.quit)
window.config(menu=menubar)

window.geometry("450x450")
window.resizable(False, False)
window.title("Hospital Management")
window.iconbitmap(r'medkit.ico')

window.mainloop()
