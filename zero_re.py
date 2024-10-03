import os 


os.system('wfuzz -w wordlist.txt -v --follow "http://google.com?redirect=FUZZ"')
