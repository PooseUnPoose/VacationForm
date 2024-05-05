from reportlab.pdfgen import canvas
import PyPDF2 as PyPDF
from os import remove
from datetime import date
import tkinter as tk
from tkcalendar import DateEntry


def CreateTextOverlay(TextEntries,ImageEntries, OutputFilename):
    c = canvas.Canvas(OutputFilename)
    for text, x, y in TextEntries:
        c.drawString(x, y, text)
    for image_path, x, y, width, height in ImageEntries:
        c.drawImage(image_path, x, y, width, height)
    c.save()


def MergePdfs(BasePdfPath, OverlayPdfPath, OutputPdfPath):
    BasePdf = open(BasePdfPath, "rb")
    Reader = PyPDF.PdfReader(BasePdf)
    Writer = PyPDF.PdfWriter()
    OverlayPdf = open(OverlayPdfPath, "rb")
    OverlayReader = PyPDF.PdfReader(OverlayPdf)
    Page = Reader.pages[0]
    Page.merge_page(OverlayReader.pages[0])
    Writer.add_page(Page)
    with open(OutputPdfPath, "wb") as OutputPdf:
        Writer.write(OutputPdf)
    BasePdf.close()
    OverlayPdf.close()


def CreateNewFile(FirstDayVacation, LastDayVacation, WorkShiftsRequested):
    #Fill in the coordingates of each section and fill in the required information
    TextEntries = [
        ("insert Name here", 105, 680),         #Name
        ("Insert ID here", 320, 680),           #Employee ID
        ("x", 510, 681),                        #PT/FT
        ("site name here", 100, 655),           #Site name
        ("site here", 320,655),                 #Site Number
        (str(date.today()), 450, 655),          #Date
        ("x", 178, 633 ),                       #Reporting Office Location
        (FirstDayVacation, 262, 612 ),          #1st day Vacation 
        (LastDayVacation, 462, 612),            #last day Vacation 
        (WorkShiftsRequested, 350 ,593),        # of work shifts requested  
    ]
    ImageEntries = [
        ("Resources/Signature.png", 350, 513, 202, 36)
    ]
    TextOverlayPdf = "TextOverlay.pdf"
    CreateTextOverlay(TextEntries,ImageEntries, TextOverlayPdf)
    MergePdfs("Resources/BlankForm.pdf", TextOverlayPdf, "OutputtedFiles/FormName + your name "+str(date.today()) + ".pdf")
    remove(TextOverlayPdf)
    print("Job Done.")



##
## GUI
##
window = tk.Tk()
window.title("Blank Window")
window.geometry("400x300")

label1 = tk.Label(window, text="1st day of vacation", justify="center")
label2 = tk.Label(window, text="Last day of vacation", justify="center")
label3 = tk.Label(window, text="Work Shifts Requested", justify="center")
textbox1 = DateEntry(window)
textbox2 = DateEntry(window)
textbox3 = tk.Entry(window)

label1.pack()
textbox1.pack()
label2.pack()
textbox2.pack()
label3.pack()
textbox3.pack()

button = tk.Button(window, text="Submit")
button.pack(pady=10)
button.pack()

def SubmitButtonClicked():
    FirstDayVacation = textbox1.get()
    LastDayVacation = textbox2.get()
    WorkShiftsRequested = textbox3.get()
    CreateNewFile(FirstDayVacation, LastDayVacation, WorkShiftsRequested)
button.config(command=SubmitButtonClicked)

window.mainloop()
#==========================================================================#
