import wfuzz

# Function to perform fuzzing for zero redirect attack
def zero_redirect_attack(base_url, wordlist):
    # Construct the fuzzing target URL
    fuzzing_url = f"{base_url}?redirect=FUZZ"
    
    # Use wfuzz's session to initiate the fuzzing process
    with wfuzz.FuzzSession(
        url=fuzzing_url, 
        payloads=[("file", dict(fn=wordlist))]
    ) as session:
        
        print(f"Performing fuzzing on: {fuzzing_url}")
        
        # Iterate through fuzzing results
        for result in session.fuzz():
            # Check for status codes that indicate a redirect (e.g., 301, 302, 307, etc.)
            if result.code in [301, 302, 307, 308]:
                print(f"Potential redirect found: {result.url}")
                print(f"Status Code: {result.code}, Length: {result.length}")

# Main function
if __name__ == "__main__":
    # Define base URL and wordlist
    base_url = input("Enter the base URL (e.g., http://example.com): ")
    wordlist = "wordlist.txt"  # Ensure you have a proper wordlist

    # Run the zero redirect attack
    zero_redirect_attack(base_url, wordlist)
