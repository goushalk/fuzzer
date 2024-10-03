import os

target = input("URL: ")

os.system(f"wfuzz -c -z file,wordlist.txt -f ze_redict.json,json -u {target}?redirect=FUZZ --hc 302" )