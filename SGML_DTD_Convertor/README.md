SGML_DTD_Convertor
==================

Converts Arbortext file DTD for BEAR purposes
These instructions will assist in converting DTDs by converting a file to a single string and then
finding and replacing tags as necessary, using the APP.

This will fix tagging throughout the file, and remove sgm references and cgm references, that don't exist, from the declarations.
  - The tool finds and replaces tags based on the text file. 
  - Changes can be made to that file in order to modify this tool.

1. Convert each file,as necessary, to single instance file.

	a. Open the file in Arbortext
	
	b. Save as file name and "_single"
	
	c. Ctrl+A, Ctrl+C, Ctrl+V, in that order with a pause in between.
	
	d. Save file, and close	
	

2. Add file names to convert and text file name to convert with to "Run.txt" file.

	a. Enter the path to the file and name with ".sgm" at the end.
	
	b. Then a space, a colon, and a space.
	
	c. Then a text file name to convert with, this will not have an extension.
	
	d. Save and close the "Run.txt" file.

	====================Example:====================

	C:\Path\TO 35C2-3-474-11_single.sgm : 87929C-AV6aD1P0 to AV8aD0P0

3. Double-click the Tag_Convertor App.

4. You will have a file with the word "New " in front of it in the appropiate folder.

5. Open the file in Arbortext again and click the "Check Completness" button to verify everything is good.
