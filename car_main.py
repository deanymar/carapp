import pyodbc
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from collections import OrderedDict
import datetime
import os
import base64
from base64 import b64decode
import PyPDF2
root = Tk()
root.geometry("500x500")
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-IBU46V5E\SQLEXPRESS;'
                      'Database=car_info;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
class Car:
    def __init__(self,make,model,modelStartYear,modelEndYear):
        self.make = make
        self.model = model
        self.modelStartYear = modelStartYear
        self.modelEndYear = modelEndYear
class Person:
    def __init__(self,ID,firstName,lastName,password):
        self.ID =ID
        self.firstName =  firstName
        self.lastName = lastName
        self.password = password
class MyCarInfo():
    def __init__(self,licPlate,company,model,modelYear,kilometers,miles,ID):
        self.licPlate = licPlate
        self.company = company
        self.model = model
        self.modelYear = modelYear
        self.kilometers = kilometers
        self.miles = miles
        self.ID = ID

def mainWindow():
    lblName = Label(root, text = "Enter User Name")
    lblPassword = Label(root,text = "Enter Password")
    lblName.grid(row=1,column=1)
    lblPassword.grid(row=2,column =1)
    entryName = Entry(root)
    entryPassword = Entry(root)#,show="*"
    entryName.grid(row=1,column =2)
    entryPassword.grid(row = 2,column=2)
    btnLogin = Button(root,text = "Log In",command = lambda : logIn(entryName.get(),entryPassword.get()))
    btnSignUp = Button(root,text = "Sign Up", command=signUp)
    btnLogin.grid(row =1 , column = 5)
    btnSignUp.grid(row = 2, column =5)
def logIn(userName,userPassword):
    idNameDict = {}
    global p
    lbl = Label(root)
    lbl.grid(row=5,column=1)
    for user in cursor.execute('SELECT * FROM Person WHERE ID like ' + "'{}'".format(userName)):
        p = Person(user[0],user[1],user[2],user[3])
        idNameDict[user[0]] = user[3]
    if idNameDict[userName] == userPassword:
        userPage(root,userName)
    else:
        lbl.config(text= "Invalid Password")
def signUp():
    global signUpWindow
    signUpWindow = newWindow(root)
    ID = Label(signUpWindow,text="ID Number")
    enterID = Entry(signUpWindow)
    enterID.grid(row=1,column=2)
    ID.grid(row=1,column=1)
    firstName = Label(signUpWindow,text ="First Name")
    firstNameEntry= Entry(signUpWindow)
    firstNameEntry.grid(row=2,column=2)
    firstName.grid(row = 2,column =1)
    lastName = Label(signUpWindow,text ="Last Name")
    lastNameEntry = Entry(signUpWindow)
    lastNameEntry.grid(row=3,column=2)
    lastName.grid(row=3,column=1)
    password = Label(signUpWindow,text ="Password")
    passwordEntry = Entry(signUpWindow)
    passwordEntry.grid(row=4,column=2)
    password.grid(row=4,column=1)
    createUser = Button(signUpWindow,text="Sign Up",command= lambda : insertUser(enterID.get(),firstNameEntry.get(),lastNameEntry.get(),passwordEntry.get()))
    createUser.grid(row=5,column= 3)
    nextButton = Button(signUpWindow,text="Next",command=userPage)
    nextButton.grid(row=5,column=4)
    closeWindow(root)
def userPage(window,userName):
    global userWindow
    global listBoxUser
    userWindow = newWindow(root)
    closeWindow(window)
    firstNameLbl = Label(userWindow,text="Hello " + userName + " Today Is : " + datetime.date.today().strftime("%d / %m / %y"))
    firstNameLbl.grid(row=1,column=2)
    addCarButton = Button(userWindow,text="Add New Car",command=lambda : [myCarInfo(1,userName),closeWindow(userWindow)])
    addCarButton.grid(row=5,column=5)
    frame = Frame(userWindow)
    listBoxUser = Listbox(frame)
    frame.grid(row= 3,column=2)
    for i in (myCarList(userName)):
        listBoxUser.insert(END,i)
    listBoxUser.grid(row= 3, column=3)
    listBoxUser.bind("<ButtonRelease-1>",carWindow)

