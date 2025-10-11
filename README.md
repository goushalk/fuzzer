# Fuzzer

Fuzzer is a Python-based web application security testing toolkit that automates common fuzzing and enumeration attacks against web applications and services. It leverages the power of [wfuzz](https://github.com/xmendez/wfuzz) to perform various security tests such as hidden directory discovery, subdomain enumeration, XSS, SQL Injection, and open redirect attacks.

## Features

- **Hidden Directory Discovery**: Identifies hidden directories on a target web server using wordlists.
- **Subdomain Enumeration**: Discovers subdomains associated with a domain using extensive wordlists.
- **XSS Fuzzing**: Tests web applications for Cross-Site Scripting (XSS) vulnerabilities.
- **SQL Injection Fuzzing**: Scans for SQL injection points using common attack payloads.
- **Open Redirect Attack Detection**: Verifies if a target is vulnerable to open redirect attacks.
- **Web Interface**: Provides a simple Flask web application for launching fuzzing attacks and downloading results.

## Requirements

- Python 3.x
- Flask
- wfuzz
- pandas
- requests

You may also need to install system dependencies for `wfuzz` and `pycurl`. Use a Python virtual environment for best results.

## Installation

```bash
git clone https://github.com/goushalk/fuzzer.git
cd fuzzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Make sure to create this file with Flask, pandas, requests, etc.
```

Ensure that `wfuzz` is installed and available in your `PATH`.

## Usage

### Web Application

Start the Flask application:

```bash
python app3.py
```

Open your browser and navigate to `http://localhost:5000` to use the web UI. You can select different attack types (XSS, SQLi, hidden directories, subdomain enumeration) and provide a target URL. Results are saved as CSV files and can be downloaded from the UI.

### Command-Line Tools

Several scripts are provided for direct command-line fuzzing:

- `fuzz.py` – Interactive script for running various scans (XSS, SQLi, CSRF, directory scan).
- `xss.py` – Run XSS fuzzing via command line.
- `zero_re.py` – Test for open redirect vulnerabilities.

Example:

```bash
python xss.py
```

Follow the prompts to enter your target URL.

## Wordlists

The `wordlist/` directory contains various wordlists used for fuzzing:

- `subdomains.txt`: Used for subdomain enumeration
- `hid_dict.txt`: Used for hidden directory discovery
- `xss.txt`, `sqli.txt`, `zero_re.txt`: Used for XSS, SQLi, and open redirect attacks

You can add or modify these wordlists as needed.

## Mitigations

The application provides mitigation tips for each attack type, for example:

- **SQL Injection**: Use parameterized queries, sanitize inputs, and apply least privilege principles.
- **Hidden Directories**: Restrict permissions, disable directory listing, and use `robots.txt`.
- **Subdomain Enumeration**: Limit subdomain exposure, apply DNS security, and rate-limit requests.

## License

This project is provided for educational and testing purposes. Use responsibly and only on systems you own or have permission to test.

---

**Note:** This tool automates potentially intrusive security tests. Always have explicit permission before running it against any target.
