# ZCAL
#### Video Demo:  <URL HERE>
#### Description:

A calendar app for scheduling meetings between teachers and students.

# Background

I work for an English education company in Japan, and with the events of this year, we suddenly
discovered that we needed to branch out into online learning.  Our primary platform for this was Zoom.

I decided to create a system where students could reserve a meeting with a teacher at a time of their choosing
via a calendar interface.  To be completely honest, I got a little carried away...

# Capablities

## With Zcal, administrators can:

Create new student, teacher or administrator accounts
Access the calendar of any student, teacher or administrator
Delete user accounts
Modify user account information for other users (as well as themselves)
Add Zoom accounts to the system (via Zoom's oauth authentication system)
Attach Zoom accounts to teachers
    (My company decided to only purchase about 10 Zoom accounts to be shared between all teachers, therefore I couldn't set it up for each teacher to register with their own zoom account or something like that, because if a teacher leaves, their account would have to be reassigned to a different teacher.)
Unattach Zoom accounts from teachers
Delete Zooom accounts from the system
Create courses, which are associated with students (Each student must have a course associated with them)
Delete courses
Create time slots for meetings
Assign or remove time slots from teachers' schedules
Schedule meetings between teachers and students (by accessing a student's calendar) - This actually schedules a meeting on the teacher's associated zoom account via the zoom api, and sends the meeting information to the teacher and the student via email.
Delete meetings - This actually deletes the meeting via the zoom api.
Log in, log out, and all that fun stuff.

## Students and teachers can:

Access their own calendar
View their scheduled meetings on the calendar
Change their own user account information
Log in, log out, and all that fun stuff.

## Students can:

Schedule meetings for themselves with the teacher of their choice.
Delete meetings that they have scheduled

# Files.. or rather, Folders

The project as a whole has become quite large, to the point where I found that I needed to sort everything into folders. Rather than go through each and every file, I'll go through all of the folders, and go over a bit of what's inside.

## zcal-repo folder

This is the base folder for the project. A number of the files and folders therein were created for the purpose of making the project installable, but the most important things there are as follows:

### dbinit.py

This is a small program that I wrote (before I discovered what unit testing is), that tests all of the sqlalchemy models to make sure that everything works the way that it's supposed to.  At some point, I realized that I could also use the file to reset the database to the state that it needs to be in when you first set up the app.  

### tests folder

At some point the project became so huge that I realized it was a huge pain to test everything every time I changed something.  This lead me to learn how to implement unit testing.  Unfortunately, the project at that point was also so huge that going through and writing tests for everything turned out to be unrealistic given the fact that it wasn't actually going to be used.  That's why tests are only written for a few areas of the app.

### zcal folder

#### __init__.py

This is of course where the app, the configuration, database and various other add-ins are initialized and blueprints are registered.

#### admin, auth, cal, day, meeting, users, zoom

Each of these folders contains the code and wtforms forms corresponding to the names thereof.

# Decisions

Two decisions that had a really big impact on thisproject were deciding to use both wtforms and sqlalchemy.  In the process of figuring out how to implement the project, I wound up watching tutorials about both of these tools, and decided to give them a try.  In hindsight, I think I learned a lot about how to learn new tools, but especially in the case of sqlalchemy, I could have probably used the practice writing my own queries.. Oh well, I suppose I can always go back and redo the SQL labs to review.

# Challenges

## Calendar

The first big challenge that I had was figuring out how to create a calendar on screen.  I now have a much greater appreciaion for just how well-designed google calendar is.  It was very difficult to get the grid to be big enough to work in multiple device sizes, and still doesn't do so as well as I'd like. 

## Zoom API

By far, the biggest challenge of this project was figuring out how to access zoom via the API.  After figuring out how to do it initially using another system... I don't remember off the top of my head, I later realized that I would need to do it using Oauth2 instead.  This took a lot of time and an incredible amount of trial and error, but I'm really happy that I did it, since if I were to take on another project that interacts with google, facebook, etc. I'd feel a lot more comfortable using Oauth to access their APIs.

# Conclusion

There's still a ton that COULD be done to improve this project  (especially on the front end), but It's not actually
going to be used, and I think I'm ready to move on.


## CS50 has been great!  I can't wait to continue my programming adventure!