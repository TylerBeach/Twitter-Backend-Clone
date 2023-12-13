import sqlite3
from datetime import datetime

connection = None
cursor = None



def connect(path) -> None:
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(' PRAGMA foreign_keys=ON; ')
        connection.commit()
    except:
        print("Failed to connect to database")
        exit(100)


def check_login(uid: int, password:str) -> bool:
    
    #TODO do input validation to prevent SQL injection
    global connection, cursor
    cursor.execute("SELECT usr, pwd FROM users WHERE usr=:uid AND pwd=:password", 
                {"uid":uid, "password":password})
    matching_user = cursor.fetchall()
    if len(matching_user) == 0: 
        return False
    if len(matching_user) == 1:
        return True
    print("How is there more than one user being return brother")
    return False


def get_new_uid() -> int:
    cursor.execute("SELECT MAX(usr) FROM users")
    return cursor.fetchone()[0] +1


def register_user(usr:int, pwd:str, name:str, email:str, city:str, timezone:float) -> None:
    cursor.execute("INSERT INTO users VALUES (:usr, :pwd, :name, :email, :city, :timezone)", 
                   {"usr":usr, "pwd":pwd, "name":name, "email":email, "city":city, "timezone":timezone})
    connection.commit()
    # this changes the actual database 
    # do we want this?
    # users will still show up if u register them without it 
    # connection.commit() just pushes them to the actual database if u get what i mean


def get_tweets_by_followee(uid:int):
    """
    After a registered user signs in, the system should list all tweets or retweets
    from users who are being followed;
    the tweets should be ordered based on date
    from the latest to the oldest.
    """


def get_tweets_by_kwd(kwds):
    """
    A tweet matches a keyword if:
    (1) the keyword has the prefix # and it is mentioned by the tweet as a hashtag in mentions table
    OR
    (2) the keyword doesn't have the prefix # and it appears in the tweet text.
    (The symbol # is not part of any keyword and only indicates that the keyword that follows is expected to appear as a hashtag.
    Also tweets can have hashtags (in mentions table) which do not explicitly appear in the tweet text.)
    The tweets should be ordered based on date from the latest to the oldest.
    """
    #return all tweet data, plus the name of the author
    # SELECT t.tid, u.name, t.tdate, t.text, t.replyto FROM tweets t, user u WHERE t.writer = u.usr
    global connection, cursor
    
    query = "SELECT DISTINCT t.tid, t.writer, u.name, t.tdate, t.text, t.replyto FROM tweets t, users u, mentions m WHERE t.writer = u.usr AND ("

    query_kwds = []
    for i in range(len(kwds)):
        print(kwds[i])
        if kwds[i][0] == '#':
            kwds[i] = kwds[i][1:].lower()
            query_kwds.append(f"(LOWER(m.term) = ? AND m.tid=t.tid)")
        else:
            kwds[i] = "%" + kwds[i].lower() + "%"
            query_kwds.append(f"(LOWER(t.text) LIKE ?)")
    query += " OR ".join(query_kwds)
    query += ") ORDER BY tdate"

    cursor.execute(query, kwds)
    return cursor.fetchall()


def get_tweet_stats(tid:int) -> (int, int):
    """
    Gets the number of retweets and replies for a given tweet
    """
    #query the number of retweets for the given tweet
    rt_query = 'SELECT COUNT(*) FROM retweets WHERE tid = :tid'
    #query the number of replys for the given tweet
    rply_query = 'SELECT COUNT(*) FROM tweets WHERE replyto = :tid'

    #execute the queries
    cursor.execute(rt_query, {'tid':tid})
    rt_count = cursor.fetchone()[0]
    
    cursor.execute(rply_query, {'tid':tid})
    rply_count = cursor.fetchone()[0]

    #returns a tuple with the retweet count and reply count
    return rt_count, rply_count


