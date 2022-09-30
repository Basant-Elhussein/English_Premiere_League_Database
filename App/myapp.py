from turtle import position
import mysql.connector
from mysql.connector import errorcode
import re
import time
from tabulate import tabulate

db = mysql.connector.connect(
    host='db4free.net',
    user='basantelhussein',
    passwd='hellothere',
    database='basant_pl'
)

cursor = db.cursor(buffered=True)  

guestMode = False
userEmail = ""
userName = ""
userBirthdate = ""
userGender = ""
userFavoriteTeam = ""
    
## Helper Functions

def check(pattern, regex):
    if re.fullmatch(regex, pattern):
      return True
    else:
      return False

def get_season(all=0):
    print("Choose in which season is the match: ")
    print("1. Season 2021/22"); print("2. Season 2020/21"); print("3. Season 2019/20"); print("4. Season 2018/19")
    if all: print("5. All")
    choice = int(input("Season: "))
    choice_to_season = {1: "2021/22", 2: "2020/21", 3: "2019/20", 4: "2018/19", 5: ""}

    return choice_to_season[choice]


def welcome():
    global guestMode
    while True:
        print("Hello to the Premier League Datacenter for the past four seasons!")
        print("Are you?")
        print("1. A new user - register now!")
        print("2. An existing user - sign in!")
        print("3. A guest - You can continue without registering but will not be able to add reviews!")

        choice = int(input("Choice: "))
        mode = 0

        if choice == 1:
            if not add_user(): continue     # present the welcome page again!
            else:
                guestMode = 0               # Not in guest mode
                return

        elif choice == 2:
            if not login(): continue     # present the welcome page again!
            else:
                guestMode = 0               # Not in guest mode
                return

        elif choice == 3:
            guestMode = 1
            return
        else:
            print("Please choose an option from 1 to 3!")
         

def add_user():
    global userEmail, userName, userFavoriteTeam, userBirthdate, userGender

    email = ''
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    while True:
        email = input("Email: ")

        if not check(email, email_regex):
            print("Please enter a valid email!")
            continue
    
        if retrieve_user(email) != None:
            print("User email already exists!")
            print("You will be returned back to welcome page.")
            return False

        break

    username = ''
    while True:
        username = input("Username (at least 3 charachters): ")
        if len(username) <3:
            print('Please enter a valid username!')
            continue
        break

    password = ''
    password_regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$")
    while True:
        password = input("Password (at least 6 charachters. Must contain letters and numbers): ")

        if not check(password, password_regex):
            print("Please enter a valid password!")
            continue

        break

    birthdate = ''
    birthdate_regex = re.compile(r"^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$")
    while True:
        birthdate = input("Birthdate (in the form yyyy-mm-dd): ")

        if not check(birthdate, birthdate_regex):
            print("Please enter a valid birthdate!")
            continue

        break

    gender = ''
    while True:
        gender = input("Enter F for female and M for male or press enter to skip: ")
        gender = gender.lower()

        if gender == 'f' or gender == 'm' or gender == '': break
        else: print("Please enter a valid gender!")
    
    favorite_club = ''
    while True:
        favorite_club = input("Please enter your favourite club: ")
        if retrieve_club(favorite_club) is None:
            print("Sorry, this club does not exist. Please try another one!")
            continue
        break
        
    add_user_query = f"INSERT INTO `user` values('{email}', '{username}', '{password}', '{birthdate}', '{gender}', '{favorite_club}');"
    queryInsert(add_user_query)

    userEmail = email
    userName = username
    userFavoriteTeam = favorite_club
    userBirthdate = birthdate
    userGender = gender
    return True


def login():
    global userEmail, userName, userFavoriteTeam, userBirthdate, userGender
    email = ''
    password = ''
    trials = 0
    while True:
        if trials >= 5:
            print("You tried many times. You will be returned to welcome page!")
            return 0
        email = input("Email: ")
        password = input("Password: ")
        if not len(password):
            print("Please enter a password!")
            continue
        res = retrieve_user(email, password)
        if res is None:
            print("Incorrect email or password")
            trials = trials + 1
            continue
        else:
            (userEmail, userName, password, userBirthdate, userGender, userFavoriteTeam) = res
            return 1


