#Author: John Conrad Seg B. Maisog
from tkinter import *
import tkinter.font as font
import csv

#Defines the dimensions and position of the main window
root = Tk()
root.config(bg="#D5F5E3")
root.title("Student Information System - J.C.S.B.M")
root.resizable(0,0)
root.geometry("500x740")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int((root.winfo_screenwidth()/2 - windowWidth/2))
positionDown = int((root.winfo_screenheight()/2 - windowHeight/2))
root.geometry("+{}+{}".format(positionRight-150, positionDown-300))

#Declares a global list to be used in storing list of students
global listStudents
listStudents = []

#Declares a global image to be used as a default display picture
global image
image = PhotoImage(file="image.png")

#Function for deleting a student. Accepts a parameter pertaining to the id# of the student to be deleted
#Reads the csv file, finds the student with the id# and rewrites the file without the student 
def deleteStudent(number):
        with open('data.csv','r') as csv_file:
                read = csv.DictReader(csv_file)
                listStudents=[]
                for line in read:
                        if line['id#'] != number:
                                listStudents.append(line)
        with open('data.csv','w',newline='') as csv_file:
                fieldnames=["id#","name","course","year","gender"]
                write = csv.DictWriter(csv_file,fieldnames=fieldnames)
                write.writeheader()
                for i in listStudents:
                        write.writerow(i)
        showList(1,2,3)

#Function for displaying the list of students. Trace method, by default, sends in 3 parameters but none of those will be used
def showList(*args):
        #Destroys the current widgets in the frame
        for frame in myFrame.winfo_children():
                frame.destroy()
        #Stores the changes made in the search bar
        searchword = entryvar.get()
        
        with open('data.csv','r') as csv_file:
                read = csv.DictReader(csv_file)
                i=0
                for line in read:
                        #If seachbar is used, filters the list according to the string in the searchbar
                        if(line['id#'].startswith(searchword) or (line['name'].lower()).startswith(searchword.lower())):
                                #Widgets for displaying list of students
                                currFrame = Frame(myFrame, bg="#D5F5E3", highlightbackground="black", highlightthickness=1, height=100, width=470)
                                currFrame.grid(row=i, column=0, padx=5, pady=5)
                                currFrame.propagate(0)

                                picFrame = Label(currFrame, image=image, height=90, width=90, bg="#F4F6F6")
                                picFrame.pack(side=LEFT, padx=(7,0), pady=7)
                                    
                                textFrame = Frame(currFrame, height=90, width=360, bg="#D5F5E3")
                                textFrame.pack(side=LEFT, padx=7, pady=7)
                                textFrame.propagate(0)
                                    
                                info = Label(textFrame, text=" ID#\t: "+line['id#']+
                                                "\nNAME\t: "+line['name']+
                                                "\nCOURSE\t: "+line['course']+
                                                "\nYEAR\t: "+line['year']+
                                                "\nGENDER\t: "+line['gender'],justify=LEFT, bg="#D5F5E3",anchor="w")
                                info.pack(side=LEFT)
                                
                                thisFrame = Frame(textFrame,bg="#D5F5E3")
                                thisFrame.pack(side=RIGHT)
                                #Creates an instance of the line['id#'] variable so that each button will have different values
                                delete = Button(thisFrame, text="Delete", bg="#F4F6F6",width=10, command=lambda x=line['id#']:deleteStudent(x))
                                delete.pack(side=BOTTOM, padx=5,pady=5)
                                edit = Button(thisFrame, text="Update", bg="#F4F6F6", width=10, command=lambda x=line:info_window("edit",x))
                                edit.pack(side=TOP, padx=5,pady=5)
                        i+=1
        #Frame used to fix scrollbar not activating
        fixFrame = Frame(myFrame, height=600, width=470)
        fixFrame.grid(row=i,column=0)
        fixFrame.propagate(0)

