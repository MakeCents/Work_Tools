'''This tool is used to rename the files rapidly. I use it to move cgms from svn.
    then I update svn as if they were never renamed.
    This will overwrite anyfiles in the topath'''

import os
#os.getcwd()

def Intro(frompath, topath):
    #Intro
    print "The following files will be moved from:"
    print "\t" + frompath
    print "To:" 
    print "\t" + topath +'\n'

def RenameFiles(frompath, topath,files):
    #Rename files from path-to path
    for i in files:
        os.rename(frompath + i,topath+i)
        print i

def CheckFiles(fileext, frompath):
    #Check which files meet the extension in the from path
    try:
        files = os.listdir(frompath)
        return [x for x in files if x[-3:] == fileext]
    except:
        raw_input("Path " + frompath + " is not valid.\nPress enter to exit.")
        return ['error']

def CheckPath(frompath):
    if len(frompath) < 1:
        return False
    return True

def OpenPath(fileName):
    with open(fileName,'r') as f:
        frompath = f.readline()
        if CheckPath(frompath):
            if frompath[-1] == '\n':
                return frompath[:-1] + "\\"
            elif(frompath[-1] == "\\"):
                return frompath
            else:
                return frompath + "\\"
        else:
            raw_input("Path in " + fileName + " is not valid.\nPress enter to exit.")
            return ""
        

def main():
    #Ask user for extension to move
    fileext = str(raw_input("What file extension are you moving?   ")).lower()
    #Get the folders involved
    frompath = OpenPath("from_path.txt")
    topath = OpenPath("to_path.txt")
    #Gather file names
    files = CheckFiles(fileext, frompath)
    filesto = CheckFiles(fileext, topath)
    #if there are files with that ext then move them, or say there wasn't any
    if files == []:
        #wait so the user can see it didn't move anything
        raw_input("No " + '"' + fileext +"'s" + '"' +
                  " were found in " + frompath +'\nPress Enter to exit.')
    elif(files == ["error"] or filesto == ["error"]):
         return
    else:
        #Say what you are going to do
        Intro(frompath, topath)
        #Rename the files from folder and to folder
        RenameFiles(frompath, topath,files)
        #new line for spacing
        print
        #wait so the user can see it finished okay
        raw_input("Previous files moved\nPress Enter to exit.")
        

#file extension to look for
print "This tool is designed to move files from one folder to any other folder.\n"
print "It's original purpose was to move things from SVN to deliverable folders,\n\tvery quickly, and\
 then update the SVN folder after, so nothing is lost.\n"
print "Ensure the path of the folder to move things FROM is on the first line of " + '\n"from_path.txt" \n--and--'
print "Ensure the path of the folder to move things TO is on the first line of " + '\n"to_path.txt"\n'

main()

