## The Current Thirst for Data
With Mozilla's controversial recent behaviors : 
- https://www.malwarebytes.com/blog/news/2024/09/privacy-watchdog-files-complaint-over-firefox-quietly-enabling-its-privacy-preserving-attribution 
- The famous privacy controversy, and Mozilla trying to mend up :  https://techcrunch.com/2025/03/03/mozilla-rewrites-firefoxs-terms-of-use-after-user-backlash/ 
- Well, As for Google : https://www.theverge.com/news/622953/google-chrome-extensions-ublock-origin-disabled-manifest-v3 

Long story short, people are very hungry for data due to the AI hype, and they don't care how they collect them.

An extract from : https://www.scss.tcd.ie/Doug.Leith/pubs/cookies_identifiers_and_other_data.pdf 

> "C. Response From Google
The Google Play Services and Google Play store apps studied
here are in active use by hundreds of millions of people. We
informed Google of our findings, and delayed publication to
allow them to respond. They gave a brief response, stating
that they would not comment on the legal aspects (they were
not asked to comment on these). They did not point out any
errors or mis-statements (which they were asked to comment
on). They did not respond to our question about whether they
planned to make any changes to the cookies etc stored by their
software."


## What this repo is for 
It's an attempt to address the issue for people who don't have access to Enterprise solutions or hardware by providing a solution that takes care mostly of privacy and security when talking about ads, trackers, adult, malware, etc content.

This repo contains mainly two components : 
- A docker container (arch linux) with adguard-home (for ad blocking) and dnscrypt-proxy used as upstream proxy for adguard-home for enhancing privacy and security
- a blocklist-manager made in python for adguard-home to process and manage blocklists auotomatically (as there are allot of duplicates around copying each-other)

Visit blocklist-manager for the python app, and adguard-dnscrypt for the container (they have their own readme) for more details