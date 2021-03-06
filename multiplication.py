#!/usr/bin/python
#
# This script is free for use and redistribution in educational purposes.
# See https://github.com/iAnatoly/multiplication/ for more info.
#
# email notification configuration is defined in multiplication.config

import random
import os
import sys
import smtplib
import ConfigParser
from email.mime.text import MIMEText
from datetime import datetime

try:
    from enum import Enum
except ImportError:
    cmd = "sudo pip install enum34"
    print "Cannot find enum module; trying to fix - running '{0}'".format(cmd)
    os.system(cmd)
    from enum import Enum



#
# Enums for different modes
#


class TrainingMode(Enum):
    Training = 1
    Precision = 2
    TimeTrial = 3
    SPARTA = 4


class TrainingTaskMode(Enum):
    Multiplication = 1
    Division = 2
    Square = 3
    PowerOfTwo = 4
    SquareRoot = 5
    LogOfTwo = 6


#
# Static input helpers
# 


class InputHelper:
    @staticmethod
    def getNumber(message):
        while True:
            try:
                result = int(raw_input(message))
                return result
            except ValueError:
                print "That is not a number"

    @staticmethod
    def getNumberWithDefault(message, default):
        while True:
            try:
                raw_result = raw_input(message + " [default={0}] ".format(default))
                if raw_result == '':
                    print "Using default={0}".format(default)
                    return default
                else:
                    return int(raw_result)
            except ValueError:
                print "That is not a number"



    @staticmethod
    def getBooleanAnswer(message):
        while True:
            result = raw_input(message)
            if 'yes' in result:
                return True
            elif 'no' in result:
                return False
            else:
                print "Please answer 'yes' or 'no'"

    @staticmethod
    def boolToYesNo(value):
        return "yes" if value else "no"

    @staticmethod
    def getBooleanAnswerWithDefault(message, default):
        while True:
            result = raw_input(message + " [default={0}] ".format(InputHelper.boolToYesNo(default)))
            if 'yes' in result:
                return True
            elif 'no' in result:
                return False
            elif result == '':
                print "Using default={0}".format(InputHelper.boolToYesNo(default))
                return default
            else:
                print "Please answer 'yes' or 'no'"

    @staticmethod
    def getSelection(max):
        while True:
            result = InputHelper.getNumber("Please enter your choice: ")
            if result > 0 and result <= max:
                return result
            else:
                print "Incorrect selection. Expecting a number [1...{0}]".format(max)

    @staticmethod
    def getSelectionWithDefault(max, default):
        while True:
            result = InputHelper.getNumberWithDefault("Please enter your choice ", default)
            if result > 0 and result <= max:
                return result
            else:
                print "Incorrect selection. Expecting a number [1...{0}]".format(max)

    @staticmethod
    def pause():
        hush = raw_input("Press [ENTER] to end the session")

    @staticmethod
    def printNoCR(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()


#
# Email helper
# 
class Config:
    def __init__(self):
        self.emailNotificationEnabled = False
        self.sender = ''
        self.recipients = ''
        self.smtpserver = 'smtp.gmail.com:587'
        self.smtptls = True
        self.smtpuser = ''
        self.smtppassword = ''


class ConfigHelper:
    @staticmethod
    def getFileName():
        return os.path.dirname(__file__) + "/multiplication.config"

    @staticmethod
    def getConfig():
        config = Config()
        try:

            parser = ConfigParser.ConfigParser()
            parser.read(ConfigHelper.getFileName())

            config.emailNotificationEnabled = parser.getboolean('EmailConfiguration', 'EmailNotificationEnabled')
            config.smtpserver = parser.get('EmailConfiguration', 'SMTPServer')
            config.smtptls = parser.getboolean('EmailConfiguration', 'SMTPTLS')
            config.sender = parser.get('EmailConfiguration', 'sender')
            config.recipients = parser.get('EmailConfiguration', 'recipients')
            config.smtpuser = parser.get('EmailConfiguration', 'SMTPUser')
            config.smtppassword = parser.get('EmailConfiguration', 'SMTPPassword')
        except Exception as e:
            print e
        return config


class EmailHelper:
    def __init__(self, config):
        self.config = config

    def prepareMessage(self, result, mode):
        msg = MIMEText(result, 'plain')
        msg['Subject'] = '{0} report at {1}'.format(mode, datetime.now())
        msg['From'] = "'{0} Report' <{1}>".format(mode, self.config.sender)
        msg['To'] = self.config.recipients
        return msg

    def sendEmail(self, result, mode):
        try:
            InputHelper.printNoCR("\nPlease wait - sending report to mom & dad...")

            server = smtplib.SMTP(self.config.smtpserver)
            server.set_debuglevel(False)
            server.ehlo()
            if self.config.smtptls:
                server.starttls()
            server.login(self.config.smtpuser, self.config.smtppassword)

            InputHelper.printNoCR('.')

            msg = self.prepareMessage(result, mode)
            recipients = map(lambda i: i.strip(), self.config.recipients.split(";"))
            server.sendmail(self.config.sender, recipients, msg.as_string())

            InputHelper.printNoCR('.')

            server.quit()
            print "done.\n"

        except Exception as e:
            print "\nError sending out email: {0}.".format(e)


class Answer:
    def __init__(self, prev1, prev2, mode):
        self.mode = mode
        if self.mode == TrainingTaskMode.Multiplication or self.mode == TrainingTaskMode.Division:
            upperLimit1 = 13
            lowerLimit = 1
        else:
            upperLimit1 = 20
            lowerLimit = 2
        upperLimit2 = 12
        self.answer = 0

        self.num1 = self.num2 = 0
        random.seed()
        while self.isRepeating(prev1, prev2):
            self.num2 = random.randrange(lowerLimit, upperLimit2)
            self.num1 = random.randrange(lowerLimit, upperLimit1)

    @property
    def question(self):
        if self.mode == TrainingTaskMode.Multiplication:
            return "{0} X {1} = ".format(self.num1, self.num2)
        elif self.mode == TrainingTaskMode.Division:
            return "{0} / {1} = ".format(self.num1 * self.num2, self.num1)
        elif self.mode == TrainingTaskMode.Square:
            return "{0} ^2 = ".format(self.num1)
        elif self.mode == TrainingTaskMode.SquareRoot:
            return "X^2 = {0}; X=".format(self.num1 * self.num1)
        elif self.mode == TrainingTaskMode.PowerOfTwo:
            return "2^ {0} = ".format(self.num1)
        elif self.mode == TrainingTaskMode.LogOfTwo:
            return "2^X = {0}; X=".format(pow(2, self.num1))
        else:
            raise Exception('unknown mode')


    @property
    def questionAnswer(self):
        return "{0}{1}".format(self.question, self.answer)

    @property
    def questionAnswerTiming(self):
        return "{0}; time taken: {1}.{2}s".format(self.questionAnswer, self.timeTaken.seconds,
                                                  self.timeTaken.microseconds / 10000)

    @property
    def getCorrectnessMessage(self):
        return "Correct" if self.isCorrect() else "Incorrect"

    @property
    def questionAnswerTimingCorrectness(self):
        return "{0} ({1})".format(self.questionAnswerTiming, self.getCorrectnessMessage)

    def isRepeating(self, prev1, prev2):
        for p in prev1:
            if self.num1 == p:
                return True
        for p in prev2:
            if self.num2 == p:
                return True
        return False

    def askQuestionWithFeedback(self, i):
        self.askQuestion(i)
        print "\t" + self.getCorrectnessMessage

    def askQuestion(self, i):
        time = datetime.now()
        self.answer = InputHelper.getNumber("Try #{0}: {1}".format(i, self.question))
        self.timeTaken = datetime.now() - time

    def isCorrect(self):
        if self.mode == TrainingTaskMode.Multiplication:
            return self.num1 * self.num2 == self.answer
        elif self.mode == TrainingTaskMode.Division:
            return self.num2 == self.answer
        elif self.mode == TrainingTaskMode.Square:
            return self.num1 * self.num1 == self.answer
        elif self.mode == TrainingTaskMode.SquareRoot:
            return self.num1 == self.answer
        elif self.mode == TrainingTaskMode.PowerOfTwo:
            return pow(2, self.num1) == self.answer
        elif self.mode == TrainingTaskMode.LogOfTwo:
            return self.num1 == self.answer
        else:
            raise Exception('unknown mode')


class Session:
    def __init__(self):
        self.stats = Stats()
        self.ttmode = TrainingTaskMode.Multiplication

    def main(self):
        self.askUserParameters()
        self.run()
        InputHelper.pause()

    @property
    def isTimeLimitEnabled(self):
        return self.modeSelection == TrainingMode.TimeTrial or self.modeSelection == TrainingMode.SPARTA

    @property
    def isPrecisionModeEnabled(self):
        return self.modeSelection == TrainingMode.Precision or self.modeSelection == TrainingMode.SPARTA

    @property
    def getMode(self):
        return self.ttmode.name

    def askUserParameters(self):
        print "Please select excercise:\n1: Multiplication;\n2: Division;\n3: Quadrat;\n4: Power of 2\n5: Square root;\n6: Log of 2.\n"
        self.ttmode = TrainingTaskMode(InputHelper.getSelectionWithDefault(6, 1))

        self.stats.tries = InputHelper.getNumberWithDefault("How many tries? [please enter a number] ",
                                                            self.stats.tries)
        print "Please select mode:\n1: Training (no time limit, mistakes are allowed);\n2: Precision trial (no time limit, stop after first mistake);\n3: Time trial (time limit, mistakes are allowed);\n4: THIS IS SPARTA (time limit, stop after first error).\n"
        self.modeSelection = TrainingMode(InputHelper.getSelectionWithDefault(4, 1))

        if self.isTimeLimitEnabled:
            self.timeLimit = InputHelper.getNumberWithDefault("Time limit (seconds)", 180)

    def run(self):
        # TODO: move the history tracking into a separate class
        prev1 = [0]
        prev2 = [0]
        self.stats.startTimer()

        for i in range(0, self.stats.tries):
            answer = Answer(prev1, prev2, self.ttmode)
            prev1.insert(0, answer.num1)
            prev2.insert(0, answer.num2)
            while len(prev1) > 5:
                prev1.pop()
            while len(prev2) > 5:
                prev2.pop()
            answer.askQuestionWithFeedback(i + 1)

            if self.isTimeLimitEnabled:
                if self.stats.isTimeLimitExceeded(self.timeLimit):
                    print " Out of Time!{0}".format(
                        " THIS IS SPARTA!!! " if self.modeSelection == TrainingMode.SPARTA else "")
                    break

            self.stats.append(answer)

            if (not answer.isCorrect()) and self.isPrecisionModeEnabled:
                break

        self.stats.stopTimer()

        result = self.stats.getResults(self.getMode)
        print result

        try:
            mailConfig = ConfigHelper.getConfig()
            if mailConfig.emailNotificationEnabled:
                mailSender = EmailHelper(mailConfig)
                mailSender.sendEmail(result, self.getMode)
            else:
                print "Email notification is disabled. Please edit {0} file to enable it.".format(
                    ConfigHelper.getFileName())
        except Exception as e:
            print "Email notification is skipped due to an error {1} or absence of configuration. Please check {0} file.".format(
                ConfigHelper.getFileName(), e)


class Stats:
    def __init__(self):
        self.stats = []
        self.tries = 100
        self.elapsed = 0
        self.date = datetime.now()
        self.timerRunning = False


    def updateTimer(self):
        self.elapsed = datetime.now() - self.date

    def startTimer(self):
        self.date = datetime.now()
        self.updateTimer()
        self.timerRunning = True

    def stopTimer(self):
        self.updateTimer()
        self.timerRunning = False

    @property
    def getElapsed(self):
        if self.timerRunning:
            self.updateTimer()
        return self.elapsed

    def isTimeLimitExceeded(self, limit):
        return self.getElapsed.seconds >= limit

    def append(self, answer):
        self.stats.append(answer)

    def getResults(self, mode):
        slow = sorted(self.stats, key=lambda x: x.timeTaken, reverse=True)[:5]
        errors = filter(lambda x: not x.isCorrect(), self.stats)
        total = len(self.stats)
        wrong = len(errors)
        right = total - wrong

        result = "\nMode: {0}".format(mode)
        result += "\nDesired attempts: {0}".format(self.tries)
        result += "\nActual attempts: {0} ({1}%)".format(total, total * 100 / self.tries)
        result += "\nTime Taken: {0} minutes {1} seconds ({2} seconds avg per try)".format(self.elapsed.seconds / 60,
                                                                                           self.elapsed.seconds % 60,
                                                                                           self.elapsed.seconds * 1.0 / total)
        result += "\nRight: {0}({1}%)".format(right, right * 100 / total if (total > 0) else 0)
        result += "\nWrong: {0}({1}%)".format(wrong, wrong * 100 / total if (total > 0) else 0)
        result += "\n\nList of wrong answers:\n" + "\n".join(
            map(lambda result: "\t" + result.questionAnswerTiming, errors))
        result += "\n\nList of slow answers:\n" + "\n".join(
            map(lambda result: "\t" + result.questionAnswerTimingCorrectness, slow))
        return result


if __name__ == "__main__":
    try:
        session = Session()
        session.main()
    except KeyboardInterrupt:
        print "\nInterrupted"
