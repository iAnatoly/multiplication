#!/usr/bin/python
#
# (C) Copyright Anatoly Ivanov <anatoly.ivanov@gamil.com>
# This script is free for use and redistribution in educational purposes.
# See https://github.com/iAnatoly/multiplication/ for more info.
#
import random;
import sys;
from datetime import datetime;
try:
	from enum import Enum;
except:
	import os;
	os.system("pip install enum34");
	from enum import Enum;

enableEmailStatistics=True;

if (enableEmailStatistics):
	import smtplib;
	from email.mime.text import MIMEText;
	sender="[YOUR ROBOT ACCOUNT]@gmail.com";
	senderPassword="PASSWORD";
	recipients=["PARENT1@live.com","PARENT2@gmail.com"];
	smtpserver="smtp.gmail.com:587";

class Mode(Enum):
	Training = 1
	Precision = 2
	TimeTrial = 3
	SPARTA = 4	

def getNumber(message):
	while (True):
		try:
			result=int(raw_input(message));
			return result;
		except:
			print "That is not a number";

def getNumberWithDefault(message,default):
	while (True):
		raw_result=raw_input(message+" [default={0}]".format(default));
		if (raw_result==''):
			return default;
		try:
			result=int(raw_result);
			return result;
		except:
			print "That is not a number";
	

def getAnswer(message):
	while (True):
		result=raw_input(message);
		if ('yes' in result):
			return True;
		elif ('no' in result):
			return False;
		else:
			print "Please answer 'yes' or 'no'";

def getSelection(max):
	while (True):
		result=getNumber("Please eneter your choice: ")
		if (result>0 and result<=max):
			return result;
		else:
			print "Incorrect selection. Expecting a number [1...{0}]".format(max);

def sendEmail(result):
	try:
		sys.stdout.write("\nPlease wait - sending report to mom & dad...");
		sys.stdout.flush();
	
		server = smtplib.SMTP(smtpserver);
		server.set_debuglevel(False);
		server.ehlo();
		server.starttls();
		server.login(sender, senderPassword);
		sys.stdout.write('.'); sys.stdout.flush();
		msg = MIMEText(result,'plain');
		msg['Subject'] = 'Multiplication report at {0}'.format(date);
		msg['From'] = "'Multiplication Report' <{0}>".format(sender);  
		msg['To'] = ",".join(recipients);
		server.sendmail(sender,recipients, msg.as_string());
		sys.stdout.write('.'); sys.stdout.flush();
		server.quit();
		print "done.\n";
	except Exception as e:
		print "\nError sending out email: {0}.".format(e);
		

class Answer:
	def __init__(self,prev1,prev2,mode):
		self.mode = mode;
		self.num1 = prev1;
		self.num2 = prev2;
		self.answer = 0;
		while (self.isRepeating(prev1,prev2)):
			self.num1 = random.randrange(1,13);
			self.num2 = random.randrange(1,12);

	def question(self):
		if (self.mode):
			return "{0} X {1} = ".format(self.num1, self.num2);
		else:
			return "{0} / {1} = ".format(self.num1*self.num2, self.num1);
			
	
	def questionAnswer(self):
		return "{0}{1}".format(self.question(),self.answer);
	
	def questionAnswerTiming(self):
		return "{0}; time taken: {1}.{2}s".format(self.questionAnswer(),self.timeTaken.seconds,self.timeTaken.microseconds/10000);
	
	def questionAnswerTimingCorrectness(self):
		return "{0} ({1})".format(self.questionAnswerTiming(),"correct" if self.isCorrect() else "WRONG");

	def isRepeating(self,prev1,prev2):
		return (self.num1==prev1 or self.num2==prev2 or self.num1==prev2 or self.num2==prev1);

	def askQuestion(self,i):
		time = datetime.now();
		self.answer = getNumber("Try #{0}: {1}".format(i,self.question()));
		self.timeTaken = datetime.now() - time;	

	def isCorrect(self):
		if (self.mode):
			return self.num1*self.num2==self.answer;
		else:
			return self.num2==self.answer;


random.seed();

right=0;
wrong=0;

prev1=0;
prev2=0;
feedback=True;
errors=[];
stats=[];

mmode = not getAnswer("Use division instead of multiplication? [yes|no] ");

tries = getNumberWithDefault("How many tries? [please neter number] ",100);
date = datetime.now();

print "\
Please select mode:\n\
1: Training (no time limit, mistakes are allowed);\n\
2: Precision trial (no time limit, stop after first mistake);\n\
3: Time trial (time limit, mistakes are allowed);\n\
4: THIS IS SPARTA (time limit, stop after first error).\n\
";
modeSelection = Mode(getSelection(4));

if (modeSelection == Mode.TimeTrial or modeSelection == Mode.SPARTA):
	timeLimit = getNumberWithDefault("Time limit (seconds)", 180);
else:
	timeLimit = -1;

for i in range(0,tries):
	answer = Answer(prev1,prev2,mmode);
	prev1=answer.num1;
	prev2=answer.num2;
	
	answer.askQuestion(i+1);
	
	if (modeSelection==Mode.TimeTrial or modeSelection == Mode.SPARTA):
		timeTaken = datetime.now()-date;
		if (timeTaken.seconds>=timeLimit):
			print " Out of Time!{0}".format(" THIS IS SPARTA!!! " if modeSelection==Mode.SPARTA else "");
			break;
	
	if (answer.isCorrect()):
		right=right+1;
		if (feedback):
			print " Correct!";
	else:
		wrong=wrong+1;
		errors.append(answer);
		if (feedback):
			print " Incorrect!";
		if (modeSelection==Mode.Precision or modeSelection==Mode.SPARTA):
			break;
	stats.append(answer);	

finished = datetime.now();
timeTaken = finished - date;
slow = sorted(stats,key = lambda x: x.timeTaken, reverse=True)[:5];

result="\nMode: {10}\nDesired tries: {2}; Actual tries: {8} ({9}%)\nTime taken: {5} minutes {6} seconds ({7} seconds avg per try)\nWrong: {0} ({3}%)\nRight: {1} ({4}%)".format(
	wrong,
	right,
	tries, 
	wrong*100/(right+wrong) if (right+wrong>0) else 0,
	right*100/(right+wrong) if (right+wrong>0) else 0,
	timeTaken.seconds / 60,
	timeTaken.seconds % 60,
	timeTaken.seconds/tries,
	right+wrong,
	(right+wrong)*100/tries,
	"Multiplication" if (mmode) else "Division");

result = result + "\n\nList of wrong answers:\n"+"\n".join(map(lambda result: "\t"+result.questionAnswerTiming(), errors));
result = result + "\n\nList of slow answers:\n"+"\n".join(map(lambda result: "\t"+result.questionAnswerTimingCorrectness(), slow));
print result;

if (enableEmailStatistics):
	sendEmail(result);

hush = raw_input("Press [ENTER] to end the session");


