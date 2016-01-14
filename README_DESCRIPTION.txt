Swatspot is an app that is intended to provide real time information on the level of crowdedness of the only dining hall,
Sharples, at Swarthmore College. A button is placed in Sharples that students press upon entry, which then sends a signal
to the server running the code on this repository (to a specific URL). Upon receiving a signal these programs will log that a
person arrived in the dining hall at this time. When a user goes on the website (a different URL), the program 
studentsView.py will compute how busy Sharples is right now against all other time and display this information to the user
outputting a percentile where 0% is vacant and 99.9% is as crowded as we have ever seen. 
By making the assumption that a student stays for 40 minutes at Sharples, this program can compute
how busy the current state of Sharples is against all historical levels. In order to have historical data for 
comparison as soon as it became live data from student meal card swipes by the minute were input to the system 
(courtesy of Lynn Grady and Linda McDougall, co-heads of the Sharples dining staff). 


Demo: 
The website was run for two and a half days on an Amazon Web Service server running a Django web framework 
and was able to obtain accurate results for a good part of the time. The most serious problems with the results were that
students would sometimes press the button many times to see if it would respond. After leaving it in the dining hall for 
several days, the raspberry-pi development board beneath the button was damaged and could no longer send signals to the server.

