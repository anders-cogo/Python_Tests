#Anders Simpson-Wolf
#09/2/2015
#Reading and Writing files with Python

#This code will look for a file in memory
#If the file doesn't exist, it will create it
#If the file does exist, it will open it
#It will add a new sentence to the file
#It will save the file
#Then print the contents to the command line

#create or open file
f = open('test_file.txt', 'a+')

#write a line to the file
f.write('I wrote a string to a file!  Look at me go!\n')

#print the contents of the file
f.seek(0) #do this to return to start of file
for line in f:
    print line

#close file
f.close()
