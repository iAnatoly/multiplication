#!/usr/bin/python
#
# (C) Copyright Anatoly Ivanov <anatoly.ivanov@gmail.com>
# This script is free for use and redistribution in educational purposes.
# See https://github.com/iAnatoly/multiplication/ for more info.
#

# configuration:
enableEmailStatistics=True;
if (enableEmailStatistics):
	sender="[YOUR ROBOT ACCOUNT]@gmail.com";
	senderPassword="PASSWORD";
	recipients=["PARENT1@live.com","PARENT2@gmail.com"];
	smtpserver="smtp.gmail.com:587";
#

import random;
import sys;
from datetime import datetime;
try:
	from enum import Enum;
except:
	import os;
	cmd = "sudo pip install enum34";
	print "Cannot find enum module; tring to fix - running '{0}'".format(cmd);
	os.system(cmd);
	from enum import Enum;
if (enableEmailStatistics):
	import smtplib;
	from email.mime.text import MIMEText;




# 
# Enums for different modes
#
class Mode(Enum):
	Training = 1
	Precision = 2
	TimeTrial = 3
	SPARTA = 4	

class MultiplicationMode(Enum):
	Multiplication = 1
	Division = 2

#
# Static input helpers
# 

class InputHelper:
	@staticmethod
	def getNumber(message):
		while (True):
			try:
				result=int(raw_input(message));
				return result;
			except:
				print "That is not a number";

	@staticmethod
	def getNumberWithDefault(message,default):
		while (True):
			raw_result=raw_input(message+" [default={0}] ".format(default));
			if (raw_result==''):
				print "Using default={0}".format(default);
				return default;
			try:
				result=int(raw_result);
				return result;
			except:
				print "That is not a number";
		

	@staticmethod
	def getBooleanAnswer(message):
		while (True):
			result=raw_input(message);
			if ('yes' in result):
				return True;
			elif ('no' in result):
				return False;
			else:
				print "Please answer 'yes' or 'no'";

	@staticmethod
	def boolToYesNo(value):
		return "yes" if value else "no";
	
	@staticmethod
	def getBooleanAnswerWithDefault(message, default):
		while (True):
			result=raw_input(message+" [default={0}] ".format(InputHelper.boolToYesNo(default)));
			if ('yes' in result):
				return True;
			elif ('no' in result):
				return False;
			elif (result == ''):
				print "Using default={0}".format(InputHelper.boolToYesNo(default));
				return default;
			else:
				print "Please answer 'yes' or 'no'";

	@staticmethod
	def getSelection(max):
		while (True):
			result=InputHelper.getNumber("Please enter your choice: ")
			if (result>0 and result<=max):
				return result;
			else:
				print "Incorrect selection. Expecting a number [1...{0}]".format(max);
	@staticmethod
	def pause():
		hush = raw_input("Press [ENTER] to end the session");

	@staticmethod
	def printNoCR(msg):
		sys.stdout.write(msg);
		sys.stdout.flush();
		

#
# Email helper
# 
class EmailHelper:
	def __init__(self,sender,senderPassword,recipients,smtpserver):
		self.sender=sender;
		self.senderPassword=senderPassword;
		self.recipients=recipients;
		self.smtpserver=smtpserver;

	def prepareMessage(self,result,mode):
		msg = MIMEText(result,'plain');
		msg['Subject'] = '{0} report at {1}'.format(mode,datetime.now());
		msg['From'] = "'{0} Report' <{1}>".format(mode,self.sender);  
		msg['To'] = ",".join(self.recipients);
		return msg;

		

		
	
	def sendEmail(self,result,mode):
		try:
			InputHelper.printNoCR("\nPlease wait - sending report to mom & dad...");
		
			server = smtplib.SMTP(self.smtpserver);
			server.set_debuglevel(False);
			server.ehlo();
			server.starttls();
			server.login(self.sender, self.senderPassword);

			InputHelper.printNoCR('.'); 

			msg = self.prepareMessage(result, mode);
			server.sendmail(self.sender,self.recipients, msg.as_string());

			InputHelper.printNoCR('.'); 
			
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
		if (self.mode == MultiplicationMode.Multiplication):
			return "{0} X {1} = ".format(self.num1, self.num2);
		else:
			return "{0} / {1} = ".format(self.num1*self.num2, self.num1);
			
	
	def questionAnswer(self):
		return "{0}{1}".format(self.question(),self.answer);
	
	def questionAnswerTiming(self):
		return "{0}; time taken: {1}.{2}s".format(self.questionAnswer(),self.timeTaken.seconds,self.timeTaken.microseconds/10000);
	
	def getCorrectnessMessage(self):
		return "Correct" if self.isCorrect() else "Incorrect";

	def questionAnswerTimingCorrectness(self):
		return "{0} ({1})".format(self.questionAnswerTiming(),self.getCorrectnessMessage());

	def isRepeating(self,prev1,prev2):
		return (self.num1==prev1 or self.num2==prev2 or self.num1==prev2 or self.num2==prev1);

	def askQuestionWithFeedback(self,i):
		self.askQuestion(i);
		print "\t"+self.getCorrectnessMessage();

	def askQuestion(self,i):
		time = datetime.now();
		self.answer = InputHelper.getNumber("Try #{0}: {1}".format(i,self.question()));
		self.timeTaken = datetime.now() - time;	

	def isCorrect(self):
		if (self.mode==MultiplicationMode.Multiplication):
			return self.num1*self.num2==self.answer;
		else:
			return self.num2==self.answer;

