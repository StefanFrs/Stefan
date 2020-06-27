from tkinter import *
import sqlite3
import tkinter.messagebox
from tkinter import messagebox as ms
from PIL import ImageTk, Image
from getpass import getpass
import logging
import time

logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def exit1():
    exit()


############# Pagina de start ##########

def main_window():
    global window
    window = Tk()
    window.geometry("1024x728")
    window.title("Get@Car")
    window.iconbitmap('C:/Users/Stefan/PycharmProjects/proiect/icon.ico')

    img = ImageTk.PhotoImage(Image.open("main5.jpg"))
    my_label_img = Label(image=img)
    my_label_img.pack()

    button1 = Button(window, text="Logare", fg='white', bg='gray30', relief=GROOVE, command=log_win,
                     font=("arial", 15, "bold"))
    button1.place(x=100, y=250)

    button2 = Button(window, text="Inregistrare", fg='white', bg='gray30', relief=GROOVE, command=sign_win,
                     font=("arial", 15, "bold"))
    button2.place(x=90, y=150)

    button3 = Button(window, text="Iesire", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                     command=exit1)
    button3.place(x=100, y=350)

    window.mainloop()


##############PUBLICA ANUNT + Vezi inregistrarile######################

def Publica_anunt_win():
    pub = Toplevel(window)
    pub.geometry("1024x728")
    pub.title("Inregistrare")
    pub.iconbitmap('C:/Users/Stefan/PycharmProjects/proiect/icon.ico')

    img = ImageTk.PhotoImage(Image.open("main5.jpg"))
    my_label_img = Label(image=img)
    my_label_img.pack()

    global fn
    global ln
    fn = StringVar()
    ln = StringVar()
    nr = StringVar()
    dog = StringVar()
    cap = StringVar()
    radio_var = StringVar()

    def data_bases():
        name1 = fn.get()
        last1 = ln.get()
        nrTel = nr.get()
        email = dog.get()
        capacitate = cap.get()
        gender = radio_var.get()
        conn = sqlite3.connect("Form.db")
        with conn:
            cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Postari_inregistrate (Marca TEXT,Model TEXT,An integer,Kilometri TEXT, Combustibil TEXT , Capacitate integer)')
        cursor.execute(
            'INSERT INTO Postari_inregistrate(Marca, Model,An,Kilometri,Combustibil,Capacitate) VALUES(?,?,?,?,?,?)',
            (name1, last1, nrTel, email, gender, capacitate))

        conn.commit()

        conn.close()

        entry_nume.delete(0, END)
        entry_parola.delete(0, END)
        entry_nrTel.delete(0, END)
        entry_Email.delete(0, END)
        entry_Cap.delete(0, END)

    #####AFISEAZA INREGISTRARILE#######3

    def query():
        conn = sqlite3.connect("Form.db")
        cursor = conn.cursor()
        cursor.execute("SELECT *,oid FROM Postari_inregistrate")
        records = cursor.fetchall()
        logging.info(records)

        print_records = ''
        for record in records:
            print_records += str(record) + "\n"

        records_label = Label(pub, text=print_records, width=50, font=("arial", 13, "bold"))
        records_label.place(x=480, y=150)

        conn.commit()
        conn.close()

    label0 = Label(pub, text="Descriere produs:", relief="solid", width=20, font=("arial", 20, "bold"))
    label0.place(x=150, y=50)

    label1 = Label(pub, text="Marca:", width=20, font=("arial", 15, "bold"))
    label1.place(x=93, y=150)

    entry_nume = Entry(pub, textvar=fn)
    entry_nume.place(x=250, y=155)

    label2 = Label(pub, text="Model:", width=20, font=("arial", 15, "bold"))
    label2.place(x=90, y=200)

    entry_parola = Entry(pub, textvar=ln)
    entry_parola.place(x=250, y=205)

    label3 = Label(pub, text="An de fabricatie:", width=20, font=("arial", 15, "bold"))
    label3.place(x=40, y=250)

    entry_nrTel = Entry(pub, textvar=nr)
    entry_nrTel.place(x=250, y=255)

    label4 = Label(pub, text="Kilometri:", width=20, font=("arial", 15, "bold"))
    label4.place(x=70, y=300)

    entry_Email = Entry(pub, textvar=dog)
    entry_Email.place(x=250, y=305)

    label5 = Label(pub, text="Combustibil:", width=20, font=("arial", 15, "bold"))
    label5.place(x=70, y=350)

    entry_Cap = Entry(pub, textvar=cap)
    entry_Cap.place(x=250, y=405)

    label6 = Label(pub, text="Capacitate motor:", width=14, font=("arial", 15, "bold"))
    label6.place(x=75, y=400)

    r1 = Radiobutton(pub, text='Benzina', variable=radio_var, value="Benzina").place(x=250, y=355)
    r2 = Radiobutton(pub, text='Motorina', variable=radio_var, value="Motorina").place(x=330, y=355)
    r3 = Radiobutton(pub, text='Hybrid', variable=radio_var, value="Hybrid").place(x=420, y=355)
    r4 = Radiobutton(pub, text='Electric', variable=radio_var, value="Electric").place(x=490, y=355)

    query_button = Button(pub, text="Inregistrarile facute:", fg='white', bg='gray30', relief=GROOVE,
                          font=("arial", 15, "bold"),
                          command=query)

    query_button.place(x=600, y=50)

    b1 = Button(pub, text="Finalizare", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=data_bases)
    b1.place(x=300, y=600)
    b2 = Button(pub, text="Exit", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=pub.destroy)
    b2.place(x=600, y=600)


