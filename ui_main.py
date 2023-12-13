import db_access
import getpass, datetime
from sys import argv

#DB_PATH = "test1.db"
DB_PATH = argv[1]



def main():
    db_access.connect(DB_PATH)

    while True:
        print("1. Login\n2. Register\n3. Exit")
        usrin = input("Enter selection: ")
        if usrin == "1":
            uid = login() 
            break
        elif usrin == "2":
            uid = register() 
            break
        elif usrin == "3":
            return
    #TODO: some way to cancel, exit out of login/register menu

    welcome_back_page(uid)

    #main control flow, select options
    while True:
        print("Available actions:\n1. Search for tweets\n2. Search for users\n3. Write tweet\n4. List followers\n5. View feed\n6. Log out")
        choice = input("Select an option: ")
        if choice == "1":
            search_tweets(uid)
        elif choice == "2":
            search_users(uid)
        elif choice == "3":
            write_tweet(uid)
        elif choice == "4":
            list_followers(uid)
        elif choice == "5":
            home_page_tweets(uid)
        elif choice == "6":
            break
        else:
            print("Invalid selection")


def login() -> int:
    while True:
        uid = input("Enter user id: ")
        try:
            uid = int(uid)
        except:
            print("Invalid user id")
            continue
        password_hash = getpass.getpass("Enter password: ")
        valid= db_access.check_login(uid, password_hash)
        if valid:
            return uid
        else:
            print("Invalid login")

def register() -> int:
    uid = db_access.get_new_uid()
    print(f"Your UID will be: {uid}. Remember this UID for logging in")
    
    while True:
        pass1 = getpass.getpass("Enter a password: ")
        pass2 = getpass.getpass("Re-enter password: ")
        if len(pass1) < 6:
            print("Password must be at least 6 characters")
        elif pass1 == pass2:
            break
        else:
            print("Passwords do not match, please try again")
        #TODO more requirements?
    
    while True:
        name = input("Enter your name: ")
        if len(name) < 2:
            print("Name must be at least 2 characters")
        else:
            break
    email = input("Enter an email: ") #TODO validate
    city = input("Enter city: ")
    while True:
        try:
            timezone = (input("Enter timezone as offset from UTC: "))#TODO valudate input
            if len(timezone) == 0:
                break
            timezone = float(timezone)
        except:
            print("Invalid timezone. Must be a whole number from -12 to +14")
            continue
        else:
            break
    db_access.register_user(uid, pass1, name, email, city, timezone)
    return uid