class Session:
	def __init__(self):
		random.seed();
		self.stats = Stats();
		self.mmode = MultiplicationMode.Multiplication;
		if (enableEmailStatistics):
			self.mailSender = EmailHelper(sender,senderPassword,recipients,smtpserver);
		
	def main(self):
		self.askUserParameters();
		self.run();
		InputHelper.pause();

	def isTimeLimitEnabled(self):
		return self.modeSelection == Mode.TimeTrial or self.modeSelection == Mode.SPARTA;

	def isPrecisionModeEnabled(self):
		return self.modeSelection == Mode.Precision or self.modeSelection == Mode.SPARTA;	

	def getMode(self):
		if (self.mmode == MultiplicationMode.Multiplication):
			return "Multiplication";
		return "Division";

	def askUserParameters(self):
		if InputHelper.getBooleanAnswerWithDefault("Use division instead of multiplication? [yes|no] ",False):
			self.mmode = MultiplicationMode.Division 

		self.stats.tries = InputHelper.getNumberWithDefault("How many tries? [please enter a number] ",self.stats.tries);
		print "Please select mode:\n1: Training (no time limit, mistakes are allowed);\n2: Precision trial (no time limit, stop after first mistake);\n3: Time trial (time limit, mistakes are allowed);\n4: THIS IS SPARTA (time limit, stop after first error).\n";
		self.modeSelection = Mode(InputHelper.getSelection(4));

		if (self.isTimeLimitEnabled()):
			self.timeLimit = InputHelper.getNumberWithDefault("Time limit (seconds)", 180);

	def run (self):
		prev1=0;
		prev2=0;

		self.stats.startTimer();

		for i in range(0,self.stats.tries):
			answer = Answer(prev1,prev2,self.mmode);
			prev1=answer.num1;
			prev2=answer.num2;
			
			answer.askQuestionWithFeedback(i+1);

			if (self.isTimeLimitEnabled()):
				if (self.stats.isTimeLimitExceeded(self.timeLimit)):
					print " Out of Time!{0}".format(" THIS IS SPARTA!!! " if self.modeSelection==Mode.SPARTA else "");
					break;
			
			self.stats.append(answer);

			if ((not answer.isCorrect()) and self.isPrecisionModeEnabled()):
				break;

		self.stats.stopTimer();

		result = self.stats.getResults(self.getMode());	
		print result;

		if (enableEmailStatistics):
			self.mailSender.sendEmail(result,self.getMode());

class Stats:
	def __init__(self):
		self.stats=[];
		self.tries=100;

	def updateTimer(self):
		self.elapsed = datetime.now() - self.date;

	def startTimer(self):
		self.date = datetime.now();
		self.updateTimer();
		self.timerRunning = True;
	
	def stopTimer(self):
		self.updateTimer();
		self.timerRunning = False;

	def getElapsed(self):
		if (self.timerRunning):
			self.updateTimer();
		return self.elapsed;

	def isTimeLimitExceeded(self,limit):
		return self.getElapsed().seconds >= limit;

	def append(self,answer):
		self.stats.append(answer);
			
	def getResults(self, mode):
		slow = sorted(self.stats,key = lambda x: x.timeTaken, reverse=True)[:5];
		errors = filter(lambda x: not x.isCorrect(), self.stats);
		total = len(self.stats);
		wrong = len(errors); 
		right = total - wrong;

		result = "\nMode: {0}".format(mode);
		result += "\nDesired attempts: {0}".format(self.tries);
		result += "\nActual attempts: {0} ({1}%)".format(total, total*100/self.tries);
		result += "\nTime Taken: {0} minutes {1} seconds ({2} seconds avg per try)".format(self.elapsed.seconds / 60, self.elapsed.seconds % 60, self.elapsed.seconds/total);
		result += "\nRight: {0}({1}%)".format(right, right*100/total if (total>0) else 0);
		result += "\nWrong: {0}({1}%)".format(wrong, wrong*100/total if (total>0) else 0);
		result += "\n\nList of wrong answers:\n"+"\n".join(map(lambda result: "\t"+result.questionAnswerTiming(), errors));
		result += "\n\nList of slow answers:\n"+"\n".join(map(lambda result: "\t"+result.questionAnswerTimingCorrectness(), slow));
		return result;


if __name__ == "__main__":
	session = Session();
	session.main();
