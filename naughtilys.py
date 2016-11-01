#!/usr/bin/env python
#AUTHOR: Samuel MacDonald
#PURPOSE: Very Minimalist Word Processor for NaNoWriMo and the like
#Not associated with Nautilus or ILYS or NaNoWriMo or anything else
# remotely reputable
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
try:
    import os,sys,time,msvcrt #MS specific imports
    host_os = "ms"
except:
    import os,sys,time,tty,termios #OSX / Unix(hopefully) imports
    host_os = "unix"
    
    
#*****INITIALISE GLOBAL VARS*****
output = projectname = ""
wordcount = targetwordcount = lastchar = 0

def clear_screen(): #cross-os clearscreen function
    os.system('cls' if os.name == 'nt' else 'clear') #use host_os instead?

def get_char_input(host_os): #cross-os return keypress
    if host_os == "ms": #for windows
        try:
            return msvcrt.getch().decode('UTF-8')
        except UnicodeDecodeError: #ignore anything like arrow keys, etc
            msvcrt.getch() #discard next input -most problem are keys 2 bytes
            return "Hmm?"
        
    if host_os == "unix": #for mac
        fd = sys.stdin.fileno() #do some oldschool terminal stuff that I copied
        old_settings = termios.tcgetattr(fd) #from someone far smarter than myself
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch
        except:
            return "Hmm?"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def gettargetwordcount(): #try catch to make sure the wordcount is a valid int
    global targetwordcount
    userinput = input("Desired word count? ")
    try:
        targetwordcount = int(userinput)
        clear_screen()
        getprojectname()
    except ValueError:
        clear_screen()
        print("That wasn't a number I understand sorry.")
        gettargetwordcount()

def getprojectname(): #try catch to ensure valid output file
    global projectname, targetwordcount
    clear_screen()
    print("Welcome to Naughtilys - Press Ctrl+C or ESC to quit early.")
    projectname = input("Project Title? ")
    try: #trycatch to ensure can read the entered projectname
        f = open("" + projectname + ".txt", 'r')
        try:
            first = f.readline
            ()
            for last in f: pass
            print("Your last line was: '" + last + "'. Now type.\n"
                  + str(targetwordcount))
        except UnboundLocalError:
                print("Nothing at " + projectname + ".txt. Get Typing \n"
                      + str(targetwordcount))
    except IOError: #if it doesn't already exist...
        try:
            f = open("" + projectname + ".txt", 'w') #create it
            clear_screen()
            print ("New Project " + projectname + ".txt created. Now type.\n"
                   + str(targetwordcount))
        except IOError: #if that fails too, ask for a new name
            clear_screen()
            print ("Couldn't find or create " + projectname
                   + ".txt. Try another.")
            getprojectname()
        
def endloop(): #standard way to close the program under normal circumstances
    global wordcount, projectname
    print (output) #print what you've gotten so far
    if lastchar == 1: #if lastchar wasn't blank
        wordcount = wordcount+1#add the word they were working on
    print ("Finished. Session word count (spaces and newlines): "
           + str(wordcount)) #output estimated wordcount
    with open(projectname + ".txt", 'a+') as outfile: 
        outfile.write(output) #open file named test.txt in append mode
    quitter()

def quitter():
    global projectname
    input("Check that you can see " + projectname
          + ".txt before pressing Enter to close")
    sys.exit()
        
def autosave():
    global wordcount, projectname
    if wordcount % 50 == 0: #every 50 words
        clear_screen() #replace normal blank output with autosave announcement
        print ("***AUTOSAVE***\n" + str(targetwordcount - wordcount))
        with open(projectname + ".bak", 'a+') as outfile: 
            outfile.write(output) #open file named test.txt in append mode
    if wordcount % 500 == 0: #every 500 words
        clear_screen() #replace normal blank output with backup announcement
        print ("***BACKUP CREATED***\n" + str(targetwordcount - wordcount))
        with open(projectname + time.strftime('%Y%m%d%H%M') + ".bak", 'a+') \
             as outfile: 
            outfile.write(output) #open file named test.txt in append mode
                

#ACTUAL START OF PROGRAM HERE
clear_screen()
print("Welcome to Naughtilys - Press Ctrl+C or ESC to quit early.")
try:
    gettargetwordcount()
except KeyboardInterrupt: #catch any -Ctrl+C inputs neatly
    input("Press Enter to quit")
    sys.exit()

while 1: #msvcrt.kbhit: #main loop - whenever there's something in the kb buffer
    char = get_char_input(host_os) #get keyinput based on OS
    clear_screen()
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
            output = output+char+'\n' #format carriage returns as \n 
            lastchar = 0 #mark lastchar as being blank
        print ("") #print a blank line
    elif char == "Hmm?":
        print ("Hmm?")
            
    else: #if it wasn't space, return or esc:
        lastchar = 1 #set lastchar to not blank
        output = output+char #concatenate this character to output string
        print (char), #otherwise print it
    #get wordcount:
    wordcount = output.count(' ') + output.count('\n') #easy wordcount hack
    if wordcount >= targetwordcount: #break if they reach target wordcount
        endloop()
        break
    else :
        print(targetwordcount - wordcount) #show remaining wordcount
        if wordcount > 1 & lastchar == 0:
            autosave() #on blank, see if autosave is needed
