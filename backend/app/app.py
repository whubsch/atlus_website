"""App entrypoint."""

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from pydantic_core import ErrorDetails

import atlus

from . import VERSION

router = APIRouter()


class ApiMeta(BaseModel):
    """Define basic API features."""

    version: str = Field(default=VERSION)
    status: str = Field(default="OK")


class AddressInput(BaseModel):
    """Define address parsing input."""

    address: str = Field(
        description="The raw address string that needs to be parsed.",
        examples=[
            "200 N. Spring St, Los Angeles, California 90012",
            "1600 Pennsylvania Ave NW Washington, DC 20500",
            "89 Broadway, New York, NY 10006",
        ],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )

    def make_error(self):
        """Convert to error submodel."""
        return ErrorAddressReturn(**self.model_dump())


class ErrorAddressReturn(AddressInput):
    """Define address error submodel."""

    error: str = Field(default="Unparseable", description="The error message.")


class AddressReturnBase(BaseModel):
    """Define address parsing fields."""

    addr_housenumber: int | str | None = Field(
        alias="addr:housenumber",
        description="The house number that is included in the address.",
        examples=[200, "1200-29"],
        default=None,
    )
    addr_street: str | None = Field(
        alias="addr:street",
        description="The street that the address is located on.",
        examples=["North Spring Street"],
        default=None,
    )
    addr_unit: str | None = Field(
        alias="addr:unit",
        description="The unit number or letter that is included in the address.",
        examples=["B"],
        default=None,
    )
    addr_city: str | None = Field(
        alias="addr:city",
        description="The city that the address is located in.",
        examples=["Los Angeles"],
        default=None,
    )
    addr_state: str | None = Field(
        alias="addr:state",
        pattern=r"^[A-Z]{2}$",
        description="The state or territory of the address.",
        examples=["CA"],
        default=None,
    )
    addr_postcode: str | None = Field(
        alias="addr:postcode",
        pattern=r"^\d{5}(?:\-\d{4})?$",
        description="The postal code of the address.",
        examples=["90012", "90012-4801"],
        default=None,
    )
    removed: list[str | None] = Field(
        alias="@removed",
        description="Any fields that were removed because they were unparseable.",
        default=[],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with inputs.",
        default=0,
    )


class AddressReturn(BaseModel):
    """Define address parsing output."""

    data: AddressReturnBase | ErrorAddressReturn
    meta: ApiMeta = Field(default=ApiMeta())


class AddressListReturn(BaseModel):
    """Define multiple address parsing output."""

    data: list[AddressReturnBase | ErrorAddressReturn]
    meta: ApiMeta = Field(default=ApiMeta())


class PhoneInput(BaseModel):
    """Define phone parsing input."""

    phone: str = Field(
        description="The raw phone string that needs to be parsed.",
        examples=["1234567890", "545-098-0988", "+1 (908) 930-3099"],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )

    def make_error(self):
        """Convert to error submodel."""
        return ErrorPhoneReturn(**self.model_dump())


class ErrorPhoneReturn(PhoneInput):
    """Define phone error submodel."""

    error: str = Field(default="Unparseable", description="The error message.")


class PhoneReturnBase(BaseModel):
    """Define phone parsing fields to return."""

    phone: str = Field(
        description="The raw phone string that needs to be parsed.",
        examples=["1234567890", "545-098-0988", "+1 (908) 930-3099"],
        pattern=r"^\+1-\d{3}-\d{3}-\d{4}$",
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )


class PhoneReturn(BaseModel):
    """Define phone parsing output."""

    data: PhoneReturnBase | ErrorPhoneReturn
    meta: ApiMeta = Field(default=ApiMeta())


class PhoneListReturn(BaseModel):
    """Define multiple phone parsing output."""

    data: list[PhoneReturnBase | ErrorPhoneReturn]
    meta: ApiMeta = Field(default=ApiMeta())


class HoursInput(BaseModel):
    """Define opening hours parsing input."""

    hours: str = Field(
        description="The raw opening hours string that needs to be parsed.",
        examples=[
            "Mo-Fr 08:00-12:00,13:00-17:30",
            "Monday to Friday 9am-5pm, Saturday 9am-12pm",
            "Closed",
        ],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )

    def make_error(self, message: str | None = None):
        """Convert to error submodel."""
        if message:
            return ErrorHoursReturn(**self.model_dump(), error=message)
        return ErrorHoursReturn(**self.model_dump())


class ErrorHoursReturn(HoursInput):
    """Define opening hours error submodel."""

    error: str = Field(default="Unparseable", description="The error message.")


class HoursReturnBase(BaseModel):
    """Define opening hours parsing fields to return."""

    opening_hours: str = Field(
        description="The formatted opening hours string.",
        examples=["Mo-Fr 08:00-12:00,13:00-17:30", "off", "24/7"],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )


class HoursReturn(BaseModel):
    """Define opening hours parsing output."""

    data: HoursReturnBase | ErrorHoursReturn
    meta: ApiMeta = Field(default=ApiMeta())


class HoursListReturn(BaseModel):
    """Define multiple opening hours parsing output."""

    data: list[HoursReturnBase | ErrorHoursReturn]
    meta: ApiMeta = Field(default=ApiMeta())


def check_fields(return_dict: dict[str, str | list]) -> bool:
    """Check if zero or one values are not None."""
    removed_keys = ["removed", "oid"]
    for remove_key in removed_keys:
        return_dict.pop(remove_key, None)
    count = sum(1 for value in return_dict.values() if value is not None)
    return count <= 1


