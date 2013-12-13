Run = open('Run.txt') 
for e in Run:
    oneline = ''
    FileName = e[:e.index(':',3)-1] 
    Filename = open(FileName) 
    CF = e[e.index(':',3)+2:-1]

    pnew = ''
    f = FileName
    for i in range(len(f.split('\\'))):
        if i == len(f.split('\\'))-1:
            pnew += 'New ' + f.split('\\')[i]
        else:
            pnew += f.split('\\')[i] + '\\'
    
    print '"' + FileName + '" with ' + CF + '.txt to ' + '"' + pnew + '"'
    print 'Converting...'
    n = open(str(pnew), 'w') # opens or starts new file
    n.write('') # writes nothing in file to clear out existing information
    n.close() # closes new file
    for i in Filename: # for every line in file
        ID = True # establis ID as True for write/nowrite purposes
        if i[-11:-1] == 'NDATA cgm>': # if this is a cgm declaration
            fid = i[i.index(' ')+1:i.index('SYSTEM')-1] #extract f-id
            p = open(FileName) # open file for each declaration
            for figure in p: # for each line in file check for declaration
                ID = False # make ID False for write/nowrite purposes
                if 'boardno="' + fid + '">' in figure: # If found
                    ID = True # make ID True for write/nowrite purposes
                    break # stop loop if found
            p.close() # close new original file
        nline = i[:len(i)-1] # what to write
        if ID == False: # if the ID is False then the line doesn't get written
            pass
        else:
            if i[-7:-1] == '.sgm">': # if the line is a sgm reference, then the line doesn't get written.
                pass
            elif nline == '\n':
                pass
            elif nline == '':
                pass
            else:
                if nline[-1] == '>' or nline[-1] == '<':
                    oneline +=nline
                else:
                    oneline +=nline + ' '
    f = open(str(pnew), 'a')
    z = open(CF + '.txt')
    for o in z:
        find = o[:-1] # q is what to find
        replace = ''
        if ':' in o: # if there is a : that means we replace q or find with something, not nothing
            find = o[:o.index(':')-1]
            replace = o[o.index(':')+2:-1] # what to replace it with
        oneline = oneline.replace(find,replace)
    fr = {'><':'>' + '\n' + '<','[ <':'[' + '\n' + '<','>]':'>' + '\n' + ']'}
    for e in fr:
        find = e
        replace = fr[e]
        oneline = oneline.replace(find, replace)
    f.write(oneline)
    f.close()
    z.close()
    n.close() # closes new file
    
print 'Finished'
