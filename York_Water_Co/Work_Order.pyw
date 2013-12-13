#Python 2.7, Dave Gillsepie
'''	
	This tool has been designed specifically for the information found
		in "sample_wo_data.txt." and only reads and displays the data.
	It assumes this tool and the file are in the same folder
	It loads a file, creates objects based on Work Order Number,
		displays those Work Order Numbers in a form, for selection, to show
		the Work Order Details in another form.
	Only one Work Order will show at a time.
	When closing the main form, with Work Order Numbers, the Details form
		will close as well.
'''
from Tkinter import *
import tkMessageBox
##########################################################################################################
########### Load files and create objects ################################################################
##########################################################################################################
def Load_Work_Orders(file_name): 
	'''Gathers data from file named "sample_wo_data.txt"'''
	#######################################################################################################
	######## The class part ###############################################################################
	#######################################################################################################
	class Sample_data(object):
		'''Sample_data splits the row of data and stores it'''
		def __init__(self, split_data):
			'''Takes a list of columns from a row of data'''
			if split_data[0] != "":
				self.split_data = split_data[:]
				self.last_six = split_data[-6:]
				self.prompt_sequence = {}
				self.load_properties()
				self.update_properties(self.last_six)
				Work_Orders[self.split_data[0]]=self #add to dictionary

		def load_properties(self):
			'''Assign an attribute for each property, from split_data in list of properties '''
			for i in range(len(self.Properties)):							  
				setattr(self, self.Properties[i], self.split_data[i])	

		def update_properties(self, last_six):
			'''Takes the last six items of the row, makes {sequence:[prompt,value]}'''
			self.prompt_sequence[last_six[0]]=[last_six[1], last_six[2]]
			self.prompt_sequence[last_six[3]]=[last_six[4], last_six[5]]

		def __repr__(self):
			'''returns a single row of all objects properties'''
			return ' '.join(self.split_data) + " Prompts: " + ' '.join([\
				' '.join([y for y in x]) for x in self.prompt_sequence])
	############################################################################################
	######## The open file and read data part ##################################################
	############################################################################################
	Work_Orders = {} #string(Order Number):Object
	with open(file_name, 'r') as sample_wo_data:
		'''Open specific file and begin'''
		first_line = sample_wo_data.readline()[:-1] #Extract properties from frist line
		Sample_data.Properties = [prop for prop in first_line[:].split(' ') \
			if prop != ""][:-6] #Set class variable for Sample_data
		dashes = sample_wo_data.readline() #Asumes dashes are seperated by spaces 
		Lengths = [len(ld) for ld in \
			dashes[:-1].split(' ') if ld != ""] #and indicate # of digits per entry
		for row in sample_wo_data: #get data from each line
			split_data =  [] #set to empty list
			nrow = row[:-1] #removes \n
			for x in range(len(Lengths)): #For each length extracted from dashes
				split_data.append(nrow[:Lengths[x]].strip()) #Append column from row
				nrow = nrow[Lengths[x]+1:] #slice nrow + 1 space for next column
			if split_data[0] not in Work_Orders: #If Work Order not in dictionary
				Sample_data(split_data) #Create an object with split_data and add to dict
			else:
				last_six = split_data[-6:] #If it is in the Work_Order dict, update it
				Work_Orders[split_data[0]].update_properties(last_six)	#Only the last six are different				
	return Work_Orders #Returns a dictionary of objects
