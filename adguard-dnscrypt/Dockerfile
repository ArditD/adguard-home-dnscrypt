# Use Arch Linux as the base image
FROM archlinux:latest

# Update package database and install dependencies
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
    dnscrypt-proxy adguardhome nano lsof drill curl less \
    # Note - we need apache for htpasswd in case we want to update the password
    wget tcpdump bind-tools net-tools supervisor apache \
    && pacman -Scc --noconfirm

# Some provisioning & minor tweaks
RUN rm /etc/adguardhome.yaml && mkdir /var/log/dnscrypt-proxy/ && \
    mkdir -p /opt/adguardhome/work && mkdir /var/cache/dnscrypt-proxy/

# Copy configuration files
COPY dnscrypt-proxy.toml /etc/dnscrypt-proxy/dnscrypt-proxy.toml
COPY adguardhome.yaml /opt/adguardhome/conf/AdGuardHome.yaml
COPY supervisord.conf /etc/supervisord.conf

# Expose necessary ports (DNS and AdGuard Home web interface)
EXPOSE 53/tcp 53/udp 3000/tcp 81/tcp

# Start supervisord to manage both services
CMD ["supervisord", "-c", "/etc/supervisord.conf"]