def options_page():
    while True:
        print("\nHere are cool stuff you can do!")
        print("")
        print("A. Match Reviews:")
        print("   1.  Add a review for a match\n   2.  View reviews for a match")
        print("")
        print("B. Teams Statistics:")
        print("   3.  View top 10 teams by ...")
        print("   4.  Show the team who won the most games in each season")
        print("   5.  View team information")
        print("   6.  Identify the home team for a given stadium name")
        print("   7.  Identify all the teams in a given city in the UK")
        print("")
        print("C. Players Statistics:")
        print("   8.  Show all the players from a certain nationality and their home teams history")
        print("   9.  View a given player information (by their first and last name)")
        print("   10. Show all the players who played a certain position")
        print("")
        print("Exit:\n   11. Exit")

        option = int(input("Choice: "))

        while option > 11 or option < 1:
            option = int(input("You did not enter a number between 1 and 11. Please enter your choice: "))

        if option == 11:
            return

        # Call the corresponding function to option
        option_to_function = {
            1: "insert_review",
            2: "retrieve_all_reviews",
            3: "view_top_10",
            4: "retrieve_won_most",
            5: "retrieve_team_info",
            6: "retrieve_home_team_for_stadium",
            7: "retrieve_teams_in_city",
            8: "retrieve_players_for_nationality",
            9: "retrieve_player",
            10: "retrieve_players_by_position"
        }

        globals()[option_to_function[option]]()


def view_top_10():
    print("View Tope 10 by:")
    print("   1. Matches won")
    print("   2. Home matches won")
    print("   3. Away matches won")
    print("   4. Yellow cards")
    print("   5. Red cards")
    print("   6. Fouls")
    print("   7. Shots")

    option = int(input("Choice: "))
    while option > 7 or option < 1:
        option = input("You did not enter a number between 1 and 6. Please enter your choice: ")

    option_to_query = {
            1: "top_10_matches_won",
            2: "top_10_home_matches_won",
            3: "top_10_away_matches_won",
            4: "top_10_yellow_cards",
            5: "top_10_red_cards",
            6: "top_10_fouls",
            7: "top_10_shots"
        }
    globals()[option_to_query[option]]()
    



## Helper functions for query exception handling

def queryFetchOne(query):
    while True:
        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            print("Couldn't connect to database. Please check you internet and try again!")
            time.sleep(1)

def queryFetchAll(query):
    while True:
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except:
            print("Couldn't connect to database. Please check you internet and try again!")
            time.sleep(1)

def queryInsert(query):
    while True:
        try:
            cursor.execute(query)
            db.commit()
            return True
        except:
            print("Couldn't connect to database. Please check you internet and try again!")
            time.sleep(1)


##  Queries (not interactive)

def retrieve_user(email, password = ''):
    if len(password):
        query = f"SELECT * FROM `user` WHERE email = '{email}' AND `password` = '{password}';"
    else:
        query = f"SELECT * FROM `user` WHERE email = '{email}';"
    user = queryFetchOne(query)
    return user
    
def retrieve_club(clubName):
    query = f"SELECT * FROM club WHERE clubName like '%{clubName}%';"
    club = queryFetchOne(query)
    return club

def retrieve_stadium(stadium):
    query = f"SELECT * FROM stadium WHERE stadiumName like '%{stadium}%"
    return queryFetchOne(query)

def retrieve_all_users():
    query = f"SELECT * FROM `user`;"
    users = queryFetchAll(query)
    print(users)
    return users

def retrieve_match_review(season, home_team, away_team):
    global userEmail
    query = f"SELECT * FROM `matchreviews` WHERE userEmail = '{userEmail}' AND season = '{season}' AND homeClub = '{home_team}' AND awayClub = '{away_team}';"
    match = queryFetchOne(query)
    return match

def retrieve_match(season, home_team, away_team):
    query = f"SELECT * FROM `match` WHERE season = '{season}' AND homeClub = '{home_team}' AND awayClub = '{away_team}';"
    review = queryFetchOne(query)
    return review

def top_10_matches_won():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, COUNT(*) AS 'won matches' "
        "FROM club INNER JOIN `match` ON (clubName = homeClub AND homeGoals > awayGoals) OR (clubName = awayClub AND awayGoals > homeGoals) "
        f"WHERE season = '{season}' "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, COUNT(*) AS 'won matches' "
        "FROM club INNER JOIN `match` ON (clubName = homeClub AND homeGoals > awayGoals) OR (clubName = awayClub AND awayGoals > homeGoals) "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    
    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Won Matches"]))

