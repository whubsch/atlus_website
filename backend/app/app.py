from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .process import process


app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


class AddressListInput(AddressInput):
    id: int = Field(
        alias="@id", description="Unique identifier to help match with outputs."
    )


class AddressReturnBase(BaseModel):
    """Define address parsing fields."""

    addr_housenumber: int | None = Field(
        alias="addr:housenumber",
        description="The house number that is included in the address.",
        examples=["200"],
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
    id: int = Field(
        alias="@id",
        description="Unique identifier to help match with inputs.",
        default=0,
    )


class AddressReturn(BaseModel):
    data: AddressReturnBase
    meta: ApiMeta = Field(default=ApiMeta())


class AddressListReturn(BaseModel):
    data: list[AddressReturnBase]
    meta: ApiMeta = Field(default=ApiMeta())


@app.get("/")
async def root() -> ApiMeta:
    """Base route."""
    return ApiMeta()


@app.post("/api/parse/", response_model_exclude_none=True)
async def single(address: AddressInput) -> AddressReturn:
    """Return a single parsed address."""
    return AddressReturn(data=dict(process(address.address)))


@app.post("/api/batch/", response_model_exclude_none=True)
async def batch(addresses: list[AddressListInput]) -> AddressListReturn:
    """Return a batch of parsed addresses."""
    cleaned = []
    for address in addresses:
        cleaned.append(dict(process(address.address)) | {"@id": address.id})
    return AddressListReturn(data=cleaned)
