from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
from datetime import datetime as dt
import datetime
import subprocess
import sqlite3
from fpdf import FPDF
import os

# Get current working directory
cwd = os.getcwd()

# Get current year and month
date=datetime.date.today()
dateformat=date.strftime("%d-%m-%Y")
current_date=date.strftime("%d")
current_year = dt.now().year
current_month = dt.now().month

# Define the directory structure
year_folder = os.path.join(cwd, str(current_year))
month_folder = os.path.join(year_folder, str(current_month))
date_folder = os.path.join(month_folder, str(current_date))
# Create the year folder if it doesn't exist
if not os.path.exists(year_folder):
    os.mkdir(year_folder)

# Create the month folder if it doesn't exist
if not os.path.exists(month_folder):
    os.mkdir(month_folder)
if not os.path.exists(date_folder):
    os.mkdir(date_folder)

#Lists
# totaltestlist=["TLC", "NEUTROPHIL", "LYMPHOCYTE", "EOSINOPHIL", "MONOCYTE", "BASOPHIL", "RBC", "HEMOGLOBIN"
#                ,"HCT","MCV", "MCH", "MCHC", "PLATELET","Blood Sugar(Random)","Blood Sugar(Fasting)",
#                "Blood Sugar(PP)","SGPT","SGOT","ALKALINE PHOSPHATASE","TOTAL PROTEIN","ALBUMIN","GLOBULIN",
#                "A/G RATIO","TOTAL BILIRUBIN","DIRECT BILIRUBIN","INDIRECT BILIRUBIN","UREA","URIC ACID", "CREATININE",
#                "SODIUM","POTASSIUM","CHLORIDE","TOTAL CHOLESTEROL","HDL","LDL","VLDL","TRIGLYCERIDE","BT","CT",
#                "HBSAG","HIV","HCV","ABO","RH","WIDAL","CRP","RA FACTOR","ASO","ESR"]
# normalrangelist=["4,000-11,000Cells/ul","50-70%","20-50%","02-15%","2-8%","0-1%","3.56-6.5 millions/ul","Women=12.5-15.5 g/dl,Men=13-16 g/dl","35-55 %","80-100 fl","28-35 pg",
#                  "32-36 g/dl","1.5-4.5lacs/ul","70-140 mg/dl","70-110 mg/dl","Less than 140 mg/dl","UPTO 40 U/L","UPTO 35 IU/ML","25-140 U/L","6.2-8.0 G/DL","3.8-5.4 G/DL",
#                  "1.5-3.6G/DL","1-2.3","0-1 MG/DL","0-0.3 MG/DL","0.2-1 MG/DL","15-45 MG/DL","MALE-3.4-7, FEMALE- 2.5-6 MG/DL", "MALE-0.7-1.3, FEMALE-0.5-1.2 MG/DL"
#                  ,"135-155 MMOL/L","3.5-5.5 MEQ/L","98-104 MEQ/L","109-202 MG/DL","35-79.5 MG/DL"
#                  ,"10-60 MG/DL","2-30 MG/DL","50-165 MG/DL","1-4 min","2-8 min",".",".",".",".",".",".","0-6 mg/dl","0-30 IU/ML",".","0-20mm"]
# totaltestliststr=""
# for i in totaltestlist:
#     totaltestliststr+=","+i
# normalrangeliststr=""
# for i in normalrangelist:
#     normalrangeliststr+=","+i
# ft=open("totaltestlist.txt","w")
# ft.write(totaltestliststr)
ft=open("totaltestlist.txt","r")
datat=ft.read()
# fnr=open("normalrangelist.txt","w")
# fnr.write(normalrangeliststr)
fnr=open("normalrangelist.txt","r")
datanr=fnr.read()
totaltestlist=datat.split(",")
normalrangelist=datanr.split(",")
ft.close()
fnr.close()
# MainWindow Structure
root = Tk()
root.title("VeraPath 1.0")

con=sqlite3.connect("namedatedata.db")
c=con.cursor()
c.execute("CREATE TABLE if not exists namedate (name text ,date text)")
con.commit()
con.close()

def addtest():
    def submitnewtest():
        ft=open("totaltestlist.txt","r+")
        ft.read()
        ft.write(","+addtestname.get())
        fnr=open("normalrangelist.txt","r+")
        fnr.read()
        fnr.write(","+addtestnr.get())
        ft.close()
        fnr.close()
    addtestwindow=Toplevel()
    addtestwindow.title("Add Test")
    Label(addtestwindow,text="Name: ").grid(row=0,column=0)
    Label(addtestwindow,text="Normal Range: ").grid(row=1,column=0)
    addtestname=Entry(addtestwindow,width=50,border=5)
    addtestname.grid(row=0,column=1)
    addtestnr=Entry(addtestwindow,width=50,border=5)
    addtestnr.grid(row=1,column=1)
    Button(addtestwindow,text="Submit",command=submitnewtest).grid(row=2,column=0)
