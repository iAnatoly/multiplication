from multiplication import Stats;
from multiplication import Session;
from multiplication import Mode;
from multiplication import MultiplicationMode;
from multiplication import Answer;

import time;
import random;
import unittest;

class TestSequenceFunctions(unittest.TestCase):
	def setUp(self):
		self.seq = range(10)
		self.stats = Stats();
		self.session = Session();
		self.mAnswer = Answer(1,1,MultiplicationMode.Multiplication);
		self.dAnswer = Answer(1,1,MultiplicationMode.Division);
		random.seed();


# u-tests for stats:

	def test_defaultTries(self):
		self.assertEqual(self.stats.tries, 100)

	def test_timer(self):
		seconds = 2;
		self.stats.startTimer();
		time.sleep(seconds);
		self.stats.stopTimer();
		self.assertEqual(self.stats.getElapsed().seconds,seconds);
	
	def test_isTimeLimitExceeded(self):
		seconds = 2;
		self.stats.startTimer();
		time.sleep(seconds-1);
		self.assertFalse(self.stats.isTimeLimitExceeded(seconds));
		time.sleep(seconds);
		self.assertTrue(self.stats.isTimeLimitExceeded(seconds));
		
#	def test_append(self):
#	def test_getResult(self):

#u-tests for Session
        def test_isTimeLimitEnabled(self):
		self.session.modeSelection = Mode.TimeTrial;
		self.assertTrue(self.session.isTimeLimitEnabled());
		self.session.modeSelection = Mode.SPARTA;
		self.assertTrue(self.session.isTimeLimitEnabled());
		self.session.modeSelection = Mode.Training;
		self.assertFalse(self.session.isTimeLimitEnabled());
		self.session.modeSelection = Mode.Precision;
		self.assertFalse(self.session.isTimeLimitEnabled());

        def test_isPrecisionModeEnabled(self):
		self.session.modeSelection = Mode.TimeTrial;
		self.assertFalse(self.session.isPrecisionModeEnabled());
		self.session.modeSelection = Mode.SPARTA;
		self.assertTrue(self.session.isPrecisionModeEnabled());
		self.session.modeSelection = Mode.Training;
		self.assertFalse(self.session.isPrecisionModeEnabled());
		self.session.modeSelection = Mode.Precision;
		self.assertTrue(self.session.isPrecisionModeEnabled());

        def test_getMode(self):
		self.session.mmode = MultiplicationMode.Multiplication;
		self.assertEqual(self.session.getMode(),"Multiplication");
		self.session.mmode = MultiplicationMode.Division;
		self.assertEqual(self.session.getMode(),"Division");

#u-test for answer

	def test_answer_init(self):
		prev1=0;
                prev2=0;
                for i in range(0,1000):
                        answer = Answer(prev1,prev2,MultiplicationMode.Multiplication);
			self.assertNotEqual(prev1,answer.num1);
			self.assertNotEqual(prev2,answer.num1);
			self.assertNotEqual(prev1,answer.num2);
			self.assertNotEqual(prev2,answer.num2);

        def test_answer_question_mul(self):
		answer = Answer(0,0,MultiplicationMode.Multiplication);
		self.assertEquals(answer.question(), "{0} X {1} = ".format(answer.num1, answer.num2));
	
        def test_answer_question_div(self):
		answer = Answer(0,0,MultiplicationMode.Division);
		self.assertEquals(answer.question(), "{0} / {1} = ".format(answer.num1*answer.num2, answer.num1));

        def test_answer_questionAnswer(self):
		answer = Answer(0,0,MultiplicationMode.Division);
		answer.answer = answer.num2;
		self.assertEquals(answer.questionAnswer(), "{0} / {1} = {2}".format(answer.num1*answer.num2, answer.num1, answer.num2));

        def test_answer_isRepeating(self):
		answer = Answer(0,1,MultiplicationMode.Division);
		answer.num1 = 0;
		self.assertTrue(answer.isRepeating(0,1));

		answer.num1 = answer.num2;
		answer.num2 = 0;
		self.assertTrue(answer.isRepeating(0,2));
		
		answer = Answer(0,2,MultiplicationMode.Division);
		answer.num1 = 2;
		self.assertTrue(answer.isRepeating(0,2));

		answer.num1 = answer.num2;
		answer.num2 = 2;
		self.assertTrue(answer.isRepeating(0,2));

        def test_answer_isCorrect(self):
		for m in [MultiplicationMode.Multiplication, MultiplicationMode.Division]:
			for i in range(0,100):
				for j in range(0,100):
					answer = Answer(0,0,m);
					answer.num1 = i;
					answer.num2 = j;
					if (m==MultiplicationMode.Multiplication):
						answer.answer = i*j;
					else:
						answer.answer = j;
					self.assertTrue(answer.isCorrect());
					
					if (m==MultiplicationMode.Multiplication):
						answer.answer = i*j+1;
					else:
						answer.answer = j+1;

					self.assertFalse(answer.isCorrect());

if __name__ == '__main__':
	unittest.main()
