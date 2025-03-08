# Arch Docker Container with DNSCrypt and AdGuard Home

This document provides an overview of a Docker-based setup combining **DNSCrypt-Proxy** and **AdGuard Home** for enhanced DNS privacy and network-wide ad-blocking. Both services are managed via `supervisord`.
Adguard-home is meant to be used for content filtering, while dnscrypt-proxy as an upstream proxy to fully encrypt and secure the internet DNS traffic

## Feature List
- Arch Linux container
- Official Arch linux dnscrypt-proxy and adguard-home packages (no AUR, from extras)
- Added supervisord for monitoring the services
- Custom dnscrypt-proxy configuration which disables by default DoH and relies only on dnscrypt-proxy 
- A bunch of utilities and tools to help you debug, change, htpasswd, etc the configurations inside the container
- Minimal adguardhome.yaml configuration - this will be rewritten and ignored regardless once you configure adguard
- dnscrypt-proxy will act as an upstream DNS encrypting all traffic towards dnscrypt servers with load balancing (the 5 fastest)


## Prerequisites
- Docker (up and running) , you can modify the Dockerfile to buildx in case of more recent dockers
- Check the device you are going to install the container for firewall rules in outgoing or incomming that may block dnscrypt, or your local DNS traffic
- Change the /var/local/workdir & confdir on accordingly (or edit the docker run to match yours)
- Make sure the ports you choose don't conflict with what's already running on your host (netstat -ptluna)
- If you have a dnsmasq running I advice to configure port=0 on dnsmasq.conf and restart to disable it's listening on port 53


## DNSCrypt-Proxy Configuration 
- Listener on 0.0.0.0:5353
- Privacy features
```
dnscrypt_ephemeral_keys = true   # Unique key per query
require_nolog = true             # No-log policy enforcement
require_nofilter = true          # No-filtering policy
```
- Performance
```
lb_strategy = "p3"               # Load balance across fastest 3 servers
cache = true                     # Enable response caching
cache_size = 4096                # Cache entries
```
- Daemon logging
The log_file = '/var/log/dnscrypt-proxy/dnscrypt-proxy.log' is **NOT** used for DNS queries, just for the daemon, 
if you want to see the DNS traffic then uncomment ``# file = '/var/log/dnscrypt-proxy/query.log'``



### Build
```
docker build -t adguard-dnscrypt-v1 .
```
### Start
```
docker run -d --name adguard-dnscrypt \
    --restart unless-stopped \
    -v /var/local/workdir:/opt/adguardhome/work \
    -v /var/local/confdir:/opt/adguardhome/conf \
    -v /etc/timezone:/etc/timezone:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -p 81:81/tcp \
    -p 3000:3000/tcp \
    -p 53:53/tcp \
    -p 53:53/udp \
    adguard-dnscrypt-v1
```

### Login inside the container
```
docker exec -it adguard-dnscrypt /bin/bash
```

### Restart the container
```
docker restart adguard-dnscrypt
```

### Check the status or restart the service
```
supervisorctl restart adguardhome
adguardhome: stopped
adguardhome: started

supervisorctl status adguardhome
adguardhome                      RUNNING   pid 37, uptime 0:00:48
```

## How-To adguard-home
- Build the container (after downloading)
- Start the container
- Visit http://your-device-IP:3000 - this will be available for first configurations
- Do the basic configuration, specify the port to 81 (or adapt accordingly) and set your user/password
- Visit http://your-device-IP:81 login and on settings > DNS Settings set 127.0.0.1:5353 **twice** (didn't spend time debugging but adguard-home has some weird behaviors)
- Save and configure as you want your adguard-home
- I wouldn't recommend enabling any encryption option since dnscrypt-proxy will act as upstream
