#!/usr/bin/env python3

import unittest

from conll_mrs import deserialize


class DeserializeTests(unittest.TestCase):
    def test_basic(self):
        test_data = """
        # global.columns = ID FORM LEMMA UPOS XPOS MRS:PRED MRS:ROLES MRS:LNK MRS:FEATS MISC
        1	I	I	PRON	PRP	pron	2:ARG1-NEQ|1.1:RSTR-H	<0:1>	cvarsort=x|pers=1|num=sg|ind=+|pt=std	_
        1.1	_	_	_	_	pronoun_q	_	<0:1>	_	_
        2	like	like	VERB	VBP	_like_v_1	_	<2:6>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
        3	dogs	dog	NOUN	NNS	_dog_n_1	2:ARG2-NEQ|3.1:RSTR-H	<7:11>	cvarsort=x|pers=3|num=pl|ind=+	_
        3.1	_	_	_	_	udef_q	_	<7:11>	_	_
        """
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
