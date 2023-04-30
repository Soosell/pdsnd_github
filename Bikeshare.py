import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nWelcome to US Bikeshare data')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      city = input('\nSelect Chicago, Washington or New York City for your analysis.\n').lower()
      if city not in ('new york city', 'chicago', 'washington'):
        print("Please try again, using the specified City names.")
        continue
      else:
        break

    # get user input for month (all, january, february, ... , june)
    while True:
      month = input("\nWhich month do you want to see data for?  Please use January, February, March, April, May, June. Type 'all' for no filter\n").lower()
      if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print("Please use the specified months, or type all.")
        continue
      else:
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input("\nWhich day would you like to see data for? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' for no filter.\n").lower()
      if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        print("Please use the specified days, or type all")
        continue
      else:
        break

    print('-'*40)
    return city, month, day


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
    # load data into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # alter start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # pull month & day from start time & create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
   	 	# get the int from months
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month & creates the new dataframe
        df = df[df['month'] == month]

        # filters by day of week
    if day != 'all':
        # filters by day of week & creates the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mc_month = df['month'].mode()[0]
    print('Most Common Month:', mc_month)

    # display the most common day of week
    mc_day = df['day_of_week'].mode()[0]
    print('Most Common day:', mc_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mc_hour = df['hour'].mode()[0]
    print('Most Common Hour:', mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Commonly Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].value_counts().idxmax()
    print("Most commonly used start station:", mc_start_station)

    # display most commonly used end station
    mc_end_station = df['End Station'].value_counts().idxmax()
    print("Most commonly used end station:", mc_end_station)

    # display most frequent combination of start station and end station trip
    mc_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("Most commonly used start station & end station: {}, {}"\
            .format(mc_start_end_station[0], mc_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    # display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available.")

    # Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo data available.")

    try:
      Recent_year = df['Birth Year'].max()
      print('\nMost Recent Year:', Recent_year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available")

    try:
      Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    # Asks user if they want raw data
    i = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter y/n.\n')
        if raw.lower() == 'y':
            print(df[i:i+5])
            i = i+5
        else:
            break
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()