def welcome_back_page(uid:int) -> None:
    #print some welcome message, date idk
    #print tweets from followed users
    name = db_access.get_user_name(uid)
    print(f"\nWelcome back, {name}")
    print(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    print("============")
    #feed = db_access.get_tweets_by_followee(uid)
    #display_tweets(uid, feed)
    home_page_tweets(uid)

def home_page_tweets(uid:int):
    tweets = db_access.get_followers_tweets(uid)
    print("Your feed")
    display_tweets(uid, tweets)
    return


#functions for the options
def search_tweets(uid:int):
    """
    If there are more than 5 matching tweets, only 5 would be shown 
        and the user would be given an option to see more but again 5 at a time.
    The user should be able to select a tweet and see some statistics about the tweet 
        including the number of retweets and the number of replies.
    Also the user should be able to compose a reply to a tweet 
        (see the section on composing a tweet), 
        or retweet it (i.e. repost it to all people who follow the user).
    """
    kwds = input("Enter keywords to search by: ").split()
    if len(kwds) == 0:
        print("No keywords entered")
        return
    matching_tweets = db_access.get_tweets_by_kwd(kwds)
    display_tweets(uid, matching_tweets)

def display_tweets(uid:int, matching_tweets:list) -> None:
    if len(matching_tweets) == 0:
        print("No tweets found")
        return

    start=0
    while True:
        print()
        for i in range(start, start+5):
            try:
                print(f"{i-start+1}.   Tweet id: {matching_tweets[i]['tid']}")
                print(f"From: {matching_tweets[i]['name']:20}     On: {matching_tweets[i]['tdate']}")
                print('"' + matching_tweets[i]["text"] +'"\n')
            except IndexError:
                print("End of search")
                break
        
        if start != 0:
            print("< View Previous")
        if start+5 < len(matching_tweets):
            print ("> View Next")
        print ("(1-5) Select Tweet")
        print ("q Home")
        
        usrin = input("Selection: ")
        if (usrin == "q"):
            return
        elif (usrin == "<" and i!=0):
            start -= 5
            continue
        elif (usrin == ">" and i!=0):
            start += 5
            continue
        try:
            usrin = int(usrin)
        except:
            print("Invalid entry")
            continue
        if (usrin <= 0 or usrin > i):
            print("Invalid index")
            continue

        selected_index = start+usrin-1
        if selected_index < 0 or selected_index >= len(matching_tweets):
            print("invalid index")
            continue
        
        retweets, replies = db_access.get_tweet_stats(matching_tweets[selected_index]['tid'])

        while True:
            print(f"{retweets} retweets, {replies} replies")
            if matching_tweets[selected_index]['writer'] != uid:
                print("r Retweet")
            print("t Reply\nq Exit")
            usrin = input("Enter selection: ")
            if usrin == "r" and matching_tweets[selected_index]['writer'] != uid:
                if not db_access.retweet(uid, matching_tweets[selected_index]['tid']):
                    print("You have previously retweeted this tweet")
            elif usrin == "t":
                write_tweet(uid, replyto=matching_tweets[selected_index]['tid'])
            elif usrin == "q":
                break
            else:
                print("Invalid action")


def search_users(uid:int):
    """
    If there are more than 5 matching users, only 5 would be shown 
        and the user would be given an option to see more but again 5 at a time.
    The user should be able to select a user and see more information about him/her 
        including the number of tweets, the number of users being followed, 
        the number of followers and up to 3 most recent tweets.
    The user should be given the option to follow the user or see more tweets.
    """  
    
    kwd = input("Enter keyword to search by: ")
    matching_users = db_access.get_users_by_kwd(kwd)

    # print(len(matching_users))
    if len(matching_users) == 0:
        print("No users found")
        return
    
    
    # USER BROWSER FEATURE HERE
    start=0
    while True:
        print()
        for i in range(start, start+5):
            try:
                print(f"{i-start+1}.   User id: {matching_users[i]['usr']}")
                print(f"Name: {matching_users[i]['name']:20}  City: {matching_users[i]['city']}\n")
            except IndexError:
                print("End of search")
                break
        
        if start != 0:
            print("View Previous: <")
        if start+5 < len(matching_users):
            print("View Next:     >")
        print("Select User: (1-5)")
        print("Exit: q")
        
        usrin = input("Selection: ")
        if (usrin == "q"):
            return
        elif (usrin == "<" and start >= 5):
            start -= 5
            continue
        elif (usrin == ">" and start >= 0 and (start+5) < len(matching_users)):
            start += 5
            continue
        try:
            usrin = int(usrin)
            if usrin > len(matching_users):
                print("Invalid entry")
                continue
        except:
            print("Invalid entry")
            continue
        if (usrin <= 0 or usrin > i):
            print("Invalid index")
            continue
        
        selected_index = start+usrin-1
        if selected_index < 0 or selected_index >= len(matching_users):
            print("invalid index")
            continue
        
        user_details(uid, [matching_users[selected_index]['name'], matching_users[selected_index]['usr']])
            
def user_details(uid, user_data:list):
    number_of_tweets_displayed = 3
    tweet_index=0
    while True:
        data = db_access.get_user_details(user_data[1])
        # [number_of_tweets, following_amount, follower_count, tweets]
        print(f"\nSelected user {user_data[0]}")
        
        print(f"Number of tweets: {data[0]}")
        print(f"Number of followers: {data[2]}")
        print(f"Number of following: {data[1]}")
        tweets = data[3]
                        
        # displays tweets
        print("Tweets:")
        if len(tweets) == 0:
            print("No tweets from this user.")
        else:
            for i in range(tweet_index, tweet_index+number_of_tweets_displayed):
                try:
                    name = db_access.get_user_name(tweets[i]['writer'])
                    print(f"{i-tweet_index+1}. {tweets[i]['text']:30}    On: {tweets[i]['tdate']}")  # DO WE NEED THE NAME? LMK
                except IndexError:
                    print("End of search")
                    break
        print()
        
        # displays user interface
        if tweet_index != 0:
            print("View Previous: <")
        if tweet_index+number_of_tweets_displayed < len(tweets):
            print ("View Next:    >")
        print(f"Follow {user_data[0]}: f")
        print ("Exit: q")
        
        # user input selection
        usrin = input("Selection: ")
        if (usrin == "q"):
            break
        elif (usrin == "<" and tweet_index >= number_of_tweets_displayed):
            tweet_index -= number_of_tweets_displayed
            continue
        elif (usrin == ">" and (tweet_index+number_of_tweets_displayed) <= len(tweets)):
            tweet_index += number_of_tweets_displayed
            continue
        
        # follow option 
        elif (usrin == "f"):
            follow = db_access.follow_user(uid, user_data[1])
            if follow == True:
                print(f"You are now following {user_data[0]}")
            elif follow == 100:
                print(f"You cannot follow yourself!")
            else:
                print(f"You are already following {user_data[0]}")
            continue
        else:
            print("Invalid entry")
            continue
        
    return

                        
def write_tweet(uid: int, replyto:int=None):
    """
    The user should be able to compose a tweet.
    A tweet can have hashtags which are marked with a # before each hashtag.
    Information about hashtags must be stored in tables mentions and if needed in hashtags.
    """
    tweet_text = input("Enter tweet text: ") # tweet is one paragraph for simplicity?

    # scan for hashtags:
    hashtags = []
    start = None

    tweet_text_l = tweet_text.lower()
    for i, char in enumerate(tweet_text_l):
        if char == '#' and start is None:
            start = i + 1
        elif char == ' ' and start is not None:
            hashtags.append(tweet_text_l[start:i])
            start = None
        elif char == '#' and start is not None:
            hashtags.append(tweet_text_l[start:i])
            start = i + 1
    if start is not None:
        hashtags.append(tweet_text_l[start:])

    #print("Found hashtags: ", hashtags)

    db_access.add_tweet(writer=uid, tweet_text=tweet_text, hashtags=hashtags, replyto=replyto)


def list_followers(uid:int ):
    """
    The user should be able to list all users who follow them.
    From the list, the user should be able to select a follower and see more information 
        about the follower including the number of tweets, the number of users being followed, 
        the number of followers and up to 3 most recent tweets.
    The user should be given the option to follow the selected user or see more tweets.
    """
    followers = db_access.get_followers(uid)
    if len(followers) == 0:
        print("You have no followers.")
        return
    start=0
    while True:
        print()
        for i in range(start, start+5):
            try:
                print(f"{i-start+1}. Name: {followers[i]['name']:20}  CITY: {followers[i]['city']}")
            except IndexError:
                print("End of search")
                break
        
        if start != 0:
            print("View Previous: <")
        if start+5 < len(followers):
            print ("View Next:    >")
        print ("Select User (1-5): ")
        print ("Exit: q")
        
        usrin = input("Selection: ")
        if (usrin == "q"):
            return
        elif (usrin == "<" and start >= 5):
            start -= 5
            continue
        elif (usrin == ">" and start >= 0 and (start+5) < len(followers)):
            start += 5
            continue
        try:
            usrin = int(usrin)
            if usrin > len(followers):
                print("Invalid entry")
                continue
        except:
            print("Invalid entry")
            continue
        if (usrin <= 0 or usrin > 5):
            print("Invalid index")
            continue
        else:
            selected_index = start+usrin-1
            
            name = followers[selected_index]['name']
            user = followers[selected_index]['flwer']
            
            user_details(uid, [name, user])
            
            continue
    # print('\n')

if __name__ == "__main__":
    main()
