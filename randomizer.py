#!env python

import sys
import string
import random

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_string = lambda n: ''.join([random.choice(string.lowercase + string.uppercase + string.digits) for i in xrange(n)])
        my_string = generate_string(int(sys.argv[1]))
        print(my_string)
    else:
        sys.exit('Please provide length in integers of string your want to generate')
