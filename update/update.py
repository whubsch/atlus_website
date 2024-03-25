"""Update dynamic DNS for Namecheap."""

import time
import logging
import requests

from priv import DOMAIN, PASS, HOSTS, BASE, INTERVAL


def get_my_ip() -> str | None:
    """Get my current IP address."""
    try:
        response = requests.get("https://ifconfig.me/ip", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except TimeoutError as e:
        logging.error(e)


def update_dynamic_dns(ip_address: str | None) -> str | None:
    """Update DNS dynamically."""
    my_ip = get_my_ip()
    if my_ip and my_ip != ip_address:
        logging.info("Setting IP address as %s", my_ip)
        for host in HOSTS:
            url = f"{BASE}/update?domain={DOMAIN}&password={PASS}&host={host}"

            try:
                requests.get(url, timeout=10)
            except TimeoutError as e:
                logging.error(e)
                return ip_address
        return my_ip
    return ip_address


if __name__ == "__main__":
    ip = None
    while True:
        ip = update_dynamic_dns(ip)
        time.sleep(INTERVAL)
