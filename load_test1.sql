-- Let's drop the tables in case they exist from previous runs
drop table if exists includes;
drop table if exists lists;
drop table if exists retweets;
drop table if exists mentions;
drop table if exists hashtags;
drop table if exists tweets;
drop table if exists follows;
drop table if exists users;

create table users (
  usr         int,
  pwd	      text,
  name        text,
  email       text,
  city        text,
  timezone    float,
  primary key (usr)
);
create table follows (
  flwer       int,
  flwee       int,
  start_date  date,
  primary key (flwer,flwee),
  foreign key (flwer) references users,
  foreign key (flwee) references users
);
create table tweets (
  tid	      int,
  writer      int,
  tdate       date,
  text        text,
  replyto     int,
  primary key (tid),
  foreign key (writer) references users,
  foreign key (replyto) references tweets
);
create table hashtags (
  term        text,
  primary key (term)
);
create table mentions (
  tid         int,
  term        text,
  primary key (tid,term),
  foreign key (tid) references tweets,
  foreign key (term) references hashtags
);
create table retweets (
  usr         int,
  tid         int,
  rdate       date,
  primary key (usr,tid),
  foreign key (usr) references users,
  foreign key (tid) references tweets
);
create table lists (
  lname        text,
  owner        int,
  primary key (lname),
  foreign key (owner) references users
);
create table includes (
  lname       text,
  member      int,
  primary key (lname,member),
  foreign key (lname) references lists,
  foreign key (member) references users
);






-- Insert test data
-- Inserting data into the 'users' table
INSERT INTO users (usr, pwd, name, email, city, timezone)
VALUES
  --actual passwords are password1, password2 ...
  (1, 'password1', 'John Doe', 'john.doe@example.com', 'New York', -5.0),
  (2, 'password2', 'Jane Smith', 'jane.smith@example.com', 'Los Angeles', -8.0),
  (3, 'password3', 'Bob Johnson', 'bob.johnson@example.com', 'Chicago', -6.0),
  (4, 'password4', 'Alice Williams', 'alice.williams@example.com', 'Houston', -6.0),
  (5, 'password5', 'Eve Davis', 'eve.davis@example.com', 'Miami', -5.0),
  (6, 'password6', 'Charlie Brown', 'charlie.brown@example.com', 'San Francisco', -8.0),
  (7, 'password7', 'Grace Taylor', 'grace.taylor@example.com', 'Seattle', -8.0),
  (8, 'password8', 'Olivia Johnson', 'olivia.johnson@example.com', 'San Diego', -7.0),
  (9, 'password9', 'David Brown', 'david.brown@example.com', 'Denver', -6.0),
  (10, 'password10', 'Sophia Wilson', 'sophia.wilson@example.com', 'Denver', -5.0),
  (11, 'password11', 'Liam Martinez', 'liam.martinez@example.com', 'Dallas', -6.0),
  (12, 'password12', 'Ava Anderson', 'ava.anderson@example.com', 'Phoenix', -7.0),
  (13, 'password13', 'Mason Taylor', 'mason.taylor@example.com', 'Philadelphia', -5.0),
  (14, 'password14', 'Emily Wilson', 'emily.wilson@example.com', 'San Antonio', -6.0),
   (15, 'password15', 'Johnny Appleseed', 'johnny.appleseed@example.com', 'Portland', -8.0),
  (16, 'password16', 'Johnathan Smith', 'johnathan.smith@example.com', 'Atlanta', -5.0),
  (17, 'password17', 'Ann Johnson', 'ann.johnson@example.com', 'Minneapolis', -6.0),
  (18, 'password18', 'Betty Johnson', 'betty.johnson@example.com', 'Las Vegas', -8.0),
  (19, 'password19', 'John Jacob', 'john.jacob@example.com', 'Orlando', -5.0),
  (20, 'password20', 'Mary-John', 'maryjohn.roberts@example.com', 'Washington D.C.', -5.0);

-- Inserting data into the 'follows' table
INSERT INTO follows (flwer, flwee, start_date)
VALUES
  (1, 2, '2023-10-25'),
  (1, 3, '2023-10-26'),
  (2, 3, '2023-10-24'),
  (3, 4, '2023-10-25'),
  (4, 5, '2023-10-26'),
  (1, 4, '2023-10-27'),
  (4, 6, '2023-10-28'),
  (5, 7, '2023-10-28'),
  (6, 7, '2023-10-30'),
  (8, 9, '2023-10-31'),
  (10, 11, '2023-11-01'),
  (12, 13, '2023-11-02'),
  (14, 1, '2023-11-03'),
  (2, 8, '2023-11-04'),
  (3, 9, '2023-11-05');

