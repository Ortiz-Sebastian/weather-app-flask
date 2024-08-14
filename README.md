This app was developed using flask,python,html, and css
Bootstrap was also used to help with some of the design features of the html templates
jenga2 was used for some of the logic present on the html pages
The app consist of a user login and register authentication system which allows the app to get a database for the users
The user can customize their account by changing their username and email
The app also has email verification if the user wishes to change their password
The users can then search up their desired city and see the weather as of the present as well as the rest of the week
The weather information was displayed utilizing openweathermaps API endpoints
It also shows the time of the city in "military time" as well as the full date
On the same page, users can add that city to their saved citys so that they can see the current weather of every city they save
They can also click on each city in saved cities to see that citys weather page as mentioned above
The user may also delete citys as they wish on the mycities route
The mycities page lets the user select the units for which they want their saved cities to be displayed, the program gets the users frequently used units and uses that as the intitial unit thats being displayed 
The app utilizes SQL in order to accomplish the task of getting the saved cities of each user as well as querying each city for the user.
SQLAlchemy was used for the SQL aspect of the pogram
