# -*- coding: utf-8 -*-
"""

@author: 
"""

def data_filter():

    import csv
    
    dataset = []
    f = open('merged.csv', 'r')
    data = csv.DictReader(f)
    
    for row in data:
        row['trip_distance_km'] = float(row['trip_distance_km'])
        row['start_hour'] = int(row['start_hour'])
        row['duration_min'] = float(row['duration_min'])
        dataset.append(row)
    f.close()
    
    if len(dataset) == 0:
        print('No data found in merged.csv.')
    else:
        while True:
            print('\nChoose filter:')
            print('1.Distance threshold filter')
            print('2.Time period during the day filter')
            print('3.Geographic area filter')
            choice = input('Enter choice 1-3: ')
    
            if choice == '1':
                filter_type = 'distance'
                value = float(input('Enter trip distance (km): '))
            elif choice == '2':
                filter_type = 'time'
                start = int(input('Enter start hour (0-23): '))
                end = int(input('Enter end hour (0-23): '))
                value = (start, end)
            elif choice == '3':
                filter_type = 'station'
                value = input('Enter start station name: ').lower()
            else:
                print('Invalid.')
                continue
    
            filtered = []
            for row in dataset:
                if filter_type == 'distance':
                    if row['trip_distance_km'] > value:
                        filtered.append(row)
                elif filter_type == 'time':
                    start, end = value
                    if start <= row['start_hour'] <= end:
                        filtered.append(row)
                elif filter_type == 'station':
                    if row['start_station'].lower() == value:
                        filtered.append(row)
    
            dataset = filtered
    
            print(f'Filtered dataset now has {len(dataset)} records.')
    
            if len(dataset) == 0:
                print('No data matches these criteria.')
            else:
                total_distance = 0
                total_duration = 0
    
                for row in dataset:
                    total_distance += float(row['trip_distance_km'])
                    total_duration += float(row['duration_min'])
    
                avg_distance = total_distance / len(dataset)
                avg_duration = total_duration / len(dataset)
    
                print('\n--- Statistics ---')
                print('Number of trips:', len(dataset))
                print('Average distance:', round(avg_distance, 2), 'km')
                print('Average duration:', round(avg_duration, 2), 'minutes')
    
    
            if len(dataset) == 0:
                print("No more records.")
                break
    
            again = input('\nApply another filter to this result? (yes/no): ').lower()
            if again != 'yes':
                print('Program ended.')
                break
    
        print('Filtering complete :)')
 