#       LOGARE         #

def log_win():
    log = Toplevel(window)
    log.geometry("1024x728")
    log.title("Logare")
    log.iconbitmap('C:/Users/Stefan/PycharmProjects/proiect/icon.ico')

    ######### LOGIN CHECK#####
    def login_database():
        conn = sqlite3.connect("Form.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Persoane_Inregistrate WHERE First_Name=? AND Last_Name=? ",
                       (username_entry1.get(), password_entry1.get()))
        row = cursor.fetchall()
        conn.close()
        print(row)
        if row != []:
            user_name = row[0][0]
            l3.config(text="User name found with name:" + user_name)
            Publica_anunt_win()
        else:
            l3.config(text="User not found")

    label0 = Label(log, text="LOGARE", relief="solid", width=20, font=("arial", 20, "bold"))
    label0.place(x=350, y=150)

    label1 = Label(log, text="Nume:", width=5, font=("arial", 15, "bold"))
    label1.place(x=380, y=200)

    l3 = Label(log, font="arial 20", fg='green')
    l3.place(x=300, y=300)

    username_verify = StringVar()
    username_entry1 = Entry(log, textvar=username_verify)
    username_entry1.place(x=455, y=205)

    label2 = Label(log, text="Parola:", width=5, font=("arial", 15, "bold"))
    label2.place(x=380, y=250)

    password_verify = StringVar()
    password_entry1 = Entry(log, textvar=password_verify, show='*')
    password_entry1.place(x=455, y=255)

    b1 = Button(log, text="Logare", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=login_database)
    b1.place(x=300, y=600)

    b2 = Button(log, text="Inapoi", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=log.destroy)
    b2.place(x=600, y=600)


########INREGISTRARE########


def sign_win():
    sign = Toplevel(window)
    sign.geometry("1024x728")
    sign.title("Inregistrare")
    sign.iconbitmap('C:/Users/Stefan/PycharmProjects/proiect/icon.ico')

    img = ImageTk.PhotoImage(Image.open("main5.jpg"))
    my_label_img = Label(image=img)
    my_label_img.pack()

    global fn
    global ln
    fn = StringVar()
    ln = StringVar()
    nr = StringVar()
    dog = StringVar()
    radio_var = StringVar()

    def data_bases():
        name1 = fn.get()
        last1 = ln.get()
        nrTel = nr.get()
        email = dog.get()
        gender = radio_var.get()
        conn = sqlite3.connect("Form.db")
        with conn:
            cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Persoane_Inregistrate (First_Name TEXT,Last_Name TEXT,nrTel integer,Email TEXT, Gender TEXT)')
        cursor.execute('INSERT INTO Persoane_Inregistrate(First_Name,Last_Name,nrTel,Email,Gender) VALUES(?,?,?,?,?)',
                       (name1, last1, nrTel, email, gender))
        conn.commit()
        conn.close()

        entry_nume.delete(0, END)
        entry_parola.delete(0, END)
        entry_nrTel.delete(0, END)
        entry_Email.delete(0, END)

    label0 = Label(sign, text="INREGISTRARE", relief="solid", width=20, font=("arial", 20, "bold"))
    label0.place(x=150, y=50)

    label1 = Label(sign, text="Nume:", width=20, font=("arial", 15, "bold"))
    label1.place(x=93, y=150)

    entry_nume = Entry(sign, textvar=fn)
    entry_nume.place(x=250, y=155)

    label2 = Label(sign, text="Parola:", width=20, font=("arial", 15, "bold"))
    label2.place(x=90, y=200)

    entry_parola = Entry(sign, textvar=ln, show='*')
    entry_parola.place(x=250, y=205)

    label3 = Label(sign, text="Numar de telefon:", width=20, font=("arial", 15, "bold"))
    label3.place(x=40, y=250)

    entry_nrTel = Entry(sign, textvar=nr)
    entry_nrTel.place(x=250, y=255)

    label4 = Label(sign, text="Email:", width=20, font=("arial", 15, "bold"))
    label4.place(x=94, y=300)

    entry_Email = Entry(sign, textvar=dog)
    entry_Email.place(x=250, y=305)

    label5 = Label(sign, text="Genul:", width=20, font=("arial", 15, "bold"))
    label5.place(x=94, y=350)

    r1 = Radiobutton(sign, text='Barbat', variable=radio_var, value="Barbat").place(x=250, y=355)
    r2 = Radiobutton(sign, text='Femeie', variable=radio_var, value="femeie").place(x=330, y=355)

    b1 = Button(sign, text="Finalizare", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=data_bases)
    b1.place(x=300, y=600)

    b2 = Button(sign, text="Inapoi", fg='white', bg='gray30', relief=GROOVE, font=("arial", 15, "bold"),
                command=sign.destroy)
    b2.place(x=600, y=600)



main_window()
