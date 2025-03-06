# AdGuard Blocklist Manager

## The Current Thirst for Data

In today's digital landscape, we're witnessing an unprecedented appetite for user data, driven largely by the AI boom. Major tech companies are increasingly compromising privacy principles:

- **Mozilla's Controversial Moves**: 
  - Privacy watchdogs [filed complaints](https://www.malwarebytes.com/blog/news/2024/09/privacy-watchdog-files-complaint-over-firefox-quietly-enabling-its-privacy-preserving-attribution) over Firefox quietly enabling tracking features
  - After significant user backlash, Mozilla was forced to [rewrite Firefox's terms of use](https://techcrunch.com/2025/03/03/mozilla-rewrites-firefoxs-terms-of-use-after-user-backlash/)

- **Google's Extension Crackdown**:
  - Google [disabled popular privacy extensions](https://www.theverge.com/news/622953/google-chrome-extensions-ublock-origin-disabled-manifest-v3) like uBlock Origin through Manifest V3 enforcement

Long story short, companies appear increasingly desperate for data to feed AI systems, often with little regard for how it's collected or what's being gathered.

Consider this revealing extract from academic research ([PDF link](https://www.scss.tcd.ie/Doug.Leith/pubs/cookies_identifiers_and_other_data.pdf)):

> "C. Response From Google
> The Google Play Services and Google Play store apps studied
> here are in active use by hundreds of millions of people. We
> informed Google of our findings, and delayed publication to
> allow them to respond. They gave a brief response, stating
> that they would not comment on the legal aspects (they were
> not asked to comment on these). They did not point out any
> errors or mis-statements (which they were asked to comment
> on). They did not respond to our question about whether they
> planned to make any changes to the cookies etc stored by their
> software."

## What This Repository Offers

This project aims to empower average users who don't have access to enterprise-grade privacy solutions. It provides robust tools to safeguard privacy and security by filtering DNS traffic to block ads, trackers, adult content, and malware.

The repository consists of two main components:

1. **Docker Container** (`adguard-dnscrypt` directory):
   - Runs AdGuard Home for comprehensive ad blocking
   - Integrates dnscrypt-proxy as an upstream resolver to enhance privacy and security
   - Built on Arch Linux for performance and minimal footprint

2. **Blocklist Manager** (`blocklist-manager` directory):
   - Python application to automatically process and manage blocklists
   - Intelligently handles duplicates (common in many blocklists that copy from each other)
   - Securely downloads, validates, and merges multiple blocklist sources
   - Splits large blocklists into manageable chunks for better performance

Each component has its own detailed README with specific instructions and documentation.

## Getting Started

### Prerequisites
- Python 3.x
- Docker (for container component)
- Basic understanding of DNS configuration

### Installation

Clone the repository:
   ```bash
   git clone https://github.com/ArditD/adguard-home-dnscrypt.git
   cd adguard-blocklist-manager
   ```

See the individual component directories for detailed setup and usage instructions:
- For the Python blocklist manager: See `blocklist-manager/README.md`
- For the Docker container: See `adguard-dnscrypt/README.md`

## Why This Matters

As companies increasingly prioritize data collection over user privacy, tools like this become essential for maintaining control over your digital footprint. 
By filtering DNS requests, you can significantly reduce tracking, ads, and malware exposure without sacrificing browsing performance.


