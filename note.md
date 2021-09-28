PROBLEM: no existing library seems to support reading/writing CONLL-U Plus format
SOLUTIONS:
* Write it from scratch
* Fork pyconll

## Notes (to delete)
* hcons are stored on their target and point to their head, like dependencies
* variables are stored on their pred
* top is represented as an empty MRS:ROLES (is this a good idea?? Maybe should be explicit about top)
