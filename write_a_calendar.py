def leap_year(year):
    ans = False
    if int(year)%100 == 0:
        if int(year)%400 == 0:
            ans = True
    else:
        if int(year)%4 == 0:
            ans = True
    return ans 



def day_of_week_jan1(year):
    day0101 = (1 + (5*((year-1)%4)) + (4*((year-1)%100)) + (6*((year-1)%400)))%7
    return day0101



def num_days_in_month(month_num, leap_year):
    if month_num in [1,3,5,7,8,10,12]:
        num_days = 31
    elif month_num in [4,6,9,11]:
        num_days = 30
    else:
        if leap_year == True:
            num_days = 29
        else:
            num_days = 28
          
    return num_days


def first_day_of_month(year,month_num):
    passedmonth = 1
    passedday = 0
    fist_day_of_month = day_of_week_jan1(year)
    while passedmonth < month_num:
        passedday += num_days_in_month(passedmonth,leap_year(year))
        passedmonth += 1
    day_difference = (passedday%7)%7
    first_day_of_month = (day_of_week_jan1(year) + day_difference)%7
    return first_day_of_month


def construct_cal_month(month_num, first_day_of_month, num_days_in_month):
    name_of_months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month_name = name_of_months[month_num - 1]
    week1 = ''
    
    for blank in range(first_day_of_month):
        week1 += '   '
    for rest_day in range(1,8 - first_day_of_month):
        week1 += ('  ' + str(rest_day))
        
    month_details = [month_name,week1]
    new_day = int(8 - first_day_of_month)
    
    while new_day <= num_days_in_month:
        new_week = ''
        num_of_days = 0
        while num_of_days < 7 and new_day <= num_days_in_month:
            if new_day < 10:
                new_week += ('  ' + str(new_day))
            else:
                new_week += (' ' + str(new_day))
            new_day += 1
            num_of_days += 1
        month_details.append(new_week)
    
    return month_details
    
        
def construct_cal_year(year):
    if year < 1800 or year > 2099:
        return None
    else:
        year_and_months = [year]
        for month in range(1,13):
            year_and_months.append(construct_cal_month(month, first_day_of_month(year,month), num_days_in_month(month,leap_year(year))))
            
    return year_and_months
        
    
def display_calendar(year):
    calendar = ""
    calendar_year = construct_cal_year(year)
    calendar_year.pop(0)
    for i, month in enumerate(calendar_year):
        for i, week in enumerate(month):
            calendar += week +"\n"
            if i == 0:
                calendar += "  S  M  T  W  T  F  S\n"
        if i !=11:
            calendar += "\n"
    return calendar.strip()
