import time
import pandas as pd
import numpy as np

# complete code refactoring
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['January','February','March','April','May','June','July','August','September','October','November','December']
DAY_DATA = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thirsday', 'Friday', 'Saterday']
DAY_INDEX = [1, 2, 3, 4, 5, 6, 7]
UNIT = ['count(s)', 'year', 'month', 'hours', 'people']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n    Hello! Let\'s explore some US bikeshare data!\n' )

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to see data? : C(Chicago), N(New York City), W(Washington) : \n")
    # Check the 'city' value
    city = check_city(city)
    month = ""
    day = ""

    if city != None:
        # get user input for month (all, january, february, ... , june)
        answer = input("Would you like to filter the data by month, day or not at all? Choose the number.\n 1. both month and day.\n 2. only month.\n 3. not at all.\n")

        if answer == "1" or answer == "2":
            month = input("Which month? january, february, march, etc:\n")
            month = month.title()

            # Check the 'month' value.
            # Only if 'month' data is correct, you can input 'day' data.
            # If 'month' data doesn't exist, month and day have 'all' condition.
            if month not in MONTH_DATA :
                month = "all"
                day = "all"
            else:
                #Check the weekday
                if answer == "1":
                    try:
                        # get user input for day of week (all, monday, tuesday, ... sunday)
                        day = int(input("Which day? Please type your response as a Number.(e.g., 1=Sunday, 2=Monday)\n"))
                        # change integer 'day' into string 'day'
                        day_Series = pd.Series(DAY_DATA, DAY_INDEX)
                        day = day_Series[day]
                    except ValueError as e:
                        day = "all"
                else:
                    day = "all"
        else:
            month = "all"
            day = "all"

    print('-'*40)
    return city, month, day

# Check whether the 'city' is correct or not.
def check_city(city):

    city_name = city.lower().replace(' ', '')
    city_list = list(CITY_DATA.keys())

    if city_name == 'c' or city_name == 'chicago':
        city = city_list[0]   #'chicago'
    elif city_name == 'n' or city_name == 'newyorkcity':
        city = city_list[1]   #'new york city'
    elif city_name == 'w' or city_name == 'washington':
        city = city_list[2]   #'washington'
    else:
        city = None

    return city


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    for name, value in CITY_DATA.items():
        if name == city:
            df = pd.read_csv('./' + CITY_DATA[name])       # return : pandas.core.frame.DataFrame
            df["Start Time"] = pd.to_datetime(df["Start Time"])     # 동일한 dataframe에서 작업해야 함.

            # create columns 'Month', 'DayOfWeek'
            df["Month"] = df["Start Time"].dt.month
            df["DayOfWeek"] = df["Start Time"].dt.weekday_name           # dayofweek

            if month != "all":
                month = MONTH_DATA.index(month) + 1
                df = df[df['Month'] == month]

            if day != "all":
                df = df[df["DayOfWeek"] == day]

    return df


