import time
import pandas as pd
import numpy as np
from datetime import  datetime
CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def  time_func(func):
  def time_func_(*args, **kwargs):
    start = time.time()
    res = func(*args, **kwargs)
    end = time.time()
    print("The  function {} Took {} seconds...".format(func.__name__,end- start))
    return res
  return time_func_


@time_func
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    try:
      print('Hello! Let\'s explore some US bikeshare data!')
      while True:
        city = str(input("Enter  the name  of  the  city  of  intrest (chicago, new_york, washington).")).lower()
        month  = str(input("Enter  the  month of  intrest (all, january, february,march,april, may, june)")).lower()
        day = str(input("Enter  the  week day  of  intrest all, monday, tuesday, ... sunday).")).lower()
        proceed = str(input("Do you  wish to proceed to th next  step?(yes, no)"))
        if  proceed.lower() == "yes":
          break
    except KeyError as e:
      print("Check your  parameters  please.")


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*40)
    return city, month, day

@time_func
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
    try:
        df = pd.read_csv(CITY_DATA[f"{city}"])
        df["Start Time"] = pd.to_datetime(df["Start Time"])
        df["End Time"]  =  pd.to_datetime(df["End Time"])
        df["Start  month"] = df["Start Time"].dt.month
        df["Ending  month"]  = df["End Time"].dt.month
        df["starting  day"] = df["Start Time"].dt.day_name()
        df["Ending  day"] = df["End Time"].dt.day_name()
        df["Start  hour"] = df["Start Time"].dt.hour
        df['Month Name'] = df["Start Time"].dt.strftime("%b")
        if  month != "all":
          months = ['january', 'february', 'march', 'april', 'may', 'june']
          month = months.index(month) + 1
          df = df[df["Start  month"] == month]
        if  day != "all":
          df = df[df["starting  day"]==day.capitalize()]
    except KeyError as e:
      print("Check your  parameters  please.")


    return df

@time_func
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        most_common_month = df['Month Name'].mode()[0]
        print('Month with the most travels is: {}'.format(most_common_month))

        date = str(df['Start Time'].mode()[0])
        dt_obj = datetime.strptime(date.split()[0], "%Y-%m-%d") 
        print('For the selected filter, the most common day of the week is: {}'.format(dt_obj.strftime("%A")))

        popular_hour = df["Start  hour"].mode()[0]
        if popular_hour < 12:
            print('Most Common Start Hour: \n', popular_hour, ' AM')
        elif popular_hour >= 12:
            if popular_hour > 12:
                popular_hour -= 12
            print('Most Common Start Hour: \n', popular_hour, ' PM')
    except KeyError as e:
      print("Check your  parameters  please.")


    # display the most common month


    # display the most common day of week


    # display the most common start hour
    print('-'*40)

@time_func
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('\nThe Most Popular Stations and Trip...\n')
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("For the selected filters, the most common start station is: " +
          most_common_start_station)


    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common start end is: " +
          most_common_end_station)

 
    df['Start to End'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start to End']
                                            .mode()[0])
    print("The most common from start-end"
          "of stations is: " + most_common_start_end_combination)
    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip
    print('-'*40)

@time_func
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
      # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('Total travel time is : ' +
          total_travel_time + '.')

      # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")
  
 
    print('-'*40)

@time_func
def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')

        # Display counts of user types
        user_types  = df["User Type"].value_counts().to_string()
        print("User  types  Counts are {}".format(user_types))
        # Display counts of gender
        try:
          genders = df["Gender"].value_counts().to_string()
          print("The  total amount of each gender  was {}".format(genders))
        except KeyError:
          print("There is no gender")
        # Display earliest, most recent, and most common year of birth
        try:
          earliest_birth, common_birth,recent_birth = df["Birth Year"].min(), df["Birth Year"].mode()[0], df["Birth Year"].max()
          print("The  earliest birth was  on {} .\n The common birth year is {}.\nThe  most recent birth year  is {}\n".format(earliest_birth, common_birth,recent_birth)) 
        except KeyError:
          print("There  is  no Birth year please.")
    except KeyError as e:
      print("Check your  parameters  please.")

    print('-'*40)
@time_func
def peek_on(df):
    # Ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break
@time_func
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        peek_on(df)

        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
            print("Thank you  for exploring the  dataset, have a  great time.")
            break


if __name__ == "__main__":
	main()
