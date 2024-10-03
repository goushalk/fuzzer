import os 

target = input("URL: ")
os.system(f"wfuzz -c -z file,xss.txt -f xss.json,json -u {target}?q=FUZZ")