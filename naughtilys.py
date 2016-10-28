#!/usr/bin/env python
#AUTHOR: Samuel MacDonald
#PURPOSE: Very Minimalist Word Processor for NaNoWriMo and the like
#Not associated with Nautilus or ILYS or NaNoWriMo or anything else remotely reputable
#KNOWN ISSUES:
    #Doesn't work in IDLE
    #Wordcount is dodgy
    #Catching non-printable inputs is probably dodgy
#TO DO:
    #Neaten up presentation so its more consistent with screen clearing etc
    #Catch errors for autosaves
    #Make it cross platform
    #Tidy code, dear god looking at this even a day later hurts me
    #Fix function names

#*****IMPORTS*****
import msvcrt,os,sys,time #MS specific tools to get character and clear screen. Will need jimmying if you want other OSes


#*****INITIALISE GLOBAL VARS*****
output = projectname = ""
wordcount = targetwordcount = lastchar = 0


def gettargetwordcount(): #try catch to make sure the wordcount is a valid integer
    global targetwordcount
    userinput = input("Desired word count? ")
    try:
        targetwordcount = int(userinput)
        os.system('cls') #clear screen
        getprojectname()
    except ValueError:
        os.system('cls') #clear screen
        print("That wasn't a number I understand sorry.")
        gettargetwordcount()
    except KeyboardInterrupt: #catch any -Ctrl+C inputs neatly
        sys.exit()

def getprojectname(): #try catch to ensure valid output file
    global projectname, targetwordcount
    os.system('cls') #clear screen
    print("Welcome to Naughtilys - Press Ctrl+C or ESC to quit early.")
    projectname = input("Project Title? ")
    try: #trycatch to ensure can read the entered projectname
        f = open(projectname + ".txt", 'r')
        try:
            first = f.readline
            ()
            for last in f: pass
            print("Your last line was: '" + last + "'. Now type.\n" + str(targetwordcount))
        except UnboundLocalError:
                print("Nothing at " + projectname + ".txt. Get Typing \n" + str(targetwordcount))
    except IOError: #if it doesn't already exist...
        try:
            f = open(projectname + ".txt", 'w') #create it
            os.system('cls') #clear screen
            print ("New Project " + projectname + ".txt created. Now type.\n" + str(targetwordcount))
        except IOError: #if that fails too, ask for a new name
            os.system('cls') #clear screen
            print ("Couldn't find or create " + projectname + ".txt. Try another.")
            getprojectname()
        
def endloop(): #function called to close the program under normal circumstances
    global wordcount, projectname
    print (output) #print what you've gotten so far
    if lastchar == 1: #if lastchar wasn't blank
        wordcount = wordcount+1#add the word they were working on
    print ("Finished. Session word count (spaces and newlines): " + str(wordcount)) #output estimated wordcount
    with open(projectname + ".txt", 'a+') as outfile: 
        outfile.write(output) #open file named test.txt in append mode
    quitter()

def quitter():
    global projectname
    input("Check that you can see " + projectname + ".txt before pressing Enter to close")
    sys.exit()
        
def autosave():
    global wordcount, projectname
    if wordcount % 50 == 0: #every 50 words
        os.system('cls') #clear screen
        print ("***AUTOSAVE***\n" + str(targetwordcount - wordcount)) #output estimated wordcount
        with open(projectname + ".bak", 'a+') as outfile: 
            outfile.write(output) #open file named test.txt in append mode
    if wordcount % 500 == 0: #every 500 words
        os.system('cls') #clear screen
        print ("***BACKUP CREATED***\n" + str(targetwordcount - wordcount)) #output estimated wordcount
        with open(projectname + time.strftime('%Y%m%d%H%M') + ".bak", 'a+') as outfile: 
            outfile.write(output) #open file named test.txt in append mode
                

#ACTUAL START OF PROGRAM HERE
os.system('cls') #clear screen
print("Welcome to Naughtilys - Press Ctrl+C or ESC to quit early.")
try:
    gettargetwordcount()
except KeyboardInterrupt: #catch any -Ctrl+C inputs neatly
    input("Press Enter to quit")
    sys.exit()

while msvcrt.kbhit: #main loop - whenever there's something in the keyboard buffer
    try:
        char = msvcrt.getch().decode('UTF-8') #get any character input as a raw byte and then convert it as UTF-8 to be readable
        os.system('cls') #clear screen
        if char == chr(27): #if it sees escape
            endloop()
            break
        elif char == chr(32): #if it sees a space
            if lastchar == 1: #make sure lastchar wasn't blank
                output = output+char #concatenate the space
                lastchar = 0 #mark lastchar as being blank
            print ("") #print a blank line
            
        elif char == chr(13): #if it sees carriage return 
            if lastchar == 1: #make sure lastchar wasn't blank
                output = output+char+'\n' #catch carriage returns as newlines for formatting's sake
                lastchar = 0 #mark lastchar as being blank
            print ("") #print a blank line
            
        else: #if it wasn't space, return or esc:
            lastchar = 1 #set lastchar to not blank
            output = output+char #concatenate this character to output string
            print (char), #otherwise print it
        #get wordcount:
        wordcount = output.count(' ') + output.count('\n') #count the spaces and carriage returns
        if wordcount >= targetwordcount: #breakout if they reach target wordcount
            endloop()
            break
        else :
            print(targetwordcount - wordcount) #show remaining wordcount
            if wordcount > 1 & lastchar == 0:
                autosave() #if you haven't just autosaved, check if it needs to again
    except UnicodeDecodeError: #ignore anything like arrow keys, etc
        os.system('cls') #clear screen
        print("Hmm?\n"+ str(targetwordcount - wordcount))
        msvcrt.getch() #discard the next input because most problem keys are two bytes
