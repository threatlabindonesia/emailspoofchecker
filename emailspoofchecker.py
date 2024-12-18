import csv
import json
import os
import dns.resolver
import pandas as pd
from tqdm import tqdm
import argparse

# Banner
BANNER = """
----------------------------------------------------------------------------
             Email Spoofing Vulnerability Checker

 Description: This tool checks for DMARC, SPF, and DKIM records
              to identify potential spoofing vulnerabilities.

 Author: Afif Hidayatullah
 Organization: ITSEC Asia
----------------------------------------------------------------------------
"""

# Configure DNS resolver with alternative nameservers and timeout
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google Public DNS
resolver.timeout = 10  # Timeout for a single query
resolver.lifetime = 10  # Total time allowed for a query

# Function to check SPF record
def check_spf(domain):
    try:
        answers = resolver.resolve(domain, "TXT")
        for txt_record in answers:
            if txt_record.to_text().startswith('"v=spf1'):
                return txt_record.to_text().strip('"')
        return "No SPF record found"
    except dns.resolver.Timeout:
        return "DNS query timed out"
    except dns.resolver.NXDOMAIN:
        return "No SPF record found (NXDOMAIN)"
    except dns.resolver.NoAnswer:
        return "No SPF record found (No Answer)"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to check DMARC record
def check_dmarc(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = resolver.resolve(dmarc_domain, "TXT")
        for txt_record in answers:
            return txt_record.to_text().strip('"')
        return "No DMARC record found"
    except dns.resolver.Timeout:
        return "DNS query timed out"
    except dns.resolver.NXDOMAIN:
        return "No DMARC record found (NXDOMAIN)"
    except dns.resolver.NoAnswer:
        return "No DMARC record found (No Answer)"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to check DKIM record
def check_dkim(domain, selector="default"):
    try:
        dkim_domain = f"{selector}._domainkey.{domain}"
        answers = resolver.resolve(dkim_domain, "TXT")
        for txt_record in answers:
            return txt_record.to_text().strip('"')
        return "No DKIM record found"
    except dns.resolver.Timeout:
        return "DNS query timed out"
    except dns.resolver.NXDOMAIN:
        return f"No DKIM record found for selector '{selector}'"
    except dns.resolver.NoAnswer:
        return "No DKIM record found (No Answer)"
    except Exception as e:
        return f"Error: {str(e)}"

# Determine spoofing vulnerability
def determine_vulnerability(spf, dmarc, dkim):
    # DMARC and SPF checks
    spf_configured = "v=spf1" in spf
    dmarc_configured = "v=DMARC1" in dmarc
    dmarc_reject_policy = "p=reject" in dmarc or "p=quarantine" in dmarc

    if not spf_configured and not dmarc_configured:
        return "Vulnerable to spoofing"
    elif not spf_configured or not dmarc_configured or not dmarc_reject_policy:
        return "Potentially vulnerable"
    else:
        return "Secure"

# Process domains and return results
def process_domains(domains):
    results = []
    for domain in tqdm(domains, desc="Processing domains", ncols=80):
        spf = check_spf(domain)
        dmarc = check_dmarc(domain)
        dkim = check_dkim(domain)
        vulnerability = determine_vulnerability(spf, dmarc, dkim)
        results.append({
            "Domain": domain,
            "SPF": spf,
            "DMARC": dmarc,
            "DKIM": dkim,
            "Vulnerability": vulnerability
        })
    return results

# Save or display results
def save_results(results, output_format, output_path):
    if output_path:
        if output_format == "json":
            with open(output_path, "w") as json_file:
                json.dump(results, json_file, indent=4)
        elif output_format == "csv":
            keys = results[0].keys()
            with open(output_path, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(results)
        elif output_format == "xlsx":
            df = pd.DataFrame(results)
            df.to_excel(output_path, index=False)
        elif output_format == "txt":
            with open(output_path, "w") as txt_file:
                for result in results:
                    txt_file.write(f"{result}\n")
        print(f"Results saved to {output_path}")
    else:
        print(json.dumps(results, indent=4))

# Main function
def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Email Spoofing Vulnerability Checker")
    parser.add_argument("--domain", type=str, help="Single domain to check")
    parser.add_argument("--file", type=str, help="File path for bulk domains (one domain per line)")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--format", type=str, choices=["json", "csv", "xlsx", "txt"], default="json", help="Output file format (default: json)")
    args = parser.parse_args()

    domains = []
    if args.domain:
        domains = [args.domain]
    elif args.file:
        if os.path.exists(args.file):
            with open(args.file, "r") as f:
                domains = [line.strip() for line in f.readlines()]
        else:
            print("Error: File not found.")
            return
    else:
        print("Error: Please specify a domain or file.")
        return

    results = process_domains(domains)
    
    save_results(results, args.format, args.output)

if __name__ == "__main__":
    main()