def carWindow(event):
    newCarWindow = newWindow(root)
    closeWindow(userWindow)
    lblInsurace = Label(newCarWindow,text = "Insurance")
    lblInsurace.grid(row=1,column=1)
    buttonUploadInsurance=Button(newCarWindow,text="Upload PDF",command=lambda: getDocument(0))
    buttonUploadInsurance.grid(row = 1,column=2)
    view = Button(newCarWindow,text="View PDF",command=lambda:(viewFile(0)))
    view.grid(row =1,column =3)
    lblRegistration = Label(newCarWindow,text="Registration")
    lblRegistration.grid(row=2,column=1)
    buttonUploadInsurance=Button(newCarWindow,text="Upload PDF",command=lambda: getDocument(1))
    buttonUploadInsurance.grid(row = 2,column=2)
    view = Button(newCarWindow,text="View PDF",command=lambda:(viewFile(1)))
    view.grid(row =2,column =3)
    backButton=Button(newCarWindow,text="Back",command=lambda: userPage(newCarWindow,p.ID))
    backButton.grid(row = 3,column=6)
    deleteCar=Button(newCarWindow,text="Delete Car")
    deleteCar.grid(row = 3,column=5)
def myCarInfo(answer,userName):
    global companyCombo
    global modelCombo
    global modelYearCombo
    myCarInfoWindow = newWindow(root)
    licPlate=Label(myCarInfoWindow,text="License Plate Number")
    licPlate.grid(row=1,column=3)
    licPlateEntry = Entry(myCarInfoWindow)
    licPlateEntry.grid(row=1,column=2)
    companyLbl = Label(myCarInfoWindow,text="Make")
    companyLbl.grid(row=2,column=1)
    companyCombo = ttk.Combobox(myCarInfoWindow,values=carMakeList)
    companyCombo.bind('<<ComboboxSelected>>',makeModels)
    companyCombo.current(0)
    companyCombo.grid(row=3,column=1)
    modelCombo = ttk.Combobox(myCarInfoWindow,values=[])
    modelCombo.bind('<<ComboboxSelected>>',makeYear)
    modelCombo.grid(row=3,column=2)
    modelYearCombo = ttk.Combobox(myCarInfoWindow,values=[])
    modelYearCombo.grid(row=3,column=3)
    kilometers=Label(myCarInfoWindow,text="Kilometers")
    kilometers.grid(row=5,column=1)
    kilometersEntry = Entry(myCarInfoWindow)
    kilometersEntry.grid(row=5,column=2)
    miles=Label(myCarInfoWindow,text="Miles")
    miles.grid(row=6,column=1)
    milesEntry = Entry(myCarInfoWindow)
    milesEntry.grid(row=6,column=2)
    addCarButton = Button(myCarInfoWindow,text="Add Car",command=lambda : [insertMyCarInfo(licPlateEntry.get(),companyCombo.get(),modelCombo.get(),modelYearCombo.get(),kilometersEntry.get(),milesEntry.get(),p.ID),deleteEntry(licPlateEntry,kilometersEntry,milesEntry,licPlateEntry)])
    addCarButton.grid(row=7,column=3)
    backButton = Button(myCarInfoWindow,text="Return",command=lambda : [windowDecide(answer,userName),closeWindow(myCarInfoWindow)])
    backButton.grid(row=7,column=4)
    