def retweet(uid:int, tid:int) -> None:
    """
    Retweets a given tweet as a given user
    """
    #check if tweet with tid exists
    cursor.execute('SELECT COUNT(*) FROM tweets WHERE tid=:tid',{'tid':tid})
    t_exists = cursor.fetchone()[0]
    
    if t_exists:
        rt_date = datetime.now().strftime("%Y-%m-%d")
        try:
            cursor.execute('INSERT INTO retweets (usr, tid, rdate) VALUES (:uid, :tid, :rt_date)', {'uid':uid, 'tid':tid, 'rt_date':rt_date})
        except sqlite3.IntegrityError as e:
            return False
        else:
            connection.commit()
            return True


def get_users_by_kwd(kwd:str):
    """
    The result would be sorted as follows:
    first, all users whose name match the keyword would be listed and these users would be sorted in an ascending order of name length.
    This would be followed by the list of users whose city but not name match the keyword and this result would be sorted in an ascending order of city length
    """
    # need 2 queries i think

    # IDK IF THE FUNCTION RETURNS THE PROPER THING FOR CITY BECAUSE EVERYONE HAS A UNIQUE CITY 
    query = """
            SELECT usr, name, city
            FROM users
            WHERE LOWER(name) LIKE LOWER(:kwd)
            ORDER BY LENGTH(name) ASC;
            """
    query2 = """
            SELECT usr, name, city
            FROM users
            WHERE city LIKE :kwd AND name NOT LIKE :kwd
            ORDER BY 
                CASE WHEN name LIKE :kwd THEN LENGTH(name) ELSE NULL END ASC,
                CASE WHEN city LIKE :kwd AND name NOT LIKE :kwd THEN LENGTH(city) ELSE NULL END ASC;
            """
    global connection, cursor
    cursor.execute(query, 
                  {"kwd":f"%{kwd}%"})
    data_list = cursor.fetchall()

    cursor.execute(query2, 
                  {"kwd":f"%{kwd}%"})
    data_list2 = cursor.fetchall()

    # print(data_list)
    # print(data_list2)

    combined_list = data_list + data_list2
    # print(combined_list)
    
    return combined_list


def add_tweet(writer:int, tweet_text:str, hashtags, replyto:int = None, tdate=None) -> None:
    # add tweet to tweets, tweet+hashtag to mentions, hashtag to hashtag if new
    # tweet id is sequential, find max and +1
    # writer is uid
    # tdate can be current date but better if passed in
    # text is given
    # replyto can be optional parameter because same function for new tweet and reply
    #Just INSERT INTO ... with the given info, handle errors tho just in case

    #find and increase max tid
    cursor.execute('SELECT MAX(tid) FROM tweets')
    curr_tid = cursor.fetchone()[0]
    new_tid = curr_tid + 1 if curr_tid != None else 1

    #if tdate is not provided, use current date
    if tdate == None:
        tdate = datetime.now().strftime("%Y-%m-%d")
    try:
        #insert tweet into tweets table
        cursor.execute('INSERT INTO tweets (tid, writer, tdate, text, replyto) VALUES (:new_tid, :writer, :tdate, :tweet_text, :replyto)', 
                       {'new_tid':new_tid, 'writer':writer, 'tdate':tdate, 'tweet_text':tweet_text, 'replyto':replyto})

        #insert hashtags into hashtag table if new hashtag
        #insert tid and hashtag into mentions table
        for hashtag in hashtags:
            cursor.execute('INSERT OR IGNORE INTO hashtags VALUES (:hashtag)', {'hashtag':hashtag})
            cursor.execute('INSERT INTO mentions VALUES (:new_tid, :hashtag)', {'new_tid':new_tid, 'hashtag':hashtag})
    except Exception as e:
        #rollback changes and exit
        connection.rollback()
        raise Exception(e)
    else:
        connection.commit()
        

def get_followers(uid:int) -> list:
    """
    The user should be able to list all users who follow them.
    From the list, the user should be able to select a follower and see more information 
        about the follower including the number of tweets, the number of users being followed, 
        the number of followers and up to 3 most recent tweets.
    The user should be given the option to follow the selected user or see more tweets.
    """
    # SHOULD RETURN UID AND NAME 


    global connection, cursor
    cursor.execute("SELECT name, flwer, city FROM follows, users WHERE flwee=:uid AND flwer=users.usr ORDER BY LENGTH(name) ASC", 
                  {"uid":uid})
    flwer_list = cursor.fetchall()

    # print(len(flwer_list))
    
    # print(flwer_list)
  
    return flwer_list


