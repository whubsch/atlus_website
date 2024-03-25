"""Update dynamic DNS for Namecheap."""

import time
import requests

from priv import DOMAIN, PASS, HOSTS, BASE, INTERVAL


def update_dynamic_dns() -> None:
    """Update DNS dynamically."""
    for host in HOSTS:
        url = f"{BASE}/update?domain={DOMAIN}&password={PASS}&host={host}"

        requests.get(url, timeout=10)


if __name__ == "__main__":
    while True:
        update_dynamic_dns()
        time.sleep(INTERVAL)  # Sleep for 300 seconds (5 minutes)
