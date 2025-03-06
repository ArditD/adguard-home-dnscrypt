# parser.py
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_domain(line):
    """Extract domain from various blocklist formats."""
    adguard_match = re.match(r'^\|\|([^/^]+)\^', line)
    if adguard_match:
        return adguard_match.group(1)
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line):
        return line
    return None

def natural_sort_key(domain):
    """Generate a key for natural sorting."""
    if domain.startswith('||') and domain.endswith('^'):
        domain = domain[2:-1]
    parts = []
    for part in re.split(r'([0-9]+)', domain):
        parts.append(int(part) if part.isdigit() else part.lower())
    return parts

def standardize_and_sort_domains(files, whitelist):
    domains = set()
    duplicate_count = 0
    headers = []
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    headers.append("! Title: Security-Enhanced Merged AdGuard Blocklist")
    headers.append(f"! Last updated: {current_date}")
    headers.append("! Description: Merged with HTTPS validation & content checks")
    headers.append("!")
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(('!', '#')):
                        continue
                    domain = extract_domain(line)
                    if domain:
                        if re.search(r"[^\w\.\-]", domain):
                            logger.debug(f"Skipping invalid domain format: {domain}")
                            continue
                        adguard_domain = f"||{domain}^"
                        if adguard_domain in domains:
                            duplicate_count += 1
                        else:
                            domains.add(adguard_domain)
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")

    sorted_domains = sorted(list(domains), key=lambda x: natural_sort_key(x.replace('||','').replace('^','')))
    logger.info(f"Securely processed {len(sorted_domains)} domains")
    logger.info(f"Found {duplicate_count} duplicate entries while processing")
    
    return headers, sorted_domains
