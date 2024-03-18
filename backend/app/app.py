from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError

from pydantic_core import ErrorDetails
from usaddress import RepeatedLabelError

from app.process import process


app = FastAPI()


origins = [
    "http://localhost:5000",
    "localhost:5000",
    "http://127.0.0.1:5000",
    "127.0.0.1:5000",
    "http://localhost",
    "localhost",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)


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


@app.get("/", response_class=FileResponse)
async def base() -> FileResponse:
    """Display single-page React frontend."""
    return FileResponse("../atlus/dist/index.html")


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


@app.post("/api/parse/", response_model_exclude_none=True)
async def single(address: AddressInput) -> AddressReturn:
    """Return a single parsed address."""
    return AddressReturn(data=validate(address))


@app.post("/api/batch/", response_model_exclude_none=True)
async def batch(addresses: list[AddressInput]) -> AddressListReturn:
    """Return a batch of parsed addresses."""
    if len({i.oid for i in addresses}) != len(addresses):
        raise HTTPException(status_code=400, detail="Ids [@id] are not unique.")

    cleaned = []
    for address in addresses:
        cleaned.append(validate(address))
    return AddressListReturn(data=cleaned)
