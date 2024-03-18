from collections import Counter
from typing import OrderedDict
import usaddress
import regex
from app.resources import (
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


def get_title(value: str, single_word: bool = False) -> str:
    """Fix ALL-CAPS string."""
    if (value.isupper() and " " in value) or (value.isupper() and single_word):
        return mc_replace(value.title())
    return value


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
ABBR_JOIN = "|".join(name_expand | street_expand)
abbr_join_comp = regex.compile(
    rf"(\b(?:{ABBR_JOIN})\b\.?)(?!')",
    flags=regex.IGNORECASE,
)

DIR_FILL = "|".join(r"\.?".join(list(abbr)) for abbr in direction_expand)
dir_fill_comp = regex.compile(
    rf"(?<!(?:^(?:Avenue) |[\.']))(\b(?:{DIR_FILL})\b\.?)(?!(?:\.?[a-zA-Z]| (?:Street|Avenue)))",
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

    # normalize 'US'
    value = regex.sub(
        r"\bU.[Ss].\B",
        "US",
        value,
    )

    # remove unremoved abbr periods
    value = regex.sub(
        r"([a-zA-Z]{2,})\.",
        r"\1",
        value,
    )

    # expand 'SR' if no other street types
    value = sr_comp.sub("State Route", value)
    return value.strip(" .").replace("  ", " ")


def clean(old: str) -> str:
    """Clean the input string before sending to parser."""
    old = regex.sub(r"<br ?/>", ",", old)
    return regex.sub(r"[^\x00-\x7F\n\r\t]", "", old)  # remove unicode


def help_join(tags, keep: list[str]) -> str:
    """Help to join address fields."""
    tag_join: list[str] = [v for k, v in tags.items() if k in keep]
    return " ".join(tag_join)


def addr_street(tags: dict[str, str]) -> str:
    """Help build the street field."""
    return help_join(
        tags,
        [
            "StreetName",
            "StreetNamePreDirectional",
            "StreetNamePreModifier",
            "StreetNamePreType",
            "StreetNamePostDirectional",
            "StreetNamePostModifier",
            "StreetNamePostType",
        ],
    )


def addr_housenumber(tags: dict[str, str]) -> str:
    """Help build the housenumber field."""
    return help_join(
        tags, ["AddressNumberPrefix", "AddressNumber", "AddressNumberSuffix"]
    )


def combine_consecutive_tuples(
    tuples_list: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    """Join adjacent `usaddress` fields."""
    combined_list = []
    current_tag = None
    current_value = None

    for value, tag in tuples_list:
        if tag != current_tag:
            if current_tag:
                combined_list.append((current_value, current_tag))
            current_value, current_tag = value, tag
        else:
            current_value = " ".join(i for i in [current_value, value] if i)

    if current_tag:
        combined_list.append((current_value, current_tag))

    return combined_list


def manual_join(parsed: list[tuple]) -> tuple[dict[str, str], list[str | None]]:
    """Remove duplicates and join remaining fields."""
    a = [i for i in parsed if i[1] not in toss_tags]
    counts = Counter([i[1] for i in a])
    ok_tags = [tag for tag, count in counts.items() if count == 1]
    ok_dict: dict[str, str] = {i[1]: i[0] for i in a if i[1] in ok_tags}
    removed = [osm_mapping.get(field) for field, count in counts.items() if count > 1]

    new_dict: dict[str, str | None] = {}
    if "addr:street" not in removed:
        new_dict["addr:street"] = addr_street(ok_dict)
    if "addr:housenumber" not in removed:
        new_dict["addr:housenumber"] = addr_housenumber(ok_dict)
    if "addr:unit" not in removed:
        new_dict["addr:unit"] = ok_dict.get("OccupancyIdentifier")
    if "addr:city" not in removed:
        new_dict["addr:city"] = ok_dict.get("PlaceName")
    if "addr:state" not in removed:
        new_dict["addr:state"] = ok_dict.get("StateName")
    if "addr:postcode" not in removed:
        new_dict["addr:postcode"] = ok_dict.get("ZipCode")

    return {k: v for k, v in new_dict.items() if v}, removed


def collapse_list(seq: list) -> list:
    """Remove duplicates in list while keeping order."""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def process(
    address_string: str,
) -> tuple[OrderedDict[str, str | int], list[str | None]]:
    """Process address strings."""
    try:
        cleaned = usaddress.tag(clean(address_string), tag_mapping=osm_mapping)[0]
        removed = []
    except usaddress.RepeatedLabelError as e:
        collapsed = collapse_list([(i[0].strip(" .,#"), i[1]) for i in e.parsed_string])
        cleaned, removed = manual_join(combine_consecutive_tuples(collapsed))

    for toss in toss_tags:
        cleaned.pop(toss, None)

    if "addr:street" in cleaned:
        street = abbrs(cleaned["addr:street"])
        cleaned["addr:street"] = street_comp.sub(
            "Street",
            street,
        ).strip(".")

    if "addr:city" in cleaned:
        cleaned["addr:city"] = abbrs(get_title(cleaned["addr:city"], single_word=True))

    if "addr:state" in cleaned:
        old = cleaned["addr:state"].replace(".", "").removesuffix(", USA")
        if old.upper() in state_expand:
            cleaned["addr:state"] = state_expand[old.upper()]
        elif len(old) == 2:
            cleaned["addr:state"] = old.upper()

    if "addr:unit" in cleaned:
        cleaned["addr:unit"] = cleaned["addr:unit"].strip(" #.")

    if "addr:postcode" in cleaned:
        # remove extraneous postcode digits
        cleaned["addr:postcode"] = post_comp.sub(r"\1", cleaned["addr:postcode"])

    return cleaned, removed
