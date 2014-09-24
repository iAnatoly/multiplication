multiplication
==============

Multiplication training script for elementary school (grades 3-4).

Well, every parent probably knows that elementary schools want their students to learn the multiplication table.
In 3rd grade, students are required to solve 100 mutiplication problems in 5 minutes. 
In 4th grade, the time constraint goes down to 3 minutes, which is not really possible without daily training.

I was lookuing for some kind of an application that is capable of doing the time trial, but to no avail.
Also, almost all training software is missing vitally important statistics - how many problems were answered, how many of them incorrectly, which problems took the longest to solve.
As a result, I wrote this simple python script that does exacttly this, end even sends the statistics to me over the email (so I always know about my daughter's progress).

Right now, the scrip supports mutiplication and division, and has 4 modes of operation:
- Simple training (time and errors are counted, but time limits are not enforced, and student can make multiple errors)
- Precision training (the trial stops after first mistake)
- Time trial (time limit is enforced)
- SPARTA mode (time trial + precision)

The script relies on several python modules:
- smtplib and MIMEText, for sending the statistics over the email;
- enum (or enum34, for python 2.x) - sorry, I cannot use a language without enums. 

Sending stats over email is disabled by defult, go ahead and correct enable it by editing multiplication.config file (I moved it to a separate file to simplify the updates).

Enjoy, and good luck.

--Anatoly.
