from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError

import regex

from app.process import process

router = APIRouter()


class ApiMeta(BaseModel):
    """Define basic API features."""

    version: str = Field(default="0.1.0")
    status: str = Field(default="OK")


class AddressInput(BaseModel):
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


class ErrorAddressReturn(AddressInput):
    error: str = Field(
        default="Unparseable",
        description="The raw address string that needs to be parsed.",
    )


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
        pattern="^[A-Z]{2}$",
        description="The state or territory of the address.",
        examples=["CA"],
        default=None,
    )
    addr_postcode: str | None = Field(
        alias="addr:postcode",
        pattern="^[0-9]{5}(?:-[0-9]{4})?$",
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
    data: AddressReturnBase | ErrorAddressReturn
    meta: ApiMeta = Field(default=ApiMeta())


class AddressListReturn(BaseModel):
    data: list[AddressReturnBase | ErrorAddressReturn]
    meta: ApiMeta = Field(default=ApiMeta())


class PhoneInput(BaseModel):
    phone: str = Field(
        description="The raw phone string that needs to be parsed.",
        examples=[
            "1234567890",
            "545-098-0988",
            "+1 (908) 930-3099",
        ],
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )


class ErrorPhoneReturn(PhoneInput):
    error: str = Field(
        default="Unparseable",
        description="The raw phone string that needs to be parsed.",
    )


class PhoneReturnBase(BaseModel):
    phone: str = Field(
        description="The raw phone string that needs to be parsed.",
        examples=[
            "1234567890",
            "545-098-0988",
            "+1 (908) 930-3099",
        ],
        pattern=r"^\+1 [0-9]{3}-[0-9]{3}-[0-9]{4}$",
    )
    oid: int | str = Field(
        alias="@id",
        description="Unique identifier to help match with outputs.",
        default=0,
    )


class PhoneReturn(BaseModel):
    data: PhoneReturnBase | ErrorPhoneReturn
    meta: ApiMeta = Field(default=ApiMeta())


class PhoneListReturn(BaseModel):
    data: list[PhoneReturnBase | ErrorPhoneReturn]
    meta: ApiMeta = Field(default=ApiMeta())


# @app.get("/", response_class=FileResponse)
# async def base() -> FileResponse:
#     """Display single-page React frontend."""
#     return FileResponse("../atlus/dist/index.html")


def validate(content: AddressInput) -> AddressReturnBase | ErrorAddressReturn:
    """Solve and resolve address inputs."""
    try:
        cleaned, removed = process(content.address)
        add_return = AddressReturnBase.model_validate(
            dict(cleaned) | {"@id": content.oid, "@removed": removed}
        )
    except ValidationError as e:
        bad_fields: list[str] = [each.get("loc")[0] for each in e.errors()]
        cleaned_ret = dict(cleaned)
        for each in bad_fields:
            cleaned_ret.pop(each, None)

        add_return = AddressReturnBase.model_validate(
            cleaned_ret | {"@id": content.oid, "@removed": bad_fields}
        )
    return add_return


@router.get("/")
async def meta() -> ApiMeta:
    """Return meta information."""
    return ApiMeta()


@router.post("/address/parse/", response_model_exclude_none=True)
async def single(address: AddressInput) -> AddressReturn:
    """Return a single parsed address."""
    return AddressReturn(data=validate(address))


@router.post("/address/batch/", response_model_exclude_none=True)
async def batch(addresses: list[AddressInput]) -> AddressListReturn:
    """Return a batch of parsed addresses."""
    if len({i.oid for i in addresses}) != len(addresses):
        raise HTTPException(status_code=400, detail="Ids [@id] are not unique.")

    cleaned = [validate(address) for address in addresses]
    return AddressListReturn(data=cleaned)


def phone_process(phone: PhoneInput) -> PhoneReturnBase | ErrorPhoneReturn:
    """Help to format."""
    phone_valid = regex.search(
        r"^\(?(?:\+? ?1?[ -.]*)?(?:\(?([0-9]{3})\)?[ -.]*)([0-9]{3})[ -.]*([0-9]{4})$",
        phone.phone,
    )
    if phone_valid:
        phone_new = (
            f"+1 {phone_valid.group(1)}-{phone_valid.group(2)}-{phone_valid.group(3)}"
        )
        return PhoneReturnBase.model_validate({"phone": phone_new, "@id": phone.oid})
    return ErrorPhoneReturn.model_validate({"phone": phone.phone, "@id": phone.oid})


@router.post("/phone/parse/", response_model_exclude_none=True)
async def phone_parse(phone: PhoneInput) -> PhoneReturn:
    """Format US and Canada phone numbers."""
    return PhoneReturn(data=phone_process(phone))


@router.post("/phone/batch/", response_model_exclude_none=True)
async def phone_batch(phones: list[PhoneInput]) -> PhoneListReturn:
    """Format US and Canada phone numbers."""
    cleaned = [phone_process(phone) for phone in phones]
    return PhoneListReturn(data=cleaned)


app = FastAPI()

app.include_router(router=router, prefix="/api")

origins = [
    "http://localhost:5000",
    "localhost:5000",
    "http://127.0.0.1:5000",
    "127.0.0.1:5000",
    "http://localhost",
    "localhost",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)
