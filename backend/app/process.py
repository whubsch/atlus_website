from typing import OrderedDict
import usaddress
import regex
from .resources import (
    street_expand,
    direction_expand,
    name_expand,
    saints,
    state_expand,
)

toss_tags = [
    "Recipient",
    "IntersectionSeparator",
    "LandmarkName",
    "USPSBoxGroupID",
    "USPSBoxGroupType",
    "USPSBoxID",
    "USPSBoxType",
    "OccupancyType",
]

osm_mapping = {
    "AddressNumber": "addr:housenumber",
    "AddressNumberPrefix": "addr:housenumber",
    "AddressNumberSuffix": "addr:housenumber",
    "StreetName": "addr:street",
    "StreetNamePreDirectional": "addr:street",
    "StreetNamePreModifier": "addr:street",
    "StreetNamePreType": "addr:street",
    "StreetNamePostDirectional": "addr:street",
    "StreetNamePostModifier": "addr:street",
    "StreetNamePostType": "addr:street",
    "OccupancyIdentifier": "addr:unit",
    "PlaceName": "addr:city",
    "StateName": "addr:state",
    "ZipCode": "addr:postcode",
}


def lower_match(match: regex.Match) -> str:
    """Lower-case improperly cased ordinal values."""
    return match.group(1).lower()


def get_title(value: str) -> str:
    """Fix ALL-CAPS string."""
    return mc_replace(value.title()) if (value.isupper() and " " in value) else value


def us_replace(value: str) -> str:
    """Fix string containing improperly formatted US."""
    return value.replace("U.S.", "US")


def mc_replace(value: str) -> str:
    """Fix string containing improperly formatted Mc- prefix."""
    mc_match = regex.search(r"(.*\bMc)([a-z])(.*)", value)
    if mc_match:
        return mc_match.group(1) + mc_match.group(2).title() + mc_match.group(3)
    return value


def ord_replace(value: str) -> str:
    """Fix string containing improperly capitalized ordinal."""
    return regex.sub(r"(\b[0-9]+[SNRT][tTdDhH]\b)", lower_match, value)


def name_street_expand(match: regex.Match) -> str:
    """Expand matched street type abbreviations."""
    mat = match.group(1).upper().rstrip(".")
    if mat:
        return (name_expand | street_expand)[mat].title()
    raise ValueError


def direct_expand(match: regex.Match) -> str:
    """Expand matched directional abbreviations."""
    mat = match.group(1).upper().replace(".", "")
    if mat:
        return direction_expand[mat].title()
    raise ValueError


# pre-compile regex for speed
abbr_join = "|".join(name_expand | street_expand)
abbr_join_comp = regex.compile(
    rf"(\b(?:{abbr_join})\b\.?)(?!')",
    flags=regex.IGNORECASE,
)

dir_fill = "|".join(r"\.?".join(list(abbr)) for abbr in direction_expand)
dir_fill_comp = regex.compile(
    rf"(?<!(?:^(?:Avenue) |[\.']))(\b(?:{dir_fill})\b\.?)(?!(?:\.?[a-zA-Z]| (?:Street|Avenue)))",
    flags=regex.IGNORECASE,
)

sr_comp = regex.compile(
    r"(\bS\.?R\b\.?)(?= [0-9]+)",
    flags=regex.IGNORECASE,
)

saint_comp = regex.compile(
    rf"^(St\.?)(?= )|(\bSt\.?)(?= (?:{'|'.join(saints)}))",
    flags=regex.IGNORECASE,
)

street_comp = regex.compile(
    r"St\.?(?= [NESW]\.?[EW]?\.?)|(?<=[0-9][thndstr]{2} )St\.?\b|St\.?$"
)

post_comp = regex.compile(r"([0-9]{5})-?0{4}")


def abbrs(value: str) -> str:
    """Bundle most common abbreviation expansion functions."""
    value = ord_replace(us_replace(mc_replace(get_title(value)))).replace("  ", " ")

    # change likely 'St' to 'Saint'
    value = saint_comp.sub(
        "Saint",
        value,
    )

    # expand common street and word abbreviations
    value = abbr_join_comp.sub(
        name_street_expand,
        value,
    )

    # expand directionals
    value = dir_fill_comp.sub(
        direct_expand,
        value,
    )

    # expand 'SR' if no other street types
    value = sr_comp.sub("State Route", value)
    return value.rstrip().lstrip().replace("  ", " ")


def process(address_string) -> OrderedDict[str, str | int]:
    """Help process address strings"""
    cleaned = usaddress.tag(address_string, tag_mapping=osm_mapping)[0]

    for toss in toss_tags:
        cleaned.pop(toss, None)

    if "addr:street" in cleaned:
        street = abbrs(cleaned["addr:street"])
        cleaned["addr:street"] = street_comp.sub(
            "Street",
            street,
        )

    if "addr:city" in cleaned:
        cleaned["addr:city"] = abbrs(cleaned["addr:city"])

    if "addr:state" in cleaned:
        if cleaned["addr:state"].upper() in state_expand:
            cleaned["addr:state"] = state_expand.get(cleaned["addr:state"].upper())
        elif len(cleaned["addr:state"]) == 2:
            cleaned["addr:state"] = cleaned["addr:state"].upper()

    if "addr:postcode" in cleaned:
        # remove extraneous postcode digits
        cleaned["addr:postcode"] = post_comp.sub(r"\1", cleaned["addr:postcode"])

    return cleaned