def get_following_amount(uid:int) -> int:
    """
    The user should be able to list all users who follow them.
    From the list, the user should be able to select a follower and see more information 
        about the follower including the number of tweets, the number of users being followed, 
        the number of followers and up to 3 most recent tweets.
    The user should be given the option to follow the selected user or see more tweets.
    """

    global connection, cursor
    cursor.execute("SELECT COUNT(*) FROM follows WHERE flwer=:uid", 
                  {"uid":uid})
    following_count = cursor.fetchone()[0]

    # print(flwer_list)
    
    return following_count


def get_user_tweets(uid:int) -> list:
    """
    The user should be able to list all users who follow them.
    From the list, the user should be able to select a follower and see more information 
        about the follower including the number of tweets, the number of users being followed, 
        the number of followers and up to 3 most recent tweets.
    The user should be given the option to follow the selected user or see more tweets.
    """

    global connection, cursor
    cursor.execute("SELECT tid, writer, tdate, text, replyto FROM tweets WHERE writer=:uid AND replyto IS NULL", 
                  {"uid":uid})
    tweet_list = cursor.fetchall()

    # print(flwer_list)
   
    return tweet_list


def get_user_details(uid:int) -> list:
    """
    THIS FUNCTION IS A COMPLIMENT TO THE GET FOLLOWERS FUNCTION 
    THE GET FOLLOWERS FUNCTION should just get the followers of that uid 
    in this function the user selects a user from the list given of get_followers
    and more details are given about them
    """

    number_of_tweets = len(get_user_tweets(uid))
    following_amount = get_following_amount(uid)
    follower_count = len(get_followers(uid))
    
    # UP TO 3 MOST RECENT TWEETS
    tweets = get_user_tweets(uid)
  
    return [number_of_tweets, following_amount, follower_count, tweets]


def get_user_name(usr):
    global connection, cursor
    cursor.execute("SELECT name FROM users WHERE usr=:usr", 
                  {"usr":usr})
    name = cursor.fetchone()[0]
    return name


def follow_user(flwer, flwee):
    global connection, cursor
    
    if flwer == flwee:
        return 100
    
    cursor.execute("SELECT flwer FROM follows, users WHERE flwer=:flwer AND flwee=:flwee", 
                  {"flwer":flwer, "flwee":flwee})
    flwer_list = cursor.fetchall()
    if len(flwer_list) == 0:
        cursor.execute("INSERT INTO follows (flwer, flwee) VALUES (:flwer, :flwee)", 
                    {"flwer":flwer, "flwee":flwee})
        connection.commit()  #   THIS WILL ACTUALLY ADD THEM TO DB
        # ^ IF U DO THAT IT WILL BE IN THE DATA BASE UNTIL YOU RE-LOAD THE load_test1.sql FILE
        return True
    else:
        return False
    
    
def get_followers_tweets(uid: int):
    """
    Retrieves all tweets from users who are being followed by the given user (`uid`),
    ordered from the latest to the oldest.
    """
    global connection, cursor

    # First, we get the list of users that `uid` is following
    cursor.execute("""
        SELECT flwee
        FROM follows
        WHERE flwer = :uid
    """, {"uid": uid})

    # Get the list of all users that are followed by `uid`
    followed_users = cursor.fetchall()

    # Now we retrieve tweets from these users
    tweets = []
    if followed_users:
        # Construct a query to select tweets from followed users
        # We use the tuple of followed user IDs to ensure the SQL "IN" clause works properly
        followed_user_ids = tuple(user['flwee'] for user in followed_users)
        placeholder = '?'  # SQLite uses "?" as placeholder for parameters
        placeholders = ', '.join(placeholder for unused in followed_user_ids)

        cursor.execute(f"""
            SELECT t.tid, t.writer, u.name, t.tdate, t.text, t.replyto
            FROM tweets t
            JOIN users u ON t.writer = u.usr
            WHERE t.writer IN ({placeholders})
            ORDER BY t.tdate DESC
        """, followed_user_ids)

        tweets = cursor.fetchall()

    return tweets