def validate(content: AddressInput) -> AddressReturnBase | ErrorAddressReturn:
    """Solve and resolve address inputs."""
    cleaned = {}
    try:
        cleaned, removed = atlus.get_address(content.address)
        add_return = AddressReturnBase.model_validate(
            dict(cleaned) | {"@id": content.oid, "@removed": removed}
        )
    except ValidationError as e:
        bad_fields: list = [each.get("loc")[0] for each in e.errors()]
        cleaned_ret = dict(cleaned)
        for each in bad_fields:
            cleaned_ret.pop(each, None)

        add_return = AddressReturnBase.model_validate(
            cleaned_ret | {"@id": content.oid, "@removed": bad_fields}
        )
    if check_fields(add_return.model_dump()):
        return content.make_error()
    return add_return


@router.get("/meta")
async def meta() -> ApiMeta:
    """Return meta information. Helpful to check if service is up."""
    return ApiMeta()


@router.post("/address/parse/", response_model_exclude_none=True, name="address parse")
async def single(address: AddressInput) -> AddressReturn:
    """Return a single parsed address."""
    return AddressReturn(data=validate(address))


@router.post("/address/batch/", response_model_exclude_none=True, name="address batch")
async def batch(addresses: list[AddressInput]) -> AddressListReturn:
    """Return a batch of parsed addresses. Limit of 10,000 items per request."""
    if len(addresses) > 10000:
        raise HTTPException(
            status_code=400,
            detail="More than 10,000 items. Submit request in smaller batches.",
        )
    if len({i.oid for i in addresses}) != len(addresses):
        raise HTTPException(status_code=400, detail="Ids [@id] are not unique.")

    cleaned = [validate(address) for address in addresses]
    return AddressListReturn(data=cleaned)


def phone_process(phone: PhoneInput) -> PhoneReturnBase | ErrorPhoneReturn:
    """Help to format."""
    try:
        phone_new = atlus.get_phone(phone.phone)
        return PhoneReturnBase.model_validate({"phone": phone_new, "@id": phone.oid})
    except ValueError:
        return phone.make_error()


@router.post("/phone/parse/", response_model_exclude_none=True, name="phone parse")
async def phone_parse(phone: PhoneInput) -> PhoneReturn:
    """Format US and Canada phone numbers."""
    return PhoneReturn(data=phone_process(phone))


@router.post("/phone/batch/", response_model_exclude_none=True, name="phone batch")
async def phone_batch(phones: list[PhoneInput]) -> PhoneListReturn:
    """Format US and Canada phone numbers. Limit of 10,000 items per request."""
    if len(phones) > 10000:
        raise HTTPException(
            status_code=400,
            detail="More than 10,000 items. Submit request in smaller batches.",
        )
    if len({i.oid for i in phones}) != len(phones):
        raise HTTPException(status_code=400, detail="Ids [@id] are not unique.")

    cleaned = [phone_process(phone) for phone in phones]
    return PhoneListReturn(data=cleaned)


def _describe_hours_error(exc: ValueError) -> str:
    """Turn an atlus/pydantic exception into a readable error message.

    atlus.get_hours raises either a plain ValueError with a human-readable
    message, or lets a pydantic ValidationError bubble up (which is itself a
    ValueError subclass) when the parsed rules fail model validation. This
    normalizes both into a single, concise, user-facing string.
    """
    if isinstance(exc, ValidationError):
        details: list[ErrorDetails] = exc.errors()
        messages = []
        for detail in details:
            loc = ".".join(str(part) for part in detail["loc"])
            msg = detail["msg"].removeprefix("Value error, ")
            messages.append(f"{loc}: {msg}" if loc else msg)
        return "; ".join(messages) if messages else str(exc)
    return str(exc)


def hours_process(hours: HoursInput) -> HoursReturnBase | ErrorHoursReturn:
    """Help to format."""
    try:
        hours_new = atlus.get_hours(hours.hours)
        return HoursReturnBase.model_validate(
            {"opening_hours": hours_new, "@id": hours.oid}
        )
    except ValueError as e:
        return hours.make_error(_describe_hours_error(e))


@router.post("/hours/parse/", response_model_exclude_none=True, name="hours parse")
async def hours_parse(hours: HoursInput) -> HoursReturn:
    """Format raw opening hours strings into the OSM opening_hours format."""
    return HoursReturn(data=hours_process(hours))


@router.post("/hours/batch/", response_model_exclude_none=True, name="hours batch")
async def hours_batch(hours: list[HoursInput]) -> HoursListReturn:
    """Format raw opening hours strings. Limit of 10,000 items per request."""
    if len(hours) > 10000:
        raise HTTPException(
            status_code=400,
            detail="More than 10,000 items. Submit request in smaller batches.",
        )
    if len({i.oid for i in hours}) != len(hours):
        raise HTTPException(status_code=400, detail="Ids [@id] are not unique.")

    cleaned = [hours_process(each) for each in hours]
    return HoursListReturn(data=cleaned)


DESC = """
Access the powers of Atlus using a public API to automate your workflow and work
with bigger datasets quickly.

Follow the clear and auto-generated documentation below to get a consistent and
reliable output. Note that fields that are not found in the address string are
not returned.

For documentation on the OSM data this application follows, check
[the OSM wiki](https://wiki.openstreetmap.org/wiki/Addresses).

I welcome issues and pull requests at the
[Atlus Github repository.](https://github.com/whubsch/atlus/)
"""

app = FastAPI(
    title="Atlus - API",
    description=DESC,
    version=VERSION,
    license_info={
        "name": "MIT",
        "identifier": "MIT",
        "url": "https://github.com/whubsch/atlus/blob/main/LICENSE",
    },
    root_path="",  # No prefix when using custom domain
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router=router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
