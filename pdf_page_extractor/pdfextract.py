'''
Import list from current file. split the name, run the text tool for each
'''
def extract_pdf_pages():
    import os

    location = os.getcwd()

    # what directory are we interested in
    directory = os.getcwd()
    # getting the list of files
    files = os.listdir(directory);
    fif = []
    for i in files:
        if i[-3:] == "pdf":
            fif.append(i)      

    print
    error = True
    while error == True:
        try:
            
            for f in fif:
                print "[" + str(fif.index(f)) + "]", f
            print
            print 'Enter "exit" to quit.'
            lf = [str(x) for x in range(len(fif))]
            wfile  = str(raw_input("Which file would you like to extract pages from (" + ', '.join(lf) + ")?  "))
            if wfile.upper() == "EXIT":
                break
            
            fname = fif[int(wfile)]
            
            start = int(raw_input("Start page? "))-1
            end = int(raw_input("End page? "))-1
            from pyPdf import PdfFileWriter, PdfFileReader
            import StringIO
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            packet = StringIO.StringIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(0,0,'')
            can.save()

            #move to the beginning of the StringIO buffer
            packet.seek(0)

            new_pdf = PdfFileReader(packet)

            # read your existing PDF
            nfname = "PAGES " + str(start+1) +" - " +str(end+1) + " extracted from " + fname
            existing_pdf = PdfFileReader(file(fname, "rb"))
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            nump = existing_pdf.getNumPages()
            page = existing_pdf.getPage(0)
            for l in range(nump):
                if l >= start and l <= end:
                    output.addPage(existing_pdf.getPage(l))
            page.mergePage(new_pdf.getPage(0))
            # finally, write "output" to a real file
            outputStream = file(nfname, "wb")
            output.write(outputStream)
            outputStream.close()
            print nfname + " written"
            error = False
        except:
            print "*" * 80
            print "There was an error.".center(80)
            print "Plase try again".center(80)
            print "If the problem persist, please see Dave Gillespie.".center(80)
            print "*" * 80
extract_pdf_pages()
again = True

while again:
    print
    ag = str(raw_input("Would you like to do another? (y/n) "))
    if ag.upper() != "N":
        extract_pdf_pages()
    else:
        again = False
