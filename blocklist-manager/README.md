# AdGuard Blocklist Manager

A secure and efficient Python tool for downloading, processing, and merging AdGuard blocklists with good security features.

## Features

- **Secure Downloads**: Enforces HTTPS, validates file integrity, and implements security checks
- **Automatic Updates**: Refreshes blocklists based on configurable age thresholds
- **Whitelist Support**: Excludes domains you want to allow
- **Format Standardization**: Converts various blocklist formats to AdGuard syntax
- **Duplicate Removal**: Eliminates redundant entries across multiple sources
- **File Splitting**: Automatically splits large blocklists into manageable 20MB chunks
- **Multi-threaded**: Downloads multiple blocklists concurrently for faster processing
- **Configurable**: Easily customizable through JSON configuration

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - urllib3



## Configuration

Create a `config.json` (or edit the default provided) file with the following structure:

```json
{
    "urls": [
        "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt",
        "https://adguardteam.github.io/HostlistsRegistry/assets/filter_49.txt",
        "https://v.firebog.net/hosts/Easyprivacy.txt"
    ],
    "download_dir": "blocklists",
    "default_output": "merged-blocklist.txt",
    "default_whitelist": "whitelist.txt",
    "default_max_age": 24
}
```

### Configuration Options

- `urls`: List of blocklist URLs to download and process (HTTPS only)
- `download_dir`: Directory to store downloaded blocklists
- `default_output`: Base name for the output file(s)
- `default_whitelist`: Name of the whitelist file
- `default_max_age`: Maximum age in hours before re-downloading a blocklist

## Whitelist File

Create a `whitelist.txt` file with domains you want to exclude from blocking, one per line:

```
example.com
safe-domain.org
```

## Usage

### Basic Usage

```bash
python main.py --help
usage: main.py [-h] [-c CONFIG] [-o OUTPUT] [-w WHITELIST] [-l] [-f] [-v] [--max-size MAX_SIZE]

AdGuard Blocklist Manager

options:
  -h, --help            show this help message and exit
  -c, --config CONFIG   Path to configuration file (JSON)
  -o, --output OUTPUT   Output file base name (default from config)
  -w, --whitelist WHITELIST
                        Whitelist file (default from config)
  -l, --local           Use local files only, do not check for updates
  -f, --force           Force download of all files regardless of age
  -v, --verbose         Enable verbose output
  --max-size MAX_SIZE   Maximum file size in bytes (default: 20MB)

```

This will download and process blocklists according to the default configuration file.

### Examples
#### Use Local Files Only

```bash
python main.py --local
```

#### Force Refresh All Blocklists
```bash
python main.py --force
```

#### Verbose Output
```bash
python main.py --verbose
```

#### Custom File Size Limit
```bash
python main.py --max-size 15728640  # Set to 15MB
```

## Output Files
With file splitting enabled, the output will be generated as multiple files:

- `merged-blocklist-1.txt`
- `merged-blocklist-2.txt`
- `merged-blocklist-3.txt`
- etc.

Each file contains:
- Header information with timestamp and description
- An indication of which part file it is
- A portion of the domains in AdGuard format (`||domain.com^`)


## .gitignore Recommendations
```
__pycache__
merged-blocklist-*.txt
config.json
custom-blocklist.txt
whitelist.txt
```

## Performance
- Processing millions of domains 3.3M in 33 sec depending on HW
- Multi-threaded downloads for improved efficiency
- Automatic removal of duplicates for cleaner output
- Memory-efficient operations for large datasets

## Troubleshooting
### Common Issues
1. **Missing dependencies**:
   ```
   pip install requests urllib3
   ```
2. **Permission errors**:
   Ensure you have write access to the output directory.
3. **SSL Certificate errors**:
   Make sure your Python installation has proper SSL certificates installed.
4. **Memory issues with large lists**:
   Adjust the `--max-size` parameter to create smaller output files.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