def search():
    searchwindow=Toplevel()
    searchwindow.title("Search by Name")
    def startsearch():
        searchnameentryvalue=searchnameentry.get()
        con=sqlite3.connect("namedatedata.db")
        c=con.cursor()
        c.execute("SELECT *,name FROM namedate WHERE name=:name",{"name":searchnameentryvalue})
        global records
        records=c.fetchall()
        record1=str()
        for record in records:
            record1 += str(record[0]) +"\t"+str(record[1])+ "\n"
        queerylabel = Label(searchwindow, text=record1)
        queerylabel.grid(row=2,column=0,columnspan=2)

    Label(searchwindow,text="Enter Name: ").grid(row=0,column=0)
    searchnameentry=Entry(searchwindow,width=30,border=5)
    searchnameentry.grid(row=0,column=1)
    Button(searchwindow,text="Start search",command=startsearch).grid(row=1,column=0,columnspan=2,sticky=NSEW)
    
global patientframe
patientframe = LabelFrame(root, text="Patient Information", padx=10, pady=10)
# patientframe.grid(row=1, column=0,columnspan=10)
patientframe.pack(fill=BOTH,expand=1)
Label(patientframe,text="Date: ",padx=5,pady=5).grid(row=0,column=4)
Label(patientframe,text="Patient Name: ",padx=5,pady=5).grid(row=0,column=0)
Label(patientframe,text="Age: ",padx=5,pady=5).grid(row=0,column=2)
Label(patientframe,text="Gender: ",padx=5,pady=5).grid(row=1,column=0)
Label(patientframe,text="Dr. Name: ",padx=5,pady=5).grid(row=1,column=2)
dateentry=Entry(patientframe,width=20,border=5)
dateentry.grid(row=0,column=5)
dateentry.insert(0,dateformat)

nameentry=Entry(patientframe,width=20,border=5)
nameentry.grid(row=0,column=1)
ageentry=Entry(patientframe,width=20,border=5)
ageentry.grid(row=0,column=3)
gendervar=StringVar(patientframe)
gendervar.set("Male")
genderentry=OptionMenu(patientframe,gendervar,"Male","Female")
genderentry.grid(row=1,column=1)
drnameentry=Entry(patientframe,width=40,border=5)
drnameentry.insert(0,"Dr (Major) Ratish Kumar (Ortho)")
drnameentry.grid(row=1,column=3)

