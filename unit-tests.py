from multiplication import Stats
from multiplication import Session
from multiplication import TrainingMode
from multiplication import TrainingTaskMode
import multiplication

import time
import random
import unittest


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)
        self.stats = Stats()
        self.session = Session()
        self.mAnswer = multiplication.Answer([1], [1], TrainingTaskMode.Multiplication)
        self.dAnswer = multiplication.Answer([1], [1], TrainingTaskMode.Division)
        self.prev1 = [0]
        self.prev2 = [0]
        random.seed()


    # u-tests for stats:

    def test_defaultTries(self):
        self.assertEqual(self.stats.tries, 100)

    def test_timer(self):
        seconds = 2
        self.stats.startTimer()
        time.sleep(seconds)
        self.stats.stopTimer()
        self.assertEqual(self.stats.getElapsed.seconds, seconds)

    def test_isTimeLimitExceeded(self):
        seconds = 2
        self.stats.startTimer()
        time.sleep(seconds - 1)
        self.assertFalse(self.stats.isTimeLimitExceeded(seconds))
        time.sleep(seconds)
        self.assertTrue(self.stats.isTimeLimitExceeded(seconds))

    # u-tests for Session
    def test_isTimeLimitEnabled(self):
        self.session.modeSelection = TrainingMode.TimeTrial
        self.assertTrue(self.session.isTimeLimitEnabled)
        self.session.modeSelection = TrainingMode.SPARTA
        self.assertTrue(self.session.isTimeLimitEnabled)
        self.session.modeSelection = TrainingMode.Training
        self.assertFalse(self.session.isTimeLimitEnabled)
        self.session.modeSelection = TrainingMode.Precision
        self.assertFalse(self.session.isTimeLimitEnabled)

    def test_isPrecisionModeEnabled(self):
        self.session.modeSelection = TrainingMode.TimeTrial
        self.assertFalse(self.session.isPrecisionModeEnabled)
        self.session.modeSelection = TrainingMode.SPARTA
        self.assertTrue(self.session.isPrecisionModeEnabled)
        self.session.modeSelection = TrainingMode.Training
        self.assertFalse(self.session.isPrecisionModeEnabled)
        self.session.modeSelection = TrainingMode.Precision
        self.assertTrue(self.session.isPrecisionModeEnabled)

    def test_getMode(self):
        self.session.ttmode = TrainingTaskMode.Multiplication
        self.assertEqual(self.session.getMode, "Multiplication")
        self.session.ttmode = TrainingTaskMode.Division
        self.assertEqual(self.session.getMode, "Division")

    # u-test for answer

    def test_answer_init(self):

        for i in range(0, 1000):
            answer = multiplication.Answer(self.prev1, self.prev2, TrainingTaskMode.Multiplication)
            self.assertFalse(answer.num1 in self.prev1)
            self.assertFalse(answer.num2 in self.prev2)

    def test_answer_question_mul(self):
        answer = multiplication.Answer(self.prev1, self.prev2, TrainingTaskMode.Multiplication)
        self.assertEquals(answer.question, "{0} X {1} = ".format(answer.num1, answer.num2))

    def test_answer_question_div(self):
        answer = multiplication.Answer(self.prev1, self.prev2, TrainingTaskMode.Division)
        self.assertEquals(answer.question, "{0} / {1} = ".format(answer.num1 * answer.num2, answer.num1))

    def test_answer_questionAnswer(self):
        answer = multiplication.Answer(self.prev1, self.prev2, TrainingTaskMode.Division)
        answer.answer = answer.num2
        self.assertEquals(answer.questionAnswer,
                          "{0} / {1} = {2}".format(answer.num1 * answer.num2, answer.num1, answer.num2))

    def test_answer_isRepeating(self):
        answer = multiplication.Answer([0], [1], TrainingTaskMode.Division)
        answer.num1 = 0
        self.assertTrue(answer.isRepeating([0], [1]))

        answer.num1 = answer.num2
        answer.num2 = 0
        self.assertFalse(answer.isRepeating([0], [2]))

        answer = multiplication.Answer([0], [2], TrainingTaskMode.Division)
        answer.num1 = 2
        self.assertFalse(answer.isRepeating([0], [2]))

        answer.num1 = answer.num2
        answer.num2 = 2
        self.assertTrue(answer.isRepeating([0], [2]))

    def test_answer_isCorrect(self):
        for m in [TrainingTaskMode.Multiplication, TrainingTaskMode.Division]:
            for i in range(0, 100):
                for j in range(0, 100):
                    answer = multiplication.Answer([0], [0], m)
                    answer.num1 = i
                    answer.num2 = j
                    if m == TrainingTaskMode.Multiplication:
                        answer.answer = i * j
                    else:
                        answer.answer = j
                    self.assertTrue(answer.isCorrect())

                    if m == TrainingTaskMode.Multiplication:
                        answer.answer = i * j + 1
                    else:
                        answer.answer = j + 1

                    self.assertFalse(answer.isCorrect())


if __name__ == '__main__':
    unittest.main()
