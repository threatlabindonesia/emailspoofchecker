# Email Spoofing Vulnerability Checker

A Python tool to check for **SPF**, **DMARC**, and **DKIM** records to identify potential email spoofing vulnerabilities. This tool supports single domain or bulk domain checking and provides output in JSON, CSV, XLSX, or TXT formats.

---

## Features

- Checks for:
  - **SPF (Sender Policy Framework)** records.
  - **DMARC (Domain-based Message Authentication, Reporting, and Conformance)** records.
  - **DKIM (DomainKeys Identified Mail)** records.
- Determines:
  - **Vulnerability** to spoofing based on SPF, DMARC, and DKIM configuration.
  - **Potential vulnerability** when some records are missing or misconfigured.
  - **Secure** when SPF, DMARC, and DKIM are properly configured.
- Supports single domain or bulk domain checks.
- Outputs results to terminal or file in **JSON**, **CSV**, **XLSX**, or **TXT** formats.
- Progress bar for bulk checks.

---

## Requirements

- Python 3.7+
- Required Python libraries:
  ```bash
  pip install dnspython pandas tqdm
  ```

---

## How to Use

### Clone the Repository

```bash
git clone https://github.com/threatlabindonesia/emailspoofchecker.git
cd emailspoofchecker
```

### Command Examples

#### Single Domain Check

```bash
python emailspoofchecker.py --domain example.com
```

#### Bulk Domain Check

1. Prepare a `.txt` file with one domain per line, e.g., `domains.txt`:
   ```
   example.com
   test.com
   yourdomain.org
   ```

2. Run the script for bulk checking:
   ```bash
   python emailspoofchecker.py --file domains.txt
   ```

#### Save Output to a File

- JSON:
  ```bash
  python emailspoofchecker.py --domain example.com --output result.json --format json
  ```

- CSV:
  ```bash
  python emailspoofchecker.py --file domains.txt --output result.csv --format csv
  ```

- XLSX:
  ```bash
  python emailspoofchecker.py --file domains.txt --output result.xlsx --format xlsx
  ```

- TXT:
  ```bash
  python emailspoofchecker.py --domain example.com --output result.txt --format txt
  ```

#### Default Behavior

If `--output` is not specified, results will be displayed in the terminal in JSON format.

---

## Output Sample

### JSON Result for Single Domain

```json
[
    {
        "Domain": "example.com",
        "SPF": "v=spf1 include:_spf.google.com ~all",
        "DMARC": "v=DMARC1; p=reject;",
        "DKIM": "selector1._domainkey.example.com DKIM valid",
        "Vulnerability": "Secure"
    }
]
```

### JSON Result for Multiple Domains

```json
[
    {
        "Domain": "example.com",
        "SPF": "v=spf1 include:_spf.google.com ~all",
        "DMARC": "No DMARC record found (NXDOMAIN)",
        "DKIM": "No DKIM record found",
        "Vulnerability": "Potentially vulnerable"
    },
    {
        "Domain": "test.com",
        "SPF": "No SPF record found",
        "DMARC": "No DMARC record found (NXDOMAIN)",
        "DKIM": "No DKIM record found",
        "Vulnerability": "Vulnerable to spoofing"
    }
]
```

---

## Code Structure

- **`email_checker.py`**: Main script that handles domain checks.
- **Functions**:
  - `check_spf(domain)`: Checks SPF records.
  - `check_dmarc(domain)`: Checks DMARC records.
  - `check_dkim(domain, selector="default")`: Checks DKIM records using a specified selector.
  - `determine_vulnerability(spf, dmarc, dkim)`: Determines if the domain is secure, potentially vulnerable, or vulnerable to spoofing.

---

## Contact

If you have any questions or suggestions, feel free to reach out to the author:

- **Afif Hidayatullah**  
  Email: afif@itsecasia.com  
  Linkedin: [AfifHidayatullah](https://www.linkedin.com/in/afif-hidayatullah/)  
  Website: [www.itsec.asia](https://www.itsec.asia)

---

## Contribution

Feel free to fork this repository, create new features, or report issues through the [issues page](https://github.com/threatlabindonesia/emailspoofchecker/issues).

---
