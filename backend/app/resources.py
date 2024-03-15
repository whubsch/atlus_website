"""Hold info for the processing script."""

direction_expand = {
    "NE": "Northeast",
    "SE": "Southeast",
    "NW": "Northwest",
    "SW": "Southwest",
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West",
}

name_expand = {
    "ARPT": "airport",
    "BLDG": "building",
    "CONF": "conference",
    "CONV": "convention",
    "CNTR": "center",
    "CTR": "center",
    "DWTN": "downtown",
    "INTL": "international",
    "FT": "fort",
    "MT": "mount",
    "MTN": "mountain",
    "SHPG": "shopping",
}

state_expand = {
    "ALABAMA": "AL",
    "ALA": "AL",
    "ALASKA": "AK",
    "ALAS": "AK",
    "ARIZONA": "AZ",
    "ARIZ": "AZ",
    "ARKANSAS": "AR",
    "ARK": "AR",
    "CALIFORNIA": "CA",
    "CALIF": "CA",
    "CAL": "CA",
    "COLORADO": "CO",
    "COLO": "CO",
    "COL": "CO",
    "CONNECTICUT": "CT",
    "CONN": "CT",
    "DELAWARE": "DE",
    "DEL": "DE",
    "DISTRICT OF COLUMBIA": "DC",
    "FLORIDA": "FL",
    "FLA": "FL",
    "FLOR": "FL",
    "GEORGIA": "GA",
    "GA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "IDA": "ID",
    "ILLINOIS": "IL",
    "ILL": "IL",
    "INDIANA": "IN",
    "IND": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KANS": "KS",
    "KAN": "KS",
    "KENTUCKY": "KY",
    "KEN": "KY",
    "KENT": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MASS": "MA",
    "MICHIGAN": "MI",
    "MICH": "MI",
    "MINNESOTA": "MN",
    "MINN": "MN",
    "MISSISSIPPI": "MS",
    "MISS": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "MONT": "MT",
    "NEBRASKA": "NE",
    "NEBR": "NE",
    "NEB": "NE",
    "NEVADA": "NV",
    "NEV": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "N MEX": "NM",
    "NEW M": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "N DAK": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OKLA": "OK",
    "OREGON": "OR",
    "OREG": "OR",
    "ORE": "OR",
    "PENNSYLVANIA": "PA",
    "PENN": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "S DAK": "SD",
    "TENNESSEE": "TN",
    "TENN": "TN",
    "TEXAS": "TX",
    "TEX": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WASH": "WA",
    "WEST VIRGINIA": "WV",
    "W VA": "WV",
    "WISCONSIN": "WI",
    "WIS": "WI",
    "WISC": "WI",
    "WYOMING": "WY",
    "WYO": "WY",
    "ONTARIO": "ON",
    "QUEBEC": "QC",
    "NOVA SCOTIA": "NS",
    "NEW BRUNSWICK": "NB",
    "MANITOBA": "MB",
    "BRITISH COLUMBIA": "BC",
    "PRINCE EDWARD ISLAND": "PE",
    "PRINCE EDWARD": "PE",
    "SASKATCHEWAN": "SK",
    "ALBERTA": "AB",
    "NEWFOUNDLAND AND LABRADOR": "NL",
    "NEWFOUNDLAND & LABRADOR": "NL",
    "NEWFOUNDLAND": "NL",
    "YUKON": "YK",
    "NUNAVUT": "NU",
    "NORTHWEST TERRITORIES": "NT",
    "NW TERRITORIES": "NT",
}

