from tkinter import *
from tkinter import messagebox
import pymysql as pm

root = Tk()
root.geometry('700x800')
root.title('Notekeeper')

# database
try:
    con = pm.connect(host='localhost', database='notes', user='root', password='12345')
    cursor = con.cursor()
    


    # function for adding new notes
    def ADD_NOTES():
        r1 = Toplevel()
        r1.title('Add notes')
        r1.geometry('550x550')

        l2 = Label(r1, text='NOTES TITLE')
        l2.place(x=5, y=5)
        e2 = Entry(r1, width=30, font=('times', 15))
        e2.place(x=5, y=25)

        l3 = Label(r1, text='NOTES')
        l3.place(x=5, y=70)

        s2 = Scrollbar(r1)
        s2.place(x=430, y=90)
        s4 = Scrollbar(r1)
        t2 = Text(r1, height=20, wrap=NONE, width=50, xscrollcommand=s4.set, yscrollcommand=s2.set)
        s2.config(command=t2.yview)
        s4.config(command=t2.xview, orient=HORIZONTAL)
        t2.place(x=5, y=90)
        s4.place(x=5, y=425)

        def ADD_NOTES_DB():
            try:
                if len(e2.get()) != 0:
                    if (len(t2.get("1.0", "end-1c")) == 0):
                        msg1 = messagebox.askokcancel("NO DATA WILL BE ADDED %s notes" % (e2.get()))
                        if msg1:
                            cursor.execute(" INSERT INTO tb1 VALUES (%s,%s) ", (e2.get(), t2.get("1.0", END)))
                            con.commit()
                            e2.delete(0, 'end')
                            t2.delete("1.0", END)
                            messagebox.showinfo("NOTES WILL BE ADDED SUCESSFULLY :D")

                        else:
                            sol = messagebox.askyesno("Q1: DO YOU WANT TO ADD AGAIN->")
                            if sol:
                                add_new_notes()

                    else:
                        cursor.execute(" INSERT INTO tb1 VALUES (%s,%s) ", (e2.get(), t2.get("1.0", END)))
                        con.commit()
                        e2.delete(0, 'end')
                        t2.delete("1.0", END)
                        l4 = Label(r1, text='ADDED SUCESSFULLY :D')
                        l4.place(x=100, y=500)
                else:
                    messagebox.showinfo("EMPTY TITLE!!... YOU HAVE TO GIVE SOME TITLE TO YOUR NOTES")
            except Exception as e:
                messagebox.showinfo("REPEATED NOTES!!..%s NOTES IS ALREADY EXIST. " % (e2.get()))

        b4 = Button(r1, text='ADD', bg='red', width=20, command=ADD_NOTES_DB)
        b4.place(x=200, y=440)

        b5 = Button(r1, text='Exit', bg='red', width=15, command=r1.destroy)
        b5.place(x=380, y=440)


    # function to list all notes
    def LIST_NOTES():
        q3 = 'select note_title from tb1 order by note_title asc'
        rows_count = cursor.execute(q3)
        t1.config(state=NORMAL)
        t4.config(state=NORMAL)
        t1.delete("1.0", END)
        t4.delete("1.0", END)

        if rows_count > 0:
            t4.insert(END, "ALL NOTES-->")
            d = cursor.fetchall()
            for row in d:
                t1.insert(END, row[0] + '\n')

        else:
            messagebox.showinfo("NOTES IS NOT AVAILABLE")
        t1.config(state=DISABLED)

        # function to update notes


    def UPDATES():
        r2 = Toplevel()
        r2.title('UPDATE NOTES')
        r2.geometry('550x550')

        l5 = Label(r2, text='NOTES TITLE')
        l5.place(x=5, y=5)
        e3 = Entry(r2, width=30, font=('times', 15))
        e3.place(x=5, y=25)

        l6 = Label(r2, text='NOTES')
        l6.place(x=5, y=70)

        s3 = Scrollbar(r2)
        s3.place(x=430, y=90)
        t3 = Text(r2, height=20, width=50, yscrollcommand=s3.set)
        s3.config(command=t3.yview)
        t3.place(x=5, y=90)

        def UPDATE_DB():
            rows_count = cursor.execute("UPDATE tb1 SET notes=%s WHERE note_title=%s",(t3.get("1.0", END), e3.get()))
            con.commit()

            if rows_count > 0:
                l7 = Label(r2, text='UPDATE SUCESSFULLY :D', width=50)
                l7.place(x=150, y=480)
            else:
                l7 = Label(r2, text='NO NOTES FOUND %s' % (e3.get()), width=50)
                l7.place(x=150, y=480)

            t3.delete("1.0", END)
            e3.delete(0, 'end')

        b8 = Button(r2, text='Save', width=20, command=UPDATE_DB)
        b8.place(x=150, y=440)

        def VIEW():
            rows_count = cursor.execute("select notes from tb1 where note_title=%s", (e3.get()))
            if rows_count > 0:
                d = cursor.fetchall()
                for row in d:
                    t3.insert(END, row[0])
            else:
                l7 = Label(r2, text='TITLE IS NOT AVAILABLE %s' % (e3.get()), width=50)
                l7.place(x=150, y=480)

        b10 = Button(r2, text='CHANGE FILE',bg='red', command=VIEW)
        b10.place(x=300, y=25)

        b9 = Button(r2, text='Exit', width=15, command=r2.destroy)
        b9.place(x=380, y=440)


    # function to delete notes
    def DELETE():
        r3 = Toplevel()
        r3.geometry('400x150')
        l8 = Label(r3, text="WHICH NOTES WANT TO DELETE!!.. SELECT NOTES:")
        l8.place(x=5, y=5)
        e4 = Entry(r3, width=30, font=('times', 15))
        e4.place(x=5, y=30)

        def DELETE_DB():
            result = messagebox.askokcancel("DELETE NOTES","YOU WANT TO DELETE?")
            if result:
                rows_count = cursor.execute(" DELETE from tb1 WHERE note_title=%s", (e4.get()))
                con.commit()
                if rows_count > 0:
                    messagebox.showinfo("NOTES WITH %s IS DELETED SUCESSFULLY" % (e4.get()))
                else:
                    if (len(e4.get()) != 0):
                        messagebox.showinfo("NO NOTES IS AVAILABLE WITH TITLE %s" % (e4.get()))
                    else:
                        messagebox.showinfo("SORRY!1.. NO NOTES IS DELETED D:")

        def DELETE_ALL_DB():
            result = messagebox.askokcancel("DELETE NOTES", "YOU WANT TO DELETE ALL NOTES?")
            if result:
                rows_count = cursor.execute(" DELETE from tb1 ")
                con.commit()
                if rows_count > 0:
                    messagebox.showinfo("ALL NOTES IS DELETED SUCESSFULLY")
                else:
                    messagebox.showinfo("NO NOTES IS AVAILABLE")

        b9 = Button(r3, text='DELETE', width=17, command=DELETE_DB)
        b9.place(x=20, y=70)

        b11 = Button(r3, text='DELETE All', width=17, command=DELETE_ALL_DB)
        b11.place(x=180, y=70)


    # function to search notes
    def SEARCH_NOTES():
        if (len(e1.get()) == 0):
            messagebox.showinfo("ENTER THE NOTES TO BE SEARCHED:")
        else:
            rows_count = cursor.execute("""SELECT * from tb1 WHERE note_title=%s""", (e1.get()))
            t1.config(state=NORMAL)
            t4.config(state=NORMAL)
            t1.delete('1.0', END)
            t4.delete('1.0', END)
            e1.delete(0, 'end')
            if rows_count > 0:
                d = cursor.fetchall()
                for row in d:
                    t1.insert(END, row[1])
                    if (len(t1.get("1.0", "end-1c")) == 1):
                        messagebox.showinfo(row[0] + " is empty.")
                    else:
                        t4.insert(END, "NOTES TITLE: " + row[0])

            else:
                messagebox.showinfo("SORRY!NO RESULT FOUND")
            t1.config(state=DISABLED)


    #frontend

    #adding new notes
    b1 = Button(root, text='Add New Note>>', height=2, width=30,font=('times', 10, 'bold'))
    b1.config(command=ADD_NOTES)
    b1.place(x=20, y=20)

    #listing all notes
    b2 = Button(root, text='List All Notes>>', height=2, width=30,font=('times', 10, 'bold'), command=LIST_NOTES)
    b2.place(x=320, y=20)

    #updating notes
    b6 = Button(root, text='Update Notes>>', height=2, width=30,font=('times', 10, 'bold'), command=UPDATES)
    b6.place(x=20, y=70)

    #deleting notes
    b7 = Button(root, text='Delete Notes>>', height=2, width=30,font=('times', 10, 'bold'), command=DELETE)
    b7.place(x=320, y=70)

    l1 = Label(root, text='Search Notes', font=('times', 20, 'bold'))
    l1.place(x=20, y=135)

    #searching notes
    large_font = ('times', 15)
    e1 = Entry(root, width=40, font=large_font)
    e1.place(x=20, y=185)

    b3 = Button(root, text='Search', height=1, width=15, font=('times', 10, 'bold'))
    b3.config(command=SEARCH_NOTES)
    b3.place(x=430, y=185)

    l2 = Label(root, text='Notes', font=('times', 15, 'bold'))
    l2.place(x=250, y=250)

    # text box to view heading
    t4 = Text(root, height=2, width=70, state=DISABLED)
    t4.place(x=0, y=280)

    # text box to view notes
    s1 = Scrollbar(root)
    s1.place(x=570, y=320)
    s5 = Scrollbar(root, orient=HORIZONTAL)
    t1 = Text(root, wrap=NONE, height=20, width=70, state=DISABLED, yscrollcommand=s1.set,xscrollcommand=s5.set)
    s1.config(command=t1.yview)
    s5.config(command=t1.xview)
    s5.place(x=0, y=640)
    t1.place(x=0, y=320)

    root.mainloop()



except pm.DatabaseError as e:
    if con:
        con.rollback()
        print("problem", e)
finally:
    cursor.close()
    con.close()
