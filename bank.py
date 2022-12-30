#Author: Nick Deupree

#create the log file if it doesnt exist
log = open("logs.dat","a")

# Import necessary modules
from tkinter import *
from tkinter.scrolledtext import *
import sys
import subprocess                                                                                                                                                 
try:
    from cryptography.fernet import Fernet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'cryptography'])            
    log.write("Installed cryptography\n")
try: 
    import customtkinter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'customtkinter'])
    log.write("Installed customtkinter\n")
try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pillow'])
    log.write("Installed pillow\n")
from datetime import date
import os


customtkinter.set_appearance_mode("System")                                               
customtkinter.set_default_color_theme("green")


# Global variables                                                                                             
key = 0

cur_path = os.path.dirname(__file__)

dateFileEmpty = False
allowance = 5
recentChange = 0
day = "Friday"
collapseSwitch = False
balance = 0.00


def load_key():    
# Read the key from the file "key.key"                                                                            
    return open("key.key", "rb").read()

def clearLogs():   
# Clear the contents of the file "logs.dat"                                                                           
    f = open("logs.dat","w")
    f.write("")
    f.close()

def getBalance():  
# Get the balance from the file "bal.dat"
# If the file does not exist, create it
# If the file is empty, set the balance to 0.00                         
    global balance
    if not os.path.exists("bal.dat"):
        f = open("bal.dat", "w")
        f.write(str(balance))
    elif os.stat("bal.dat").st_size == 0:
        f = open("bal.dat", "w")
        f.write(str(balance))
    else:
        f = open("bal.dat", "r")
        balance = float(f.read())
        f.close()
        if os.stat("temp.dat").st_size == 0:
            balance = 0.00

def writeBalance(self):  
# Write the balance to the file "bal.dat"
# Update the balance label in the user interface                                                                                          
    global balance
    f = open("bal.dat", "w")
    f.write(str(balance))
    f.close()
    self.balLabel.configure(text="Balance: $" + str(balance))


def add(key,self,amount : float, date : str, description : str):                               
# Add money to the balance and write it to the file "bank.dat"
# Encrypt the message using a Fernet object
# Update the text widget in the user interface
# Clear the amount and description entries in the user interface
    if(amount == "amount" and description == "description"):
        return
    try:
        float(amount)
    except ValueError:
        global log
        log.write("Value Error\n")
        return
    fer = Fernet(key) 
    global balance
    balance += float(amount)
    message = str(date) + ": Added $" + str(amount) + " | " + description
    message = message.encode()
    encrypted = fer.encrypt(message)
    with open("bank.dat","wb") as f:
        f.write(encrypted)
    updateText(key,self)
    writeBalance(self)
    #clear amount entry and description entry
    self.amountEntryAdd.delete(0,END)
    self.descriptionEntryAdd.delete(0,END)

def delete(key,self,amount : float, date : str, description : str):        
# Subtract money from the balance and write it to the file "bank.dat"
# Encrypt the message using a Fernet object
# Update the text widget in the user interface
# Clear the amount and description entries in the user interface    
    if(amount == "amount" and description == "description"):
        return
    try:
        float(amount)
    except ValueError:
        return
    fer = Fernet(key)
    global balance
    balance -= float(amount)
    message = str(date) + ": Deleted $" + str(amount) + " | " + description
    encrypted = fer.encrypt(message.encode())
    with open("bank.dat","wb") as f:
        f.write(encrypted)
    updateText(key,self)
    writeBalance(self)
    self.amountEntryDel.delete(0,END)
    self.descriptionEntryDel.delete(0,END)

def checkDate(self):                                                                      
    with open("date.dat", "r") as f:
        pastDate = f.read()
        currDate = date.today()
    print(str(pastDate) + " " + str(currDate))
    global log
    dev = False
    global recentChange
    global dateFileEmpty
    if(str(pastDate) != str(currDate) or dev == True or recentChange == 2 or dateFileEmpty == True):
        log.write(str(currDate) + ": Added $"+ str(allowance) + " | Weekly Allowance\n")
        add(key,self,allowance,currDate,"Weekly Allowance")
        recentChange = 1
        with open("date.dat", "w") as f:
            f.write(str(currDate))
        \
        dateFileEmpty = False
    elif(recentChange == 1):
        log.write("Allowance has already been changed today. Not adding money\n")
    else:
        log.write(str(currDate) + ": Same day\n")
    f.close()


