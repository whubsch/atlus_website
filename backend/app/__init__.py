"""Backend for the atlus code."""

from importlib.metadata import PackageNotFoundError, version

try:
    VERSION = version("atlus")
except PackageNotFoundError:
    VERSION = "unknown"
