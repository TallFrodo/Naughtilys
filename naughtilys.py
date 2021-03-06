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
    total_words = wordcount #initialise cumulative word count 
    print (output) #print what you've gotten so far
    if lastchar == 1: #if lastchar wasn't blank
        wordcount = wordcount+1#add the word they were working on
    print ("Finished. Session word count: "
           + str(wordcount)) #output estimated wordcount
    with open(projectname + ".txt", 'a+') as outfile: 
        outfile.write(output) #open file named test.txt in append mode
        with open(projectname + ".txt", 'r') as f: #read again to get wordcount
            for line in f: #get cumulative wordcount (one per line + all spaces)
                total_words = total_words + 1 + line.count(' ')
        # output cumulative wordcount
    print ("Cumulative word count is something like " + str(total_words))
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
        with open(projectname + ".bak", 'w+') as outfile: #open or create a .bak
            with open(projectname + ".txt",'r') as infile: #copy in exiting proj
                for line in infile:
                    outfile.write(line)
            outfile.write(output) #overwite .bak file
    if wordcount % 500 == 0: #every 500 words
        clear_screen() #replace normal blank output with backup announcement
        print ("***BACKUP CREATED***\n" + str(targetwordcount - wordcount))
        with open(projectname + time.strftime('%Y%m%d%H%M') + ".bak", 'w+') \
             as outfile: #create new unique .bak file
            with open(projectname + ".txt",'r') as infile: #copy in exiting proj
                for line in infile:
                    outfile.write(line)
            outfile.write(output) #overwrite .bak file
                

#ACTUAL START OF PROGRAM HERE
clear_screen()
print("Welcome to Naughtilys - Ctrl+C or ESC to quit early or [~`] for a sneaky peek")
try:
    gettargetwordcount()
except KeyboardInterrupt: #catch any -Ctrl+C inputs neatly
    input("Press Enter to quit")
    sys.exit()

while 1: #msvcrt.kbhit: #main loop - whenever there's something in the kb buffer
    char = get_char_input(host_os) #get keyinput based on OS
    clear_screen()
    if char == chr(27): #on ESCAPE KEY
        endloop()
        break
    elif char == chr(32): #on SPACE BAR
        if lastchar == 1: #make sure lastchar wasn't blank
            output = output+char #concatenate the space
            lastchar = 0 #mark lastchar as being blank
        print ("") #print a blank line
        
    elif char == chr(13) and len(output) > 1: #on CARRIAGE RETURN
        previous_key = output[-1]#check the latest key
        if previous_key == " ": #if previous key was space
            output = output[:-1]+"\n" #replace it with \n for formatting
        if lastchar == 1: #if last character wasn't blank
            output = output+char+"\n" #format carriage returns as \n 
        lastchar = 0 #mark lastchar as being blank
        print ("") #print a blank line
    elif char == "Hmm?": #catch invalid inputs (still broken for mac)
        print ("Hmm?")
        
    elif char == chr(8): #on BACKSPACE
        if len(output) >1: #if there's something to delete
            if lastchar == 1: #if lastchar wasn't \n or space
                output = output[:-1] #remove last letter from output
                previous_key = output[-1]#name the new latest key
                print(previous_key) #display new last key
                if (previous_key == ' ' or previous_key == '\n'): #if blank
                    lastchar = 0 #update lastchar to blank
            elif lastchar == 0: #if they try and backspace a blank
                print("No Backsies") #tell user to harden up
        else: #if they haven't started writing
            print("Nothing to delete.") #inform user

    elif char == chr(96): #on BACKTICK
        targetwordcount +=1 #increment wordcount as punishment
        if len(output) > 30: print("Sneaky Peek: " + output[-30:])
        #and show last 30 characters
        else:
            under30 = len(output) #or at least those that exist so far
            print ("The story so far: " + output[-under30:])

    else: #if it wasn't space, return, esc, etc.
        lastchar = 1 #set lastchar to not blank
        output = output+char #concatenate this character to output string
        print (char) #otherwise print it
    #get wordcount:
    wordcount = output.count(' ') + output.count('\n') #easy wordcount hack
    if wordcount >= targetwordcount: #break if they reach target wordcount
        endloop()
        break
    else :
        print(targetwordcount - wordcount) #show remaining wordcount
        if wordcount > 1 & lastchar == 0:
            autosave() #on blank, see if autosave is needed
