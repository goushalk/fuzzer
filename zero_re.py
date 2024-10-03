import os

# Get URL from user input
turl = input("Enter the base URL (e.g., http://example.com): ")

# Check if URL has a trailing slash and adjust if needed
if not turl.endswith('/'):
    turl += '/'

# Prepare the target URL with FUZZ placeholder for fuzzing the redirect parameter
targeturl = f"{turl}?redirect=FUZZ"

# Show the command that will be executed
print("Fuzzing target URL: ", targeturl)
print(f'Running command: wfuzz -w wordlist.txt -v --follow "{targeturl}"')

# Execute the wfuzz command
try:
    os.system(f'wfuzz -w wordlist.txt -v --follow "{targeturl}"')
except Exception as e:
    print(f"An error occurred: {e}")