def checkFileEmpty():                                                                                       
    global log
    if not os.path.exists("date.dat"):
        f = open("date.dat", "w")
        f.write(str(date.today()))
        f.close()
        log.write("Date file created\n")
    elif os.stat("date.dat").st_size == 0:
        f = open("date.dat", "w")
        f.write(str(date.today()))
        global dateFileEmpty
        dateFileEmpty = True
        f.close()
        log.write("Date file is empty\n")
    else:
        log.write("Date file exists\n")

def checkDay(self):                                                                                        
    today = date.today()
    global log
    currDay = today.strftime("%A")
    if(currDay == day):
        log.write("Allowance Day\n")
        checkFileEmpty()
        checkDate(self)

def updateText(key,self):   
# Read the contents of the file "bank.dat"
# Decrypt the messages using the                                                                                                          
    fer = Fernet(key)  
    with open("bank.dat", "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    decrypted_data = fer.decrypt(encrypted_data)
    self.T.configure(state="normal")
    self.T.insert(customtkinter.END, decrypted_data.decode() + "\n")
    self.T.yview(customtkinter.END)
    self.T.configure(state="disabled")

def onClosing(self):  
    #writes the history to the temp.dat file and the balance to the bal.dat file                                                                       
    fer = Fernet(load_key())
    with open("temp.dat", "wb") as f:
        message = self.T.get("1.0",customtkinter.END)
        message = message[:-1]
        encrypted = fer.encrypt(message.encode())
        f.write(encrypted)
    with open("bal.dat", "w") as f:
        f.write(str(balance))
    global log
    log.close()  

def fillText(key,self):
    #fills the text widget with the history from the temp.dat file                                                                         
    if(os.stat("temp.dat").st_size != 0):
        fer = Fernet(key)
        with open("temp.dat", "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        decrypted_data = fer.decrypt(encrypted_data)
        self.T.insert(customtkinter.END, decrypted_data.decode())
        self.T.yview(customtkinter.END)
    with open("temp.dat", "w") as f:
        f.write("")


def createFiles():
    #creates the necessary files
    if not os.path.exists("temp.dat"):
        f = open("temp.dat", "w")
        f.close()
    if not os.path.exists("bank.dat"):
        f = open("bank.dat", "w")
        f.close()
    if not os.path.exists("bal.dat"):
        f = open("bal.dat", "w")
        f.close()
    if not os.path.exists("key.key"):
        f = open("key.key", "w")
        f.close()        

class App(customtkinter.CTk):   
# Main window                                                                                        
    def __init__(self):
    # Set up the user interface
    # Create necessary files
    # Read the key from the file "key.key"
    # Clear the contents of the file "logs.dat"
    # Get the balance from the file "bal.dat"
    # Set the title of the window
    # Set up the sidebar
    # Set up the sidebar collapse button
    # Set up the allowance amount entry and button
    # Set up the allowance day of the week dropdown menu
    # Set up the appearance mode dropdown menu
    # Set up the clear files button
    # Set up the text widget
    # Set up the balance label
    # Set up the add money entry and button
    # Set up the delete money entry and button
    # Set up the quit button
        super().__init__()
        createFiles()
        global key                                                                                                           
        if os.stat("key.key").st_size == 0:                                                 
            key = Fernet.generate_key()
            with open("key.key","wb") as key_file:
                key_file.write(key)
        else:
            key = load_key()

        clearLogs()
        getBalance()
        self.title("Bank")

        #sidebar
        self.sidebar = customtkinter.CTkFrame(master=self,width=140,corner_radius=0)
        self.sidebar.grid(column=0,row=0,rowspan=12,sticky="nsew")
        #self.sidebar.grid_rowconfigure(9,weight=1)
        self.sidebar.configure(fg_color=("gray80","gray17"))

        light_img = Image.open(os.path.join(cur_path, 'Icons', 'crossLight.png'))
        dark_img = Image.open(os.path.join(cur_path, 'Icons', 'crossDark.png'))
        self.sidebarCollapse = customtkinter.CTkButton(master=self.sidebar,
                                                image=customtkinter.CTkImage(light_image=light_img,dark_image=dark_img,size=(10,10)),
                                                text="",
                                                width =10,
                                                height=10,
                                                command= self.sidebarCollapseCommand
                                                )
        self.sidebarCollapse.grid(column=0,row=0,sticky="w")
        
        
        self.allowanceAmountEntryLabel = customtkinter.CTkLabel(master=self.sidebar,text="Allowance Amount")
        self.allowanceAmountEntryLabel.grid(column=0,row=3,padx=10,pady=10)
        self.allowanceAmountEntry = customtkinter.CTkEntry(master=self.sidebar,placeholder_text = "allowance amount")
        self.allowanceAmountEntry.grid(column=0,row=4,padx=10)
        self.allowanceAmountButton = customtkinter.CTkButton(master=self.sidebar,text="Change Amount",command=self.allowanceAmountButtonCommand)
        self.allowanceAmountButton.grid(column=0,row=5,padx=10,pady=10)

        self.allowanceDayOfTheWeekLabel = customtkinter.CTkLabel(master=self.sidebar,text="Allowance Day of the Week")
        self.allowanceDayOfTheWeekLabel.grid(column=0,row=6,padx=10,pady=10)
        self.allowanceDayOfTheWeekOption = customtkinter.CTkOptionMenu(master=self.sidebar,
                                                                        values=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                                                                        command=self.allowanceDayOfTheWeekDropDownCommand
                                                                        )
        self.allowanceDayOfTheWeekOption.set("Friday")
        self.allowanceDayOfTheWeekOption.grid(column=0,row=7,padx=10)


        self.modeLabel = customtkinter.CTkLabel(master=self.sidebar,text="Appearance Mode")
        self.modeLabel.grid(column=0,row=8,padx=10,pady=10)
        self.modeOption = customtkinter.CTkOptionMenu(master=self.sidebar,
                                                                        values=["Light","Dark","System"],
                                                                        command=self.modeDropDownCommand
                                                                        )
        self.modeOption.set("System")
        self.modeOption.grid(column=0,row=9,padx=10)

        #button to clear files and update the balance and text box
        self.clearButton = customtkinter.CTkButton(master=self.sidebar,text="Clear Files",command=self.clearButtonCommand)
        self.clearButton.grid(column=0,row=12,padx=10,pady=30)


        #sidebar that will hold the balance label, date label, and text box label
        self.sidebar2 = customtkinter.CTkFrame(master=self,width=140,corner_radius=0)
        self.sidebar2.grid(column=1,row=0,rowspan=1,columnspan=3,sticky="nsew")
        self.sidebar2.configure(fg_color=("gray80","gray17"))

        #Balance Label
        global balance
        self.balLabel = customtkinter.CTkLabel(self.sidebar2, text="Balance: $" + str(balance))
        self.balLabel.grid(column=3, row=1)
        self.balLabel.configure(font=("Arial", 14))
        #add padding
        self.balLabel.grid(padx=10,pady=10)

        #date label
        self.dateLabel = customtkinter.CTkLabel(self.sidebar2, text="Date: " + str(date.today()))
        self.dateLabel.grid(column=4, row=1, sticky="e")    
        self.dateLabel.configure(font=("Arial", 14))
        #add padding
        self.dateLabel.grid(padx=10,pady=10)

        #text box label
        self.TLabel = customtkinter.CTkLabel(self.sidebar2, text="Transactions")
        self.TLabel.grid(column=1, row=1, sticky="w")
        self.TLabel.configure(font=("Arial", 20))
        #add padding
        self.TLabel.grid(padx=100)

        #text box
        self.T = customtkinter.CTkTextbox(master=self, height=300, width=300,wrap="word")
        fillText(key,self)
        self.T.grid(column = 1, row = 3)
        self.T.configure(state="disabled")
        self.T.configure(font=("Arial", 20))
        
        #frame where the add and delete buttons will be
        self.addDeleteFrame = customtkinter.CTkFrame(master=self,width=140,corner_radius=0)
        self.addDeleteFrame.grid(column=1,row=5,rowspan=1,columnspan=1,sticky="nsew")
        self.addDeleteFrame.configure(fg_color=("gray93","gray14"))
        
        #add button
        self.amountEntryAdd = customtkinter.CTkEntry(master=self,placeholder_text = "amount")
        self.descriptionEntryAdd = customtkinter.CTkEntry(master=self,placeholder_text="description")
        self.amountEntryAdd.grid(column=2, row=5,rowspan=2)
        self.descriptionEntryAdd.grid(column = 3, row = 5,rowspan=2)
        self.addButton = customtkinter.CTkButton(master=self.addDeleteFrame,text="Add", command=lambda: add(key,self,self.amountEntryAdd.get(), date.today(), self.descriptionEntryAdd.get()))
        self.addButton.grid(column = 1, row = 5,sticky="w",padx = 5)
        #add padding
        self.addButton.grid(padx=10,pady=5)
        self.amountEntryAdd.grid(padx=10,pady=5)
        
        

        #remove button
        self.delButton = customtkinter.CTkButton(master=self.addDeleteFrame,text="Delete", command=lambda: delete(key,self,self.amountEntryAdd.get(), date.today(), self.descriptionEntryAdd.get()))
        self.delButton.grid(column = 2, row = 5 ,sticky="e")
        #add padding
        self.delButton.grid(padx=10,pady=10)
        self.delButton.configure(fg_color=("red"))
        self.delButton.configure(hover_color=("#8b0000"))

        checkDay(self)
        self.protocol("WM_DELETE_WINDOW",lambda: (onClosing(self),self.destroy()))
        #window.attributes( "-fullscreen", True)
        self.grid_columnconfigure(0, weight=1)
    

    def sidebarCollapseCommand(self):  
    # Collapse the sidebar by hiding it and showing the sidebar collapse button                                 
        global collapseSwitch
        if(collapseSwitch == False):
            light_img = Image.open(os.path.join(cur_path,'Icons','burgerLight.png'))
            dark_img = Image.open(os.path.join(cur_path,'Icons','burgerDark.png'))
            self.sidebarCollapse.configure(image=customtkinter.CTkImage(light_image=light_img,dark_image=dark_img,size=(10,10)))
            self.allowanceAmountEntryLabel.grid_forget()
            self.allowanceAmountEntry.grid_forget()
            self.allowanceDayOfTheWeekLabel.grid_forget()
            self.allowanceDayOfTheWeekOption.grid_forget()
            self.modeLabel.grid_forget()
            self.modeOption.grid_forget()
            self.allowanceAmountButton.grid_forget()
            self.clearButton.grid_forget()
            collapseSwitch = True
        else:
            light_img = Image.open(os.path.join(cur_path, 'Icons', 'crossLight.png'))
            dark_img = Image.open(os.path.join(cur_path, 'Icons', 'crossDark.png'))
            self.sidebarCollapse.configure(image=customtkinter.CTkImage(light_image=light_img,dark_image=dark_img,size=(10,10)))
            self.allowanceAmountEntryLabel.grid(column=0,row=3,padx=10,pady=10)
            self.allowanceAmountEntry.grid(column=0,row=4,padx=10)
            self.allowanceAmountButton.grid(column=0,row=5,padx=10,pady=10)
            self.allowanceDayOfTheWeekLabel.grid(column=0,row=6,padx=10,pady=10)
            self.allowanceDayOfTheWeekOption.grid(column=0,row=7,padx=10)
            self.modeLabel.grid(column=0,row=8,padx=10,pady=10)
            self.modeOption.grid(column=0,row=9,padx=10)
            self.clearButton.grid(column=0,row=12,padx=10,pady=30)
            collapseSwitch = False

    
    def allowanceDayOfTheWeekDropDownCommand(self,currDay):
    # Update the allowance day of the week with the selected value in the allowance day of the week dropdown menu
        global day
        day = currDay
        global recentChange
        print(recentChange)
        recentChange = 2 if recentChange == 0 else 1
        checkDay(self)

    def modeDropDownCommand(self,mode : str):
    # Update the appearance mode with the selected value in the appearance mode dropdown menu
        customtkinter.set_appearance_mode(mode)
    
    def allowanceAmountButtonCommand(self):
    # Update the allowance amount with the value entered in the allowance amount entry
        global allowance
        allowance = self.allowanceAmountEntry.get()
    
    def clearButtonCommand(self):
    # Clear the contents of the files
        with open("bal.dat", "w") as f:
            f.write("")
        with open("bank.dat", "w") as f:
            f.write("")
        with open("temp.dat", "w") as f:
            f.write("")
        with open("date.dat", "w") as f:
            f.write("")
        self.T.configure(state="normal")
        self.T.delete("1.0", "end")
        self.T.configure(state="disabled")
        self.balLabel.configure(text="Balance: $0")
        global balance
        balance = 0
        
    
if __name__ == '__main__':
    app = App()
    app.resizable(False, False)
    app.mainloop()