def time_stats(df, city, month, day):
    """ Displays statistics on the most frequent times of travel.
        Args:
            (DataFrame) df - filtered dataset
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('filter : \'{},\'\'{},\'\'{}\''.format(city.title(), month, day))
    start_time = time.time()

    # display the most common month
    # if 'month' condition is 'all', don't need to display "Popular month "
    #Series.mode()[0])         # returns Series even if only one value is returned
    if month == "all":
        print("Popular month :" , df["Month"].mode()[0], UNIT[2])       # UNIT[2] : month

    # display the most common day of week
    # if 'day' condition is 'all', don't need to display "Popular day of week "
    if day == "all":
        str = "Popular day of week in {} : {}"
        print(str.format(month, df["DayOfWeek"].mode()[0]))  # test : new york city March all

    # display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    if df["Hour"].mode()[0] >= 12:   # ex) 17>12
        hour = df["Hour"].mode()[0] - 12
        unit = "pm, "
    else:
        hour = df["Hour"].mode()[0]
        unit = "am, "
    print("Popular start hour : ", hour, unit, df["Hour"].count(), UNIT[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """ Displays statistics on the most popular stations and trip.
        Args:
            (DataFrame) df - filtered dataset
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('filter : \'{},\'\'{},\'\'{}\''.format(city.title(), month, day))
    start_time = time.time()

    # display most commonly used start station and coount
    print("The Most used start station is \"{}\"".format(df["Start Station"].mode()[0]))
    print(df["Start Station"].value_counts().head(1).values[0], UNIT[0])

    # display most commonly used end station and coount
    print("The Most used end station is \"{}\"".format(df["End Station"].mode()[0]))
    print(df["End Station"].value_counts().head(1).values[0], UNIT[0])

    # display most frequent combination of start station and end station trip # ascending=False
    text = "The most frequent combination of start station and end station trip : \n"
    top_item = df.groupby(["Start Station", "End Station"]).size().nlargest(1)
    print(text , top_item.index[0])
    print(top_item.values[0], UNIT[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration.
       Args:
           (DataFrame) df - filtered dataset
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating Trip Duration...\n')
    print('filter : \'{},\'\'{},\'\'{}\''.format(city.title(), month, day))
    start_time = time.time()

    # display total travel time
    print("Total travel time : ", df["Trip Duration"].sum(), UNIT[3])

    # display mean travel time
    print("Mean travel time : ", df["Trip Duration"].mean(), UNIT[3])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users.
       Args:
           (DataFrame) df - filtered dataset
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating User Stats...\n')
    print('filter : \'{},\'\'{},\'\'{}\''.format(city.title(), month, day))
    start_time = time.time()

    # Display counts of user types
    # print(df.groupby(["User Type"]).size())  # return pandas.core.series.Series
    for i in range(len(df.groupby(["User Type"]).size())):
        print("User types {}: ".format(i+1), df.groupby(["User Type"]).size().index[i], df.groupby(["User Type"]).size().values[i], "people")

    # Gender, Birth Year are only available for NYC and Chicago , if city == "washington"
    if city == list(CITY_DATA.keys())[2]:
        print("No Data of \'Gender, Birth Year\' in {} City".format(city.title()))
    else:
        # Display counts of gender
        for i in range(len(df.groupby(["Gender"]).size())):
            print("Gender {}: ".format(i+1), df.groupby(["Gender"]).size().index[i], df.groupby(["Gender"]).size().values[i], "people")

        # Display earliest, most recent, and most common year of birth
        print()
        print("The Earliest year of birth : ", int(df["Birth Year"].min()), UNIT[1])
        print("The most Recent year of birth : ", int(df["Birth Year"].max()), UNIT[1])
        print("The most Common year of birth", int(df["Birth Year"].mode()[0]), UNIT[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        #print(city, month, day)
        if city != None:
            print("Processing......")

            df = load_data(city, month, day)

            # If there is no dataset selected from the conditions, notice 'No data is found'
            # The case of no data : The condition 'Chicago April Thirsday(5)' & 'New York City,''April,''Thirsday'
            if not df.empty:
                print("Completed Successfully! Total ", df.size, UNIT[0])
                # Ask whether the user want to see 5 lines of data.
                show_data = input("Would you like to specify the data?(yes or no)")
                # if you type [yes'] except bracket, this program show all data. So I can't code ' show_data == 'yes' '
                if "yes" in show_data:
                    count = 5
                    print(df.head(count))
                    show = True

                    while show:
                        # Ask whether the user will see the data more or not.
                        show_more = input("Do you want to see 5 more data or all or stop?(yes, all, stop)")
                        if "yes" in show_more:
                            print(df[count:count+5])
                            count += 5
                        elif "all" in show_more:
                            print(df)
                            show = False
                        else:
                            break

                time_stats(df, city, month, day)
                station_stats(df, city, month, day)
                trip_duration_stats(df, city, month, day)
                user_stats(df, city, month, day)
            else:
                print("<< No Data is found for \'{},\'\'{},\'\'{}\' condition.  >>".format(city.title(), month, day))

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            print("City was wrong. Please try correctly.")
            print('-'*40)

if __name__ == "__main__":
	main()