#########################################################################################################################	
######## Function to display the Work Orders information ################################################################
#########################################################################################################################
def Display_Work_Order(WORK_ORDERS, current_pos):
	disp_order = Tk() #instance
	global windows
	windows = disp_order #For one work order open at a time purposes
	Button(disp_order, text="Exit Order " + current_pos,
		bg='#FE9A2E', command=disp_order.destroy).pack(fill=BOTH) #Exit button
	frame2 = Frame(disp_order) #frame for upper Work Order part
	frame2.pack(fill=BOTH,expand=1)
	frame2.config(bd=10,relief='raised')
	frame3 = Frame(disp_order) #frame for lower Work Order part
	frame3.pack(fill=BOTH,expand=1)
	frame3.config(bd=10,relief='raised')
	for i in range(4): #configure all 4 columns in both frames
		frame2.columnconfigure(i,weight=i%1+1)
		frame3.columnconfigure(i,weight=i%1+1)
	order = WORK_ORDERS[current_pos[1:]] #set order to the indexed Work Order object
	disp_order.title("Work Order " + current_pos) #set name of form
	properties = order.Properties[:] #copy class properties, not necessary?
	prop_next_column = len(properties)/2 #When to go to the next set of columns
	for prop in properties: #handles common attributes of object, not prompts
		pro_row = properties.index(prop) #Where we are
		if pro_row <= prop_next_column: #Split information into to columns
			columns = (0,1,0) #First, Second column, add to row position
			frame2.rowconfigure(pro_row, weight=1) #each row gets a weight for expanding
		else: #Third, Fourth column, add to row position
			columns = (2,3,-prop_next_column-len(properties)%2) #ensures 2 set of columns row=0 for odd number of rows
		propname = ' '.join(x.title() for x in prop.split('_')) #Clean up name
		L1 = Label(frame2, text=propname, anchor=W).grid(row=pro_row+columns[2],
			column = columns[0], sticky=NSEW,in_=frame2) #Adds label with property name
		e1 = Entry(frame2, width = 40) 
		e1.insert(0,getattr(order, prop) ) #Adds property value
		e1.grid(row=pro_row+columns[2], column=columns[1], sticky=NSEW,in_=frame2)
	L1 = Label(frame3, text ='Prompts and Values',relief='sunken',background='gray').grid(row=prop_next_column+1, 
		column = 0, columnspan=4,in_=frame3, sticky =NSEW, pady=5, padx=5) #seperates common data and prompts
	prompt_next_column =  len(order.prompt_sequence)/2 #When to go to the next set of columns
	sorted_prompts = sorted(order.prompt_sequence, 
		key = lambda key: int(key)) #sorts in order of prompt number
	for prompt in sorted_prompts: #handles all the prompts of object in order of prompts
		pro_row = sorted_prompts.index(prompt)+prop_next_column+1 
		if pro_row-1 < prompt_next_column+prop_next_column:
			columns = (0,1,1) #First, Second column, add to row position 
			frame3.rowconfigure(pro_row+1, weight=1) #each row gets a weight for expanding
		else: #Third, Fourth column, add to row position
			columns = (2,3,-prompt_next_column+1)
		L1 = Label(frame3, text=order.prompt_sequence[prompt][0] + ": ", anchor=W).grid(row=pro_row+columns[2],
			column = columns[0], sticky=NSEW,in_=frame3) #Adds label with prompt name
		e1 = Entry(frame3, width = 40) 
		e1.insert(0,order.prompt_sequence[prompt][1]) #Adds prompt attribute values
		e1.grid(row=pro_row+columns[2], column=columns[1], sticky=NSEW,in_=frame3)
###########################################################################################################
################ GUI ######################################################################################
###########################################################################################################
file_name = 'sample_wo_data.txt'
windows = '' #For one work order open at a time
master = Tk() #instance
frame = Frame(master) #Create a frame for master
frame.pack(expand = 1, fill=BOTH) #Make frame stretchy
Work_Orders = Load_Work_Orders(file_name) #Read file and create objects
master.title(file_name[:file_name.index('.')]) #sets title
l1 = Label(master, text = 'Work Orders') #adds descritpion for listbox
l1.pack(in_=frame, fill=X)
############## Close open order and then open new one ################
def nextord(): #Select Work Order in Listbox and display it
	try:windows.destroy() #kill the last Word Order, applicable
	except:	pass #if not, then move along
	finally:Display_Work_Order(Work_Orders, 
		listbox.get(listbox.curselection())) #Show me the Work Order
########### Add button and listbox with scrollbar #############
Button(master, text="VIEW WORK ORDER", anchor=S, width=30, 
	command=nextord).pack(side = BOTTOM, padx = 5, 
	pady = (0,5), in_=frame,fill=X) #Add a button to show order
scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y, padx = (0,5), in_=frame)
listbox = Listbox(master, yscrollcommand=scrollbar.set) 
scrollbar.config(command=listbox.yview)
listbox.pack(fill=BOTH, expand=1,  padx = (5,0), in_=frame)
######### Populate Listbox ##########
for item in Work_Orders: # listbox.insert(END, "Order Numbers")
    listbox.insert(END, ' ' + item)
listbox.selection_set(0)
###### click to show Work Order ######
def onselect(evt): #makes it so clicking an order number will show the work order too
    nextord() #Just hole the left mouse button down and go over orders, its cool.
listbox.bind('<<ListboxSelect>>', onselect) #show work order on click
########### What happens when you close master ##################
def handler():
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        master.quit()
        try:windows.quit() #if there is a window open, close it
    	except:pass #if not, see you later
master.protocol('WM_DELETE_WINDOW',handler) #When you close master

master.mainloop()
