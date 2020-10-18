"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""

import arrow

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):

    above200 = 0
    num200 = 0
    i = 0
    div = 34
    totHrs = 0
    totMins = 0
    per20 = (1.2 * brevet_dist_km)
    #checks if number over 20% of the brevet
    if control_dist_km > per20:
        
        print("can't use this number for this distance")
    #code will run depending on the distance set by user
    elif brevet_dist_km == 200:

        if control_dist_km > brevet_dist_km:
            control_dist_km = brevet_dist_km

        totHrs = float(control_dist_km / 34)
        totMins = round((totHrs - int(totHrs))*60)

    elif brevet_dist_km <= 600:

        if control_dist_km > brevet_dist_km:
            control_dist_km = brevet_dist_km
        #check how many 200s and the remainder from last 200
        #then enters a for loop depending on how many 200s there
        #it will start dividing from 34 then -2 for each 200
        if control_dist_km >= 200:
            above200 = (control_dist_km % 200)
            num200 = int(control_dist_km / 200)

            for i in range(num200):
                totHrs += (200 / div)
                div -= 2

            totHrs += (above200 / div)

        else:

            totHrs += (control_dist_km / 34)
        totMins = round((totHrs - int(totHrs))*60)

        print("open_time <= 600km",int(totHrs),'H',totMins)

    elif brevet_dist_km > 600:
        if control_dist_km > brevet_dist_km:
            control_dist_km = brevet_dist_km
        
        if control_dist_km >= 600:
            above200 = control_dist_km - 600
            for i in range(3):
                totHrs += (200 / div)
                div -= 2
            totHrs += (above200 / div)
        elif control_dist_km >= 200:
            above200 = (control_dist_km % 200)
            num200 = int(control_dist_km / 200)
            for i in range(num200):
                totHrs += (200 / div)
                div -= 2
            totHrs += (above200 / div)
        else:
            totHrs += (control_dist_km / 34)
        totMins = round((totHrs - int(totHrs))*60)
        print("open_time 1000km",int(totHrs),'H',totMins)

    else:
        print("This shouldn't happen")

    hrs = int(totHrs)

    now = arrow.get(brevet_start_time)
    now = now.replace(tzinfo='US/Pacific')
    now = now.shift(hours=+hrs)
    now = now.shift(minutes=+totMins)


    return (now.isoformat())

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):

    totHrs = 0
    totMins = 0
    above600 = 0
    num = 0
    per20 = (1.2 * brevet_dist_km)
    if control_dist_km > per20:
        print("can't use this number for this distance")

    #any distance with 600 or less have same implementations
    elif control_dist_km < 60:
        totHrs += ((control_dist_km / 20) + 1)
    elif brevet_dist_km <= 600:

        if control_dist_km >= brevet_dist_km:
            control_dist_km = brevet_dist_km
            num = brevet_dist_km / 100
            totMins += (5 * num)

        totHrs += (control_dist_km / 15)
        totMins += (round((totHrs - int(totHrs))*60))
        
        print("close_time <=600km:", int(totHrs),'H',totMins)

    elif brevet_dist_km <= 1000:

        if control_dist_km > brevet_dist_km:
            control_dist_km = brevet_dist_km

        if control_dist_km >= 600:
            above600 = control_dist_km - 600
            totHrs += (600 / 15)
            totHrs += (above600 / 11.428)

        else:
            totHrs += (control_dist_km / 15)

        totMins = round((totHrs - int(totHrs))*60)
        print("close_time <=1000km", int(totHrs),'H',totMins)
    else:
        print("This shouldn't happen")

    #totMins = round((totHrs - int(totHrs))*60)
        
    hrs = int(totHrs)
    now = arrow.get(brevet_start_time)
    now = now.replace(tzinfo='US/Pacific')
    now = now.shift(hours=+hrs)
    now = now.shift(minutes=+totMins)
    return now.isoformat()

