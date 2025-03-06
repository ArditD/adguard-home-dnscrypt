"""
AdGuard Blocklist Manager - with improved security and stability

This script downloads, standardizes, sorts, and merges multiple blocklist files
for use with AdGuard Home. It now supports splitting large blocklists into multiple files.
"""

import os
import sys
import argparse
import logging
from downloader import download_all_files, get_url_filename, is_valid_text_file
from parser import standardize_and_sort_domains
from config import load_config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Maximum file size in bytes (20MB)
MAX_FILE_SIZE = 20 * 1024 * 1024

def parse_arguments():
    parser = argparse.ArgumentParser(description='AdGuard Blocklist Manager')
    parser.add_argument('-c', '--config', default=None,
                        help='Path to configuration file (JSON)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file base name (default from config)')
    parser.add_argument('-w', '--whitelist', default=None,
                        help='Whitelist file (default from config)')
    parser.add_argument('-l', '--local', action='store_true',
                        help='Use local files only, do not check for updates')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force download of all files regardless of age')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--max-size', type=int, default=MAX_FILE_SIZE,
                        help='Maximum file size in bytes (default: 20MB)')
    return parser.parse_args()

def check_requirements():
    # Ensure Python 3.x is being used
    if sys.version_info < (3, 0):
        sys.exit("This script requires Python 3.x. Please upgrade your Python interpreter.")

    # List of required libraries (module name: pip package name)
    required_modules = {
        "requests": "requests",
        "urllib3": "urllib3",
    }

    missing = []
    for module, package in required_modules.items():
        try:
            __import__(module)
        except ImportError:
            if package:
                missing.append(package)
            else:
                missing.append(module)
    
    if missing:
        print("Missing required libraries: " + ", ".join(missing))
        print("Please install them using your OS package manager or:")
        print("    pip install " + " ".join(missing))
        sys.exit(1)

def get_local_files(download_dir):
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
             if os.path.isfile(os.path.join(download_dir, f)) and f.endswith(('.txt', '.list'))]
    if not files:
        logger.error(f"No compatible files found in {download_dir}")
    else:
        logger.info(f"Found {len(files)} local files in {download_dir}")
    return files

def load_whitelist(whitelist_file):
    whitelist = set()
    if whitelist_file and os.path.exists(whitelist_file):
        try:
            with open(whitelist_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        whitelist.add(line)
            logger.info(f"Loaded {len(whitelist)} domains from whitelist: {whitelist_file}")
        except Exception as e:
            logger.error(f"Failed to load whitelist: {e}")
    else:
        logger.info("No whitelist file specified or file not found")
    return whitelist

def estimate_file_size(headers, domains, chunk_size):
    """Estimate the file size based on the number of domains."""
    # Average bytes per domain (domain + newline)
    avg_domain_size = 30  # This is an estimate, adjust if needed
    headers_size = sum(len(h) + 1 for h in headers)  # +1 for newline
    
    # Calculate how many domains we can fit in the remaining space
    remaining_space = chunk_size - headers_size
    domains_per_file = max(1, int(remaining_space / avg_domain_size))
    
    return domains_per_file

def write_output_split(output_base, headers, domains, max_size=MAX_FILE_SIZE):
    """Write domains to multiple files, splitting when approaching max_size."""
    try:
        # Get file extension and base name
        base_name, extension = os.path.splitext(output_base)
        if not extension:
            extension = ".txt"
        
        # Estimate domains per file
        domains_per_file = estimate_file_size(headers, domains, max_size)
        
        file_count = 0
        total_domains = len(domains)
        domains_written = 0
        
        while domains_written < total_domains:
            file_count += 1
            current_filename = f"{base_name}-{file_count}{extension}"
            
            # Get the next chunk of domains
            start_idx = domains_written
            end_idx = min(domains_written + domains_per_file, total_domains)
            current_domains = domains[start_idx:end_idx]
            domains_written = end_idx
            
            # Add file-specific header
            current_headers = headers.copy()
            current_headers.append(f"! Part {file_count} of the split blocklist")
            
            # Write the file
            with open(current_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(current_headers) + '\n\n')
                f.write('\n'.join(current_domains) + '\n')
            
            logger.info(f"Wrote {len(current_domains)} domains to {current_filename}")
        
        logger.info(f"Successfully split {total_domains} domains into {file_count} files")
        return True
    except Exception as e:
        logger.error(f"Failed to write split output files: {e}")
        return False

def main():
    args = parse_arguments()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        # Use default config file from config.py
        config = load_config()
    
    urls = config.get("urls", [])
    download_dir = config.get("download_dir", ".")
    default_output = config.get("default_output", "merged_blocklist.txt")
    default_whitelist = config.get("default_whitelist", None)
    max_age = config.get("default_max_age", 24)
    
    output_file = args.output if args.output else default_output
    whitelist_file = args.whitelist if args.whitelist else default_whitelist
    max_size = args.max_size
    
    files = []
    if args.local:
        logger.info("Local mode enabled: checking for expected files")
        for url in urls:
            local_file = os.path.join(download_dir, get_url_filename(url))
            if not os.path.exists(local_file):
                logger.info(f"Missing file {local_file}; downloading it now.")
                downloaded = download_all_files([url], download_dir, max_age, args.force)
                if downloaded:
                    files.extend(downloaded)
            else:
                if is_valid_text_file(local_file):
                    files.append(local_file)
                else:
                    logger.error(f"Skipping invalid local file: {local_file}")
        if not files:
            logger.error("No valid files available in local mode.")
            sys.exit(1)
    else:
        files = download_all_files(urls, download_dir, max_age, args.force)
        if not files:
            logger.error("No valid files were successfully processed")
            sys.exit(1)
    
    whitelist = load_whitelist(whitelist_file)
    headers, sorted_domains = standardize_and_sort_domains(files, whitelist)
    
    # Use the new split output function
    if write_output_split(output_file, headers, sorted_domains, max_size):
        logger.info("Blocklist processing and splitting completed securely")
    else:
        logger.error("Failed to complete secure blocklist processing and splitting")
        sys.exit(1)

if __name__ == "__main__":
    check_requirements()
    main()