def generate():
    selectedtestindices=[]
    selectedtests=[]
    selectednr=[]
    resultwindow=Toplevel()
    resultwindow.title("Result Entry")

    ptinformationframe = LabelFrame(resultwindow, text="Patient Information", padx=10, pady=10)
    ptinformationframe.pack(fill=BOTH,expand=1)
    resultframe=LabelFrame(resultwindow,text="Result")
    resultframe.pack(fill=BOTH,expand=1)
    canvas=Canvas(resultframe,width=800)
    canvas.grid(row=0,column=0,sticky=NSEW)
    scrollbar=ttk.Scrollbar(resultframe,orient=VERTICAL,command=canvas.yview)
    scrollbar.grid(row=0,column=4,sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    secondframe=Frame(canvas)
    canvas.create_window((0,0),window=secondframe,width=800,anchor="nw")
    Label(ptinformationframe,text="Patient Name: ").grid(row=0,column=0)
    Label(ptinformationframe,text=nameentry.get()).grid(row=0,column=1)
    Label(ptinformationframe,text="Age: ").grid(row=1,column=0)
    Label(ptinformationframe,text=ageentry.get()).grid(row=1,column=1)
    Label(ptinformationframe,text="Gender: ").grid(row=1,column=2)
    Label(ptinformationframe,text=gendervar.get()).grid(row=1,column=3)
    Label(ptinformationframe,text="Date: ").grid(row=0,column=4)
    Label(ptinformationframe,text=dateentry.get()).grid(row=0,column=5)
    Label(ptinformationframe,text="Dr Name: ").grid(row=1,column=4)
    Label(ptinformationframe,text=drnameentry.get()).grid(row=1,column=5)
    Label(secondframe,text="Tests").grid(row=0,column=0,sticky="w")
    Label(secondframe,text="Result").grid(row=0,column=1,sticky="w")
    Label(secondframe,text="Normal Range").grid(row=0,column=2,sticky="w")
    

    for i, var in enumerate(testvars):
        if var.get() == "on":
            selectedtestindices.append(i)
    for i in selectedtestindices:
        selectedtests.append(totaltestlist[i])
        selectednr.append(normalrangelist[i])
    results=[]
    for i in range(len(selectedtests)):
        resultvar=StringVar()
        Label(secondframe,text=selectedtests[i]).grid(row=i+1,column=0,sticky="w")
        Label(secondframe,text=selectednr[i]).grid(row=i+1,column=2,columnspan=2,sticky="w")
        e=Entry(secondframe,textvariable=resultvar)
        e.grid(row=i+1,column=1,sticky="w")
        results.append(resultvar)
    
    dateentryvalue = dateentry.get()
    file_name = nameentry.get()
    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica',style='B',size=13)
            self.cell(0,40,"",border=False,ln=1)
            self.cell(180,10,"","BU",ln=1)
            self.cell(20,10,"Name: ","B")
            self.cell(80,10,file_name,"B")
            self.cell(10,10,"Age: ","B")
            self.cell(30,10,ageentry.get(),"B")
            self.cell(20,10,"Gender: ","B")
            self.cell(20,10,gendervar.get(),"B",ln=1)
            self.cell(30,10,"Referred by : ","B")
            self.cell(80,10,drnameentry.get(),"B")
            self.cell(40,10,"Reporting Date: ","B")
            self.cell(30,10,dateentryvalue,"B",ln=1)

            self.set_font('helvetica','', 12)
            self.cell(80,10,"","",ln=1)
            self.cell(70,10,"Tests","BU")
            self.cell(20,10,"Result","BU")
            self.cell(90,10,"Normal Range","BU",ln = True)
    def submittopdf():
        # save into db
        con=sqlite3.connect("namedatedata.db")
        c=con.cursor()
        c.execute("INSERT INTO namedate VALUES (:name,:date)",{"name": file_name,"date":dateentryvalue})
        con.commit()
        con.close()

        pdf=PDF('p','mm',"A4")
        pdf.add_page()
        pdf.set_font('helvetica','', 13)
        pdf.set_auto_page_break(auto=True,margin=50)
        
        for i in range(len(selectedtests)):
            pdf.cell(70,10,selectedtests[i])
            pdf.cell(20,10,results[i].get())
            pdf.cell(90,10,selectednr[i],ln=True)
        if os.path.exists(os.path.join(date_folder, f"{file_name}.pdf")):
            old_path=os.path.join(f"{date_folder}",f"{file_name}.pdf")
            for i in range(1000):
                if not os.path.exists(os.path.join(date_folder, f"{file_name}{i}.pdf")):
                    new_path=os.path.join(f"{date_folder}",f"{file_name}{i}.pdf")
                else:
                    new_path=os.path.join(f"{date_folder}",f"{file_name}{i+1}.pdf")
            os.rename(old_path,new_path)
            pdf.output(os.path.join(date_folder, f"{file_name}.pdf"))
        else:
            pdf.output(os.path.join(date_folder, f"{file_name}.pdf"))

        filepath=date_folder
        os.startfile(filepath)
    b=Button(resultframe,text="Submit",command=submittopdf)
    b.grid(row=200,column=0)
    
    resultwindow.mainloop()

testvars=[]
testframe=LabelFrame(root,text="Result")
testframe.pack(fill=BOTH,expand=1)
canvas=Canvas(testframe,width=1300)
canvas.grid(row=0,column=0,sticky=NSEW)
scrollbar=ttk.Scrollbar(testframe,orient=HORIZONTAL,command=canvas.xview)
scrollbar.grid(row=11,column=0,sticky="we")
canvas.configure(xscrollcommand=scrollbar.set)
canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
thirdframe=Frame(canvas)
canvas.create_window((0,0),window=thirdframe,width=1300,anchor="nw")
for i in range(10):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=2,column=i,sticky=W)
    testvars.append(testvar)
for i in range(10,13):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=3,column=i-10,sticky=W)
    testvars.append(testvar)
for i in range(13,16):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=4,column=i-13,sticky=W)
    testvars.append(testvar)
for i in range(16,26):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=5,column=i-16,sticky=W)
    testvars.append(testvar)
for i in range(26,32):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=6,column=i-26,sticky=W)
    testvars.append(testvar)
for i in range(32,37):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=7,column=i-32,sticky=W)
    testvars.append(testvar)
for i in range(37,39):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=8,column=i-37,sticky=W)
    testvars.append(testvar)
for i in range(39,42):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=8,column=i-39,sticky=W)
    testvars.append(testvar)
for i in range(42,44):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=9,column=i-42,sticky=W)
    testvars.append(testvar)
for i in range(44,len(totaltestlist)):
    testvar = StringVar(value="off")
    c=Checkbutton(thirdframe,text=totaltestlist[i],variable=testvar,onvalue="on",offvalue="off")
    c.grid(row=10,column=i-44,sticky=W)
    testvars.append(testvar)
generatebtn=Button(root,text="Generate",command=generate)
generatebtn.pack()


# menu
mymenu=Menu(root)
root.config(menu=mymenu)
treemenu=Menu(mymenu)
mymenu.add_cascade(menu=treemenu,label="File")
treemenu.add_command(label="Search",command=search)
treemenu.add_command(label="Add Test",command=addtest)

root.mainloop()