-- Inserting data into the 'tweets' table
INSERT INTO tweets (tid, writer, tdate, text, replyto)
VALUES
  (1, 1, '2023-10-25', 'Hello world!', NULL),
  (15, 1, '2023-10-25', 'My second tweet!', NULL),
  (16, 1, '2023-10-25', 'OMG SLAY!', NULL),
  (17, 1, '2023-10-25', 'Brotha!', NULL),
  (18, 1, '2023-10-25', 'Amen Sisters!', NULL),
  (2, 2, '2023-10-26', 'Just testing.', NULL),
  (3, 3, '2023-10-24', 'SQL is fun!', NULL),
  (4, 4, '2023-10-25', 'Good morning!', NULL),
  (5, 5, '2023-10-26', 'Having a great day!', NULL),
  (6, 6, '2023-10-27', 'I love this city!', NULL),
  (7, 7, '2023-10-28', 'Exploring new places.', NULL),
  (8, 8, '2023-10-30', 'Enjoying the sunshine.', NULL),
  (9, 9, '2023-10-31', 'Coding all day!', NULL),
  (10, 10, '2023-11-01', 'New book recommendation.', NULL),
  (11, 11, '2023-11-02', 'Morning coffee is the best!', NULL),
  (12, 12, '2023-11-03', 'Trying a new recipe.', NULL),
  (13, 13, '2023-11-04', 'Exploring the city.', NULL),
  (14, 14, '2023-11-05', 'Just a random thought.', NULL);


-- Inserting data into the 'hashtags' table
INSERT INTO hashtags (term)
VALUES
  ('test'),
  ('sql'),
  ('coding'),
  ('fun'),
  ('goodmorning'),
  ('citylife'),
  ('adventure'),
  ('sunshine'),
  ('codinglife'),
  ('books'),
  ('coffee'),
  ('cooking'),
  ('randomthought');

-- Inserting data into the 'mentions' table
INSERT INTO mentions (tid, term)
VALUES
  (1, 'coding'),
  (2, 'test'),
  (3, 'sql'),
  (4, 'goodmorning'),
  (5, 'fun'),
  (6, 'citylife'),
  (7, 'adventure'),
  (8, 'sunshine'),
  (9, 'codinglife'),
  (10, 'books'),
  (11, 'coffee'),
  (12, 'cooking'),
  (13, 'citylife'),
  (14, 'randomthought');
  
-- Inserting data into the 'retweets' table
INSERT INTO retweets (usr, tid, rdate)
VALUES
  (2, 1, '2023-10-26'),
  (3, 1, '2023-10-24'),
  (4, 2, '2023-10-25'),
  (5, 2, '2023-10-26'),
  (1, 3, '2023-10-25'),
  (2, 6, '2023-10-28'),
  (3, 6, '2023-10-28'),
  (2, 7, '2023-10-29'),
  (4, 7, '2023-10-29'),
  (1, 8, '2023-11-01'),
  (2, 9, '2023-11-02'),
  (3, 10, '2023-11-03'),
  (4, 11, '2023-11-04'),
  (5, 12, '2023-11-05'),
  (6, 13, '2023-11-06'),
  (7, 14, '2023-11-07');

-- Inserting data into the 'lists' table
INSERT INTO lists (lname, owner)
VALUES
  ('Favorites', 1),
  ('Tech Enthusiasts', 2),
  ('Book Club', 3),
  ('Travel Buddies', 4),
  ('Foodies', 5),
  ('Work Colleagues', 1),
  ('Hiking Enthusiasts', 2),
  ('Reading Club', 3),
  ('Family', 6),
  ('Work Buddies', 7);

-- Inserting data into the 'includes' table
INSERT INTO includes (lname, member)
VALUES
  ('Favorites', 2),
  ('Tech Enthusiasts', 3),
  ('Book Club', 1),
  ('Travel Buddies', 5),
  ('Foodies', 4),
  ('Work Colleagues', 4),
  ('Hiking Enthusiasts', 5),
  ('Reading Club', 1),
  ('Family', 7),
  ('Work Buddies', 6),
  ('Hiking Enthusiasts', 9),
  ('Reading Club', 8);
