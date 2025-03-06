## What is this?
I like adguard-home, it provides an easy way through it's interface to control the DNS traffic, by enabling us to block domains that we don't like for our entire home network.
**However** , I didn't like how it didn't how by default it doesn't encrypt the DNS traffic (which adds security and privacy).
Yes, it provides DoH , etc out-of-the box but they are not particularly private, so I wanted to have it interact with dnscrypt-proxy.
There's some documentation around but I didn't have much access inside the default adguard-home container, I couldn't tweak it and I didn't know what was going on inside,and as with any open source it's good to build your own, here's the : 

## Feature List
- Arch Linux container
- Official Arch linux dnscrypt-proxy and adguard-home packages (no AUR, from extras)
- Added supervisord for monitoring the services
- Custom dnscrypt-proxy configuration which disables by default DoH and relies only on dnscrypt-proxy 
- A bunch of utilities and tools to help you debug, change, htpasswd, etc the configurations inside the container
- Minimal adguardhome.yaml configuration - this will be rewritten and ignored regardless
- dnscrypt-proxy will act as an upstream DNS encrypting all traffic towards dnscrypt servers with load balancing (the 5 fastest)


## Prerequisites
1) Docker (up and running) , you can modify the Dockerfile to buildx in case of more recent dockers
2) Check the device you are going to install the container for firewall rules in outgoing or incomming that may block dnscrypt, or your local DNS traffic
3) Change the /var/local/workdir & confdir on accordingly (or edit the docker run to match yours)
4) Make sure the ports you choose don't conflict with what's already running on your host (netstat -ptluna)
5) If you have a dnsmasq running I advice to configure port=0 on dnsmasq.conf and restart to disable it's listening on port 53


## How-To
1) Build the container (after downloading)
2) Start the container
3) Visit http://your-device-IP:3000
4) Do the basic configuration, specify the port to 81 and set your user/password
5) Visit http://your-device-IP:81 login and on settings > DNS Settings set 127.0.0.1:5353 **twice**

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