def top_10_home_matches_won():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, COUNT(*) AS 'home won matches' "
        "FROM club INNER JOIN `match` ON (clubName = homeClub AND homeGoals > awayGoals) "
        f"WHERE season = '{season}' "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, COUNT(*) AS 'home won matches' "
        "FROM club INNER JOIN `match` ON (clubName = homeClub AND homeGoals > awayGoals) "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    
    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Home Won Matches"]))

def top_10_away_matches_won():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, COUNT(*) AS 'won matches' "
        "FROM club INNER JOIN `match` ON (clubName = awayClub AND awayGoals > homeGoals) "
        f"WHERE season = '{season}' "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, COUNT(*) AS 'won matches' "
        "FROM club INNER JOIN `match` ON (clubName = awayClub AND awayGoals > homeGoals) "
        "GROUP BY clubName ORDER BY 2 DESC LIMIT 10;"
        )
    
    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Away Won Matches"]))

def top_10_yellow_cards():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeYCards "
        "WHEN clubName = awayClub THEN awayYCards END) AS 'yellow cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        f"WHERE season = '{season}' "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeYCards "
        "WHEN clubName = awayClub THEN awayYCards END) AS 'yellow cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )

    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Yellow Cards"]))

def top_10_red_cards():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeRCards "
        "WHEN clubName = awayClub THEN awayRCards END) AS 'red cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        f"WHERE season = '{season}' "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeRCards "
        "WHEN clubName = awayClub THEN awayRCards END) AS 'yellow cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )

    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Red Cards"]))

def top_10_fouls():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeFouls "
        "WHEN clubName = awayClub THEN awayFouls END) AS 'red cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        f"WHERE season = '{season}' "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeFouls "
        "WHEN clubName = awayClub THEN awayFouls END) AS 'yellow cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )

    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Fouls"]))

def top_10_shots():
    season = get_season(all=1)
    if len(season):
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeShots "
        "WHEN clubName = awayClub THEN awayShots END) AS 'red cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        f"WHERE season = '{season}' "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )
    else:
        query = (
        "SELECT clubName, SUM( "
        "CASE WHEN clubName = homeClub THEN homeShots "
        "WHEN clubName = awayClub THEN awayShots END) AS 'yellow cards' "
        "FROM club INNER JOIN `match` ON clubName = homeClub OR clubName = awayClub "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
        )

    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Club Name", "Shots"]))

def retrieve_won_most():
    query = (
        "SELECT season, clubName, won "
        "FROM (SELECT *, MAX(won) OVER (PARTITION BY season) AS mx_won "
        "FROM (SELECT season, clubName, COUNT(*) AS won "
        "FROM club INNER JOIN `match` ON (clubName = homeClub AND homeGoals > awayGoals) OR (clubName = awayClub AND awayGoals > homeGoals) "
        "GROUP BY 1, 2 ORDER BY 3 DESC) AS won_matches) AS won_with_max "
        "WHERE won = mx_won "
        "ORDER BY 1 DESC; "
        )
    res = queryFetchAll(query)
    print(tabulate(res, headers = ["Season", "Club Name", "Won Matches"]))
    


# Queries (interactive)

def insert_review():
    # A user can add only 1 review
    if guestMode:
        print("You are in guest mode. You cannot add a review!")
        return
    season = get_season()
    home_team = input("Home team: ")
    away_team = input("Away Team: ")

    if retrieve_match(season, home_team, away_team) is None:
        print("Sorry, this match does not exist in our database!")
        return
    
    if retrieve_match_review(season, home_team, away_team) is not None:
        print("Sorry you already reviewed this match!")
        return

    rate = input("How much do you rate this match out of 10? ")
    while True:
        try:
            if int(rate) < 0 or int(rate) > 10:
                print("Sorry rate should be from 0 to 10! your rate: ")
                rate = input("Your rate: ")
            else:
                break
        except ValueError:
            print("Invalid value. Please enter a number from 1 to 10!")
            rate = input("Your rate: ")


    text = input("Enter you review: ")
    while len(text) > 1199:
        print("The review is too long please enter a shorter one!")
        text = input("Enter you review: ")

    query = f"INSERT INTO matchreviews values('{userEmail}', '{season}', '{home_team}', '{away_team}', '{text}', '{rate}');"
    if queryInsert(query):
        print("Your review is added successfully. Thanks!")
        return


