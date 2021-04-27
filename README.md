# conll-mrs
`conll-mrs` is a Python library to create CONLL-U formatted files.
`conll-mrs` has two primary functionalities:
* parse existing CONLL-U files and conduct parse selection using existing dependencies
* create new CONLL-U files from scratch

# CONLL-MRS Format
`conll-mrs` reads and writes files in the CONLL-MRS format.
CONLL-MRS builds on [the existing CONLL-U Plus format](https://universaldependencies.org/ext-format.html) by adding:
* an additional column for DMRS relations
* additional rows representing either relations without a link (LNK) to a surface form and the second or further relations linked to the same surface form
  * additional rows are represented using the existing `E\d+.\d+` format where the first number represents the new node's head index and the second a 1-based index of the additional node.
* files should be saved with the .conllup extension

See the following example of CONLL-MRS:
```
# global.columns = ID FORM LEMMA UPOS XPOS MRS:PRED MRS:ROLES MRS:LNK MRS:FEATS MISC
1	I	I	PRON	PRP	pron	2:ARG1-NEQ|1.1:RSTR-H	<0:1>	cvarsort=x|pers=1|num=sg|ind=+|pt=std	_
1.1	_	_	_	_	pronoun_q	_	<0:1>	_	_
2	like	like	VERB	VBP	_like_v_1	_	<2:6>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
3	dogs	dog	NOUN	NNS	_dog_n_1	2:ARG2-NEQ|3.1:RSTR-H	<7:11>	cvarsort=x|pers=3|num=pl|ind=+	_
3.1	_	_	_	_	udef_q	_	<7:11>	_	_
```

Here is a larger example
```
# global.columns = ID FORM LEMMA UPOS XPOS MRS:PRED MRS:ROLES MRS:LNK MRS:FEATS MISC
1	They	they	PRON	PRP	pron	2:ARG1-NEQ|1.1:RSTR-H|4:ARG1-NEQ	<0:4>	cvarsort=x|pers=3|num=pl|ind=+|pt=std	_
1.1	_	_	_	_	pronoun_q	_	<0:4>	_	_
2	buy	buy	VERB	VBP	_buy_v_1	3:ARG1-EQ|4:MOD-EQ	<5:8>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
3	and	and	CCONJ	CC	_and_c	_	<9:12>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
4	sell	sell	VERB	VBP	_sell_v_1	3:ARG1-EQ	<13:17>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
5	books	book	NOUN	NNS	_book_n_of	2:ARG2-NEQ|5.1:RSTR-H|4:ARG2-NEQ	<18:24>	cvarsort=x|pers=3|num=pl|ind=+	_
5.1	_	_	_	_	udef_q	_	<18:24>	_	_
```

It can also accompany other treebank information, such as universal dependencies
```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MRS:PRED MRS:ROLES MRS:LNK MRS:FEATS MISC
1	They	they	PRON	PRP	Case=Nom|Number=Sing|Person=1|PronType=Prs	2	nsubj	2:nsubj	pron	2:ARG1-NEQ|1.1:RSTR-H|4:ARG1-NEQ	<0:4>	cvarsort=x|pers=3|num=pl|ind=+|pt=std	_
1.1	_	_	_	_	_	_	_	_	pronoun_q	_	<0:4>	_	_
2	buy	buy	VERB	VBP	Number=Plur|Person=3|Tense=Pres	0	root	0:root	_buy_v_1	3:ARG1-EQ|4:MOD-EQ	<5:8>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
3	and	and	CCONJ	CC	_	4	conj	4:conj:and	_and_c	_	<9:12>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
4	sell	sell	VERB	VBP	Number=Plur|Person=3|Tense=Pres	0	root	0:root	_sell_v_1	3:ARG1-EQ	<13:17>	cvarsort=e|sf=prop|tense=pres|mood=indicative|prog=-|perf=-	_
5	books	book	NOUN	NNS	Case=Acc|Number=Plur	2	obj	2:obj	_book_n_of	2:ARG2-NEQ|5.1:RSTR-H|4:ARG2-NEQ	<18:24>	cvarsort=x|pers=3|num=pl|ind=+	_
5.1	_	_	_	_	_	_	_	_	udef_q	_	<18:24>	_	_
```