#Function for displaying the add and edit window
def info_window(command,student):
        #Function for both adding and editing a student
        #For editing student, saves the current changes to the info, delete the current info and rewrites the file with the new info
        def addStudent():
                student = [ID.get(),name.get(),course.get(),year.get(),gender.get()]
                if command == "edit":
                        deleteStudent(student[0])
                with open('data.csv','a',newline='') as csv_file:
                        write = csv.writer(csv_file)
                        write.writerow(student)
                infoWindow.destroy()
                showList(1,2,3)
        #Creates a new window
        infoWindow = Toplevel()
        infoWindow.configure(bg="#D5F5E3")
        infoWindow.title("Add Student" if command == "add" else "Edit Student")
        infoWindow.resizable(0,0)
        infoWindow.geometry("500x280")
        infoWindow.geometry("+{}+{}".format(positionRight-150, positionDown-150))

        #Widgets for displaying the entry fields
        thisFrame = LabelFrame(infoWindow,bg="#D5F5E3")
        thisFrame.pack(fill="both", expand=True, padx=10, pady=10)

        headFrame = Label(thisFrame, text="Add Student", font=30,bg="#D5F5E3")
        headFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

        Label(thisFrame, text="ID #\t:", anchor=W,bg="#D5F5E3").grid(row=1,column=0, padx=5, pady=5)
        Label(thisFrame, text="Name\t:", anchor=W,bg="#D5F5E3").grid(row=2,column=0, padx=5,pady=5)
        Label(thisFrame, text="Course\t:", anchor=W,bg="#D5F5E3").grid(row=3,column=0, padx=5, pady=5)
        ID = Entry(thisFrame, width=66)
        ID.grid(row=1, column=1, pady=5)
        name = Entry(thisFrame, width=66)
        name.grid(row=2, column=1, pady=7)
        course = Entry(thisFrame, width=66)
        course.grid(row=3, column=1, pady=5)

        thisframe = Frame(thisFrame,bg="#D5F5E3")
        thisframe.grid(row=4, column=0, columnspan=2,pady=5, sticky=W)
        Label(thisframe, text="Year\t:",bg="#D5F5E3").grid(row=0,column=0, padx=5, pady=5)
        Label(thisframe, text="Gender\t:", anchor=E,bg="#D5F5E3").grid(row=0,column=2, padx=5, pady=5)
        year = StringVar()
        year.set("1st year")
        drop = OptionMenu(thisframe, year, "1st year","2nd year","3rd year","4th year","5th year","6th year","7th year")
        drop.grid(row=0, column=1, padx=5,pady=5)
        drop.config(width=18)
        gender = StringVar()
        gender.set("Male")
        Radiobutton(thisframe, text="Male",variable=gender, value="Male",bg="#D5F5E3").grid(row=0, column=4, padx=10,pady=5)
        Radiobutton(thisframe, text="Female",variable=gender, value="Female",bg="#D5F5E3").grid(row=0, column=5, padx=10,pady=5)
        
        #Sets the entry fields with the current student info
        if (command == "edit"):
                ID.insert(0,student['id#'])
                name.insert(0,student['name'])
                course.insert(0,student['course'])
                year.set(student['year'])
                gender.set(student['gender'])
                    
        tempFrame = Frame(thisFrame,bg="#D5F5E3")
        tempFrame.grid(row=5, column=0, columnspan=2)
        cancel = Button(tempFrame, text="Cancel", height=2, width=30, bg="#F4F6F6", command=infoWindow.destroy)
        cancel.grid(row=0,column=0, padx=5, pady=5)
        add = Button(tempFrame, text="Add" if command=="add" else "Save", height=2, width=32, bg="#F4F6F6", command=addStudent)
        add.grid(row=0,column=1, padx=5, pady=5)

#Widgets in the main window                    
header = LabelFrame(root, height=100, width=500, bg="#9FE2BF")
header.propagate(0)
header.grid(row=0, column=0)
Label(header, text="STUDENT INFORMATION SYSTEM", font = 'Helvitica 20 bold', bg="#9FE2BF").place(relx=.5, rely=.4, anchor='c')
Label(header, text="a simple demonstration", font = 'Helvitica 12 italic', bg="#9FE2BF").place(relx=.5, rely=.65, anchor='c')

#Code for a dynamic searchbar
searchFrame = Frame(root)
searchFrame.grid(row=1,column=0,pady=3)
Label(searchFrame, bg="#D5F5E3", text="Search:", anchor=W).grid(row=0, column=0)
#Declares a string variable to contain the current string in the search bar
entryvar = StringVar()      
myentry = Entry(searchFrame, textvariable=entryvar, width = 68)
myentry.grid(row=0, column=1)
#Traces the changes made in the search bar
entryvar.trace('w',showList)

#Code for making a frame with a scrollbar
wrapper = LabelFrame(root, height=350, width=800)
wrapper.grid(row=2, column=0)
mycanvas = Canvas(wrapper, width=475,height=550)
myFrame= Frame(mycanvas, bg="#F4F6F6")
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=myFrame, anchor="nw")

add = Button(root, bg="#F4F6F6", text="Add Student", height=2, width=60, command=lambda:info_window("add",1))
add.grid(row=3, column=0, pady=5)

showList(1,2,3)

root.mainloop()