street_expand = {
    "ACC": "ACCESS",
    "ALY": "ALLEY",
    "ANX": "ANEX",
    "ARC": "ARCADE",
    "AV": "AVENUE",
    "AVE": "AVENUE",
    "BYU": "BAYOU",
    "BCH": "BEACH",
    "BND": "BEND",
    "BLF": "BLUFF",
    "BLFS": "BLUFFS",
    "BTM": "BOTTOM",
    "BLVD": "BOULEVARD",
    "BR": "BRANCH",
    "BRG": "BRIDGE",
    "BRK": "BROOK",
    "BRKS": "BROOKS",
    "BG": "BURG",
    "BGS": "BURGS",
    "BYP": "BYPASS",
    "CP": "CAMP",
    "CYN": "CANYON",
    "CPE": "CAPE",
    "CTR": "CENTER",
    "CTRS": "CENTERS",
    "CIR": "CIRCLE",
    "CIRS": "CIRCLES",
    "CLF": "CLIFF",
    "CLFS": "CLIFFS",
    "CLB": "CLUB",
    "CMN": "COMMON",
    "CMNS": "COMMONS",
    "COR": "CORNER",
    "CORS": "CORNERS",
    "CRSE": "COURSE",
    "CT": "COURT",
    "CTS": "COURTS",
    "CV": "COVE",
    "CVS": "COVES",
    "CRK": "CREEK",
    "CRES": "CRESCENT",
    "CRST": "CREST",
    "CSWY": "CAUSEWAY",
    "CURV": "CURVE",
    "DL": "DALE",
    "DM": "DAM",
    "DV": "DIVIDE",
    "DR": "DRIVE",
    "DRS": "DRIVES",
    "EXPY": "EXPRESSWAY",
    "EXPWY": "EXPRESSWAY",
    "EXT": "EXTENSION",
    "EXTS": "EXTENSIONS",
    "FLS": "FALLS",
    "FLD": "FIELD",
    "FLDS": "FIELDS",
    "FLT": "FLAT",
    "FLTS": "FLATS",
    "FRD": "FORD",
    "FRDS": "FORDS",
    "FRST": "FOREST",
    "FRG": "FORGE",
    "FRGS": "FORGES",
    "FRK": "FORK",
    "FRKS": "FORKS",
    "FT": "FORT",
    "FWY": "FREEWAY",
    "GD": "GRADE",
    "GDN": "GARDEN",
    "GDNS": "GARDENS",
    "GTWY": "GATEWAY",
    "GLN": "GLEN",
    "GLNS": "GLENS",
    "GRN": "GREEN",
    "GRNS": "GREENS",
    "GRV": "GROVE",
    "GRVS": "GROVES",
    "HBR": "HARBOR",
    "HBRS": "HARBORS",
    "HGWY": "HIGHWAY",
    "HVN": "HAVEN",
    "HTS": "HEIGHTS",
    "HWY": "HIGHWAY",
    "HL": "HILL",
    "HLS": "HILLS",
    "HOLW": "HOLLOW",
    "INLT": "INLET",
    "IS": "ISLAND",
    "ISS": "ISLANDS",
    "JCT": "JUNCTION",
    "JCTS": "JUNCTIONS",
    "KY": "KEY",
    "KYS": "KEYS",
    "KNL": "KNOLL",
    "KNLS": "KNOLLS",
    "LK": "LAKE",
    "LKS": "LAKES",
    "LNDG": "LANDING",
    "LN": "LANE",
    "LGT": "LIGHT",
    "LGTS": "LIGHTS",
    "LF": "LOAF",
    "LCK": "LOCK",
    "LCKS": "LOCKS",
    "LDG": "LODGE",
    "LP": "LOOP",
    "MNR": "MANOR",
    "MNRS": "MANORS",
    "MDW": "MEADOW",
    "MDWS": "MEADOWS",
    "ML": "MILL",
    "MLS": "MILLS",
    "MSN": "MISSION",
    "MTWY": "MOTORWAY",
    "MT": "MOUNT",
    "MTN": "MOUNTAIN",
    "MTNS": "MOUNTAINS",
    "NCK": "NECK",
    "ORCH": "ORCHARD",
    "OPAS": "OVERPASS",
    "PKY": "PARKWAY",
    "PKWY": "PARKWAY",
    "PSGE": "PASSAGE",
    "PNE": "PINE",
    "PNES": "PINES",
    "PL": "PLACE",
    "PLN": "PLAIN",
    "PLNS": "PLAINS",
    "PLZ": "PLAZA",
    "PT": "POINT",
    "PTS": "POINTS",
    "PRT": "PORT",
    "PRTS": "PORTS",
    "PR": "PRAIRIE",
    "PVT": "PRIVATE",
    "RADL": "RADIAL",
    "RNCH": "RANCH",
    "RPD": "RAPID",
    "RPDS": "RAPIDS",
    "RST": "REST",
    "RDG": "RIDGE",
    "RDGS": "RIDGES",
    "RIV": "RIVER",
    "RD": "ROAD",
    "RDS": "ROADS",
    "RT": "ROUTE",
    "RTE": "ROUTE",
    "SHL": "SHOAL",
    "SHLS": "SHOALS",
    "SHR": "SHORE",
    "SHRS": "SHORES",
    "SKWY": "SKYWAY",
    "SPG": "SPRING",
    "SPGS": "SPRINGS",
    "SQ": "SQUARE",
    "SQS": "SQUARES",
    "STA": "STATION",
    "STRA": "STRAVENUE",
    "STRM": "STREAM",
    "STS": "STREETS",
    "SMT": "SUMMIT",
    "SRVC": "SERVICE",
    "TER": "TERRACE",
    "TRWY": "THROUGHWAY",
    "THFR": "THOROUGHFARE",
    "TRCE": "TRACE",
    "TRAK": "TRACK",
    "TRFY": "TRAFFICWAY",
    "TRL": "TRAIL",
    "TRLR": "TRAILER",
    "TUNL": "TUNNEL",
    "TPKE": "TURNPIKE",
    "UPAS": "UNDERPASS",
    "UN": "UNION",
    "UNP": "UNDERPASS",
    "UNS": "UNIONS",
    "VLY": "VALLEY",
    "VLYS": "VALLEYS",
    "VW": "VIEW",
    "VWS": "VIEWS",
    "VLG": "VILLAGE",
    "VL": "VILLE",
    "VIS": "VISTA",
    "WKWY": "WALKWAY",
    "WL": "WELL",
    "WLS": "WELLS",
    "XING": "CROSSING",
    "XRD": "CROSSROAD",
    "XRDS": "CROSSROADS",
}

saints = [
    "Abigail",
    "Agatha",
    "Agnes",
    "Andrew",
    "Anthony",
    "Augustine",
    "Bernadette",
    "Brigid",
    "Catherine",
    "Charles",
    "Christopher",
    "Clare",
    "Cloud",
    "Dymphna",
    "Elizabeth",
    "Faustina",
    "Felix",
    "Francis",
    "Gabriel,",
    "George",
    "Gerard",
    "James",
    "Joan",
    "John",
    "Joseph",
    "Jude",
    "Kateri",
    "Louis",
    "Lucie",
    "Lucy",
    "Luke",
    "Maria",
    "Mark",
    "Martin",
    "Mary",
    "Maximilian",
    "Michael",
    "Monica",
    "Padre",
    "Patrick",
    "Paul",
    "Peter",
    "Philomena",
    "Raphael",
    "Rita",
    "Rose",
    "Sebastian",
    "Teresa",
    "Therese",
    "Thomas",
    "Valentine",
    "Victor",
    "Vincent",
]