def retrieve_all_reviews():
    season = get_season()
    home_team = input("Home team: ")
    away_team = input("Away Team: ")

    if retrieve_match(season, home_team, away_team) is None:
        print("Sorry, this match does not exist in our database!")
        return

    query = ("SELECT username, rate, textReview "
    "FROM matchreviews INNER JOIN `user` ON userEmail = email "
    f"WHERE season = '{season}' AND homeClub = '{home_team}' AND awayClub = '{away_team}';")

    reviews = queryFetchAll(query)

    if len(reviews) == 0:
        print("There are no reviews for that match. You may add one through option 1 :)")
    else:
        print(tabulate(reviews, headers = ["Reviewer Username", "Rating", "Text Review"]))


def retrieve_team_info():
    team = input("What is the team name? ")
    team = retrieve_club(team)
    
    if team is None:
        print("The team is not in our database!")
        return

    season = get_season(all=1)

    (teamname, website, homestad) = team
    website = website.split('?')[0]
    team = (teamname, website, homestad)
    print(tabulate([team], headers = ["Team Name", "Website", "Home Stadium"]))

    if len(season):
        query = (
            "SELECT playerName, nationality, `position` "
            "FROM player INNER JOIN clubplayers ON player.playerID = clubplayers.playerID "
            f"WHERE clubplayers.clubName like '%{team[0]}%' AND season like '{season}' "
            "ORDER BY 3; "
        )
        res = queryFetchAll(query)
        print(tabulate(res, headers = ["Player Name", "Nationality", "Position"]))

    else:
        seasons = ["2021/22","2020/21", "2019/20", "2018/19"]
        for season in seasons:
            query = (
                "SELECT playerName, nationality, `position` "
                "FROM player INNER JOIN clubplayers ON player.playerID = clubplayers.playerID "
                f"WHERE clubplayers.clubName like '%{team[0]}%' AND season like '{season}' "
                "ORDER BY 3; "
            )
            print(f"\nPlayers in season {season}:")
            res = queryFetchAll(query)
            print(tabulate(res, headers = ["Player Name", "Nationality", "Position"]))
    
def retrieve_home_team_for_stadium():
    stadium = input("Stadium: ")
    query = f"SELECT clubName, homeStadium FROM club WHERE homeStadium like '%{stadium}%';"
    res = queryFetchOne(query)

    if res is None:
        print("Not in our database!")
    else:
        print(tabulate([res], headers = ["Team Name", "Home Stadium"]))
    
def retrieve_teams_in_city():
    city = input("City: ")
    query = f"SELECT clubName, city FROM club INNER JOIN stadium ON club.homeStadium = stadium.stadiumName WHERE city like '%{city}%'"
    res = queryFetchAll(query)

    if res is None:
        print("Not in our database!")
    else:
        print(tabulate(res, headers = ["Team Name", "City"])) 

def retrieve_players_for_nationality():
    nationality = input("Nationality: ")
    query = (
        "SELECT playerName, nationality, `position`, birthDate, height, weight, clubName, season "
        f"FROM player INNER JOIN clubplayers ON player.playerID = clubplayers.playerID WHERE nationality LIKE '%{nationality}%';"
    )
    res = queryFetchAll(query)

    if len(res) == 0:
        print("No players with this nationality!")
    else:
        print(tabulate(res, headers = ["Player Name", "Nationality", "Position", "Bith Date", "Height", "Weight", "Club Name", "Season"]))

def retrieve_player():
    first = input("First Name: ")
    last = input("Last Name: ")
    query = f"SELECT playerName, nationality, `position`, birthDate, height, weight FROM player WHERE playerName like '{first}%{last}';"
    res = queryFetchAll(query)

    if len(res) == 0:
        print("No players with this name!")
    else:
        print(tabulate(res, headers = ["Player Name", "Nationality", "Position", "Bith Date", "Height", "Weight"]))

def retrieve_players_by_position():
    print("Choose a position:")
    print("   1. Defender")
    print("   2. Forward")
    print("   3. Goalkeeper")
    print("   4. Midfielder")

    position = int(input("Position: "))
    map_to_position = {1: "Defender", 2: "Forward", 3: "Goalkeeper", 4: "Midfielder"}

    position = map_to_position[position]

    query = f"SELECT playerName, nationality, `position`, birthDate, height, weight FROM player WHERE `position` like '%{position}%';"
    res = queryFetchAll(query)


    print(tabulate(res, headers = ["Player Name", "Nationality", "Position", "Bith Date", "Height", "Weight"]))


if __name__ == "__main__":
    welcome()
    options_page()  

    
