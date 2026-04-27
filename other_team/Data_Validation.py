# -*- coding: utf-8 -*-
"""
@author: 
"""

def data_validation():

    import csv
    import math
    from datetime import datetime
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371 
        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))
        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    f = open('merged.csv', 'r')
    data = csv.DictReader(f)
    
    total = 0
    suspects = 0
    suspect_list = []
    
    for row in data:
        total += 1
        errors = []
        
        try:
            distance = float(row['trip_distance_km'])
            avg_speed = float(row['avg_speed'])
            duration = float(row['duration_min'])
            start_lat = float(row['start_lat'])
            start_lon = float(row['start_long'])
            end_lat = float(row['end_lat'])
            end_lon = float(row['end_long'])
            
            start_time = datetime.strptime(row['start_date'], '%d/%m/%Y %H:%M')
            end_time = datetime.strptime(row['end_date'], '%d/%m/%Y %H:%M')
            
            if end_time <= start_time:
                errors.append('Wrong time')
                
            if distance <= 0:
                errors.append('Wrong distance')
    
            if row['is_weekend'] == '0' and (row['start_day'] == 'Saturday' or row['start_day'] == 'Sunday'):
                errors.append('Weekend mismatch')
                
            if duration <= 0:
                errors.append("Wrong duration")
                
            if duration > 0:
                calc_distance = haversine(start_lat, start_lon, end_lat, end_lon)
                calc_speed = calc_distance/(duration/60)
                
                tolerance = 10
                if abs(calc_speed - avg_speed) > tolerance:
                    errors.append('Wrong speed')
    
            if not row['bike_number'].isdigit():
                errors.append('Wrong bike number')
    
            if not (-90 <= start_lat <= 90 and -180 <= start_lon <= 180):
                errors.append('Wrong coordinates')
    
        except Exception as e:
            errors.append(f'Data parsing error: {str(e)}')
    
        if len(errors) > 0:
            suspects += 1
            suspect_list.append((row, errors))
    
    f.close()
    
    g = open('defects_trips.csv', 'w')
    g.write('start_station,end_station,errors\n')
    
    for item in suspect_list:
        row = item[0]
        errors = ';'.join(item[1])
        g.write(f"{row['start_station']},{row['end_station']},{errors}\n")
    
    g.close()
    
    if total > 0:
        percentage = (suspects / total) * 100
    else:
        percentage = 0
    
    print('Total records:', total)
    print('Suspect records:', suspects)
    print('Percentage suspect:', percentage, '%')
    print('Data Validation complete :)')
    
