# -*- coding: utf-8 -*-

import csv_File_Merging
import Data_Validation
import Station_Analysis
import Week_Day_Analysis
import Data_Filter

def run():
    
    cont = 0
    
    while cont == 0:
        
        print("1. csv file merger")
        print("2. data validation")
        print("3. station analysis")
        print("4. week day analysis")
        print("5. data filter")
        print("q. quit")
        
        choice = input("Select an option: ").lower()
    
        print("\n")
    
        if choice == '1':
            csv_File_Merging.csv_file_merger()
            
        elif choice == '2':
            Data_Validation.data_validation()
            
        elif choice == '3':
            Station_Analysis.station_analysis()
            
        elif choice == '4':
            Week_Day_Analysis.week_day_analysis()
            
        elif choice == '5':
            Data_Filter.data_filter()
            
        elif choice == 'q':
            print("ANALYSIS COMPLETE! :)")
            cont = 1
        
        print("\n")    

run()