def getDocument(answer):
    cs = listBoxUser.curselection()
    licPlate = (listBoxUser.get(cs))
    if answer == 0:
        name= fd.askopenfilename()
        #change it to base64
        with open(name, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        info = [encoded_string,licPlate]
        insertFile = '''
            INSERT INTO checks(insurancePDf,licPlate)
            VALUES(?,?)
        '''
        cursor.execute(insertFile,info)
        conn.commit()
    if answer == 1:
        newFile= fd.askopenfilename()
        #change it to base64
        with open(newFile, "rb") as pdfFile:
            encodedString = base64.b64encode(pdfFile.read())
        newInfo = [encodedString,licPlate]
        updateCheck = '''
            UPDATE checks SET car_registrationPDF =? WHERE licPlate=?
        '''
        cursor.execute(updateCheck,newInfo)
        conn.commit()
def viewFile(answer):
    pdfFile=""
    try:
        if answer == 0:
            for i in (cursor.execute('select insurancePDF from checks where licPlate like ' + str(listBoxUser.get(listBoxUser.curselection())))):
                newFile = (i[0])
                pdfFile = "Insurance"
        elif answer == 1:
            pdfFile = "Car_Registraiton"
            for i in (cursor.execute('select car_registrationPDF from checks where licPlate like ' + "'{}'".format(listBoxUser.get(listBoxUser.curselection())))):
                newFile = (i[0])
        with open(pdfFile + ".pdf", "wb") as pdf:
            pdf.write(base64.b64decode(newFile))
        os.system(pdfFile+ ".pdf")  
    except:
        print("No File exists")
        

    
def insertUser(ID,firstName,lastName,password):
    Person(ID,firstName,lastName,password)
    try:
        newUser = [ID,firstName,lastName,password]
        insertUser = '''
        insert into Person(ID,firstName,lastName,password)
        VALUES(?,?,?,?)
        '''
        cursor.execute(insertUser,newUser)
        myCarInfo()
        closeWindow(signUpWindow)
        conn.commit()
    except:
        lblAlreadyExist = Label(signUpWindow,text="User Already Exists")
        lblAlreadyExist.grid(row=6,column=3)
def insertMyCarInfo(licPlate,company,model,modelYear,kilometers,miles,userID):
    global mci
    mci = MyCarInfo(licPlate,company,model,modelYear,kilometers,miles,userID)
    carInfo = [licPlate,company,model,modelYear,kilometers,miles,userID]
    insertMyCar =  '''
    insert into MyCarInfo(licPlate,company,model,modelYear,kilometers,miles,ID)
    VALUES(?, ?,?,?,?,?,?)
    '''
    cursor.execute(insertMyCar,carInfo)               
    conn.commit()
    
def myCarList(userName):
    licNums = []
    for licNum in (cursor.execute('select licPlate from MyCarInfo where ID like ' + "'{}'".format(userName))):
        licNums.append(licNum[0])
    return licNums


    
def makeModels(event):
    models = []
    for model in (cursor.execute('select model from Car where make like ' + "'{}'".format(companyCombo.get()))):
        models.append(model[0])
    modelCombo.config(values=models)
    modelCombo.current(0)
def makeYear(event):
    years=[]
    endDate = datetime.date.today().year
    for startYear in (cursor.execute('select modelStartYear from Car where model like ' + "'{}'".format(modelCombo.get()))):
        startYear = int(startYear[0])
        for i in range(endDate+1-startYear):
            years.append(startYear+i)
    
    
    modelYearCombo.config(values=years)
    modelYearCombo.current(0)

def newWindow(window):
    newWindow = Toplevel(window)
    newWindow.geometry("500x500")
    return newWindow
def closeWindow(window):
    window.withdraw()           
def deleteEntry(entryOne,entryTwo,entryThree,entryFour):
    entryOne.delete(0,END)
    entryTwo.delete(0,END)
    entryThree.delete(0,END)
    entryFour.delete(0,END)
def windowDecide(answer,userName):
    if answer == 1:
        userPage(root,userName)



carMakeList = []
carModelList = []
allCar = []
for car in (cursor.execute('select * from Car')):
    c=Car(car[0],car[1],car[2],car[3])
    allCar.append(c)
    carMakeList.append(c.make)
    carModelList.append(c.model)
carMakeList = sorted(set(carMakeList))

mainWindow()

#Show PDF
#import os
#url = r"C:\Users\16dea\OneDrive\Desktop\bored\okay.pdf"
#os.startfile(url)









mainloop()