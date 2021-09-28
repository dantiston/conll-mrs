#!/usr/bin/env python3

import unittest

from conll_mrs import process
from delphin import ace


class ProcessTests(unittest.TestCase):
    def test_construct_sentence_basic(self):
        sentence = 'I like dogs'
        response = ace.parse('/Users/Dantiston/Code/grammars/erg/2020.dat', sentence)
        actual = process._construct_sentence(sentence, response)
        expected = """1	I	I	PRON	PRP	pron	2:ARG1-NEQ|1.1:RSTR-H	<0:1>	cvarsort=x|pers=1|num=sg|ind=+|pt=std	_
1.1	_	_	_	_	pronoun_q	_	<0:1>	_	_
2	like	like	VERB	VBP	_like_v_1	_	<2:6>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
3	dogs	dog	NOUN	NNS	_dog_n_1	2:ARG2-NEQ|3.1:RSTR-H	<7:11>	cvarsort=x|pers=3|num=pl|ind=+	_
3.1	_	_	_	_	udef_q	_	<7:11>	_	_"""
        self.assertEquals(actual, expected)
