# -*- coding: utf-8 -*-

def csv_file_merger():

    # User inputs .csv file names
    user_files = input("Type file names to be analysed (You must add .csv at the end and only put a space between file names, eg: a.csv b.csv):")
    
    # Python splits the string into a list using .split()
    files = user_files.split()
    
    # Python opens merged.csv for writing
    f = open('merged.csv', 'w')
    
    # Creating an index so python doesn't print the header rows multiple times when merging
    index = 0
    
    # Creating a for loop to read data from user file and add it to merged.csv
    for filename in files:
       
        g = open(filename, 'r')
        
        # enumerate gives the row position of the row in the user file
        for row_position, row in enumerate(g):
            
            # If row is empty it is skipped. strip('\n') removes hidden \n in row
            in_row = row.strip('\n')
            
            if len(in_row) == 0:
                
                continue
            
            # If the row is the first row in the user data file (i.e the headers) 
            # and the headers haven't already been copied into merged.csv the headers are copied
            if row_position == 0 and index == 0:
                
                f.write(row)
                index = 1
            
            # If the row is the first row in the user data file but the headers have already
            # been copied, the row is skipped
            
            elif row_position == 0 and index == 1:
                
                continue
            
            # If the row is not a header, the row is copied into merged.csv
            
            else:
                
                f.write(row)
                
    # Closes merged.csv    
    f.close()
                
    print("file merging complete :)")  

    