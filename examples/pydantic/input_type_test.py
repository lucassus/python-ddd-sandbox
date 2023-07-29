from typing import Optional

from pydantic import BaseModel, Field


class KeynestParams(BaseModel):
    class Config:
        allow_population_by_field_name = True


# TODO: Use single dispatch?
class CreateKeyCollectionCode(KeynestParams):
    key_id: str = Field(..., alias="KeyId")
    store_id: str = Field(..., alias="StoreId")
    user_name: Optional[str] = Field(None, alias="ExpectedCollectionUserName")
    user_email: Optional[str] = Field(None, alias="ExpectedCollectionUserEmail")


class Response1(BaseModel):
    id: int
    name: str


class Response2(BaseModel):
    id: int
    name: str
    mail: str


# @functools.singledispatch
# def call(params: KeynestParams):
#     raise NotImplementedError
#
#
# @call.register(CreateKeyCollectionCode)
# def _(params: CreateKeyCollectionCode) -> Response1:
#     return Response1(id=int(params.key_id))
#
#
# def call(params: KeynestParams) -> None:
#     ...
#
#
# @overload
# def call(params: CreateKeyCollectionCode) -> Response1:
#     return Response1(id=int(params.key_id), name="Testing...")
#
#
# def call(**kwargs: CreateKeyCollectionCode):
#     pass


def test_it():
    params = CreateKeyCollectionCode(key_id="asdf", store_id="qwerty")

    assert params
    assert params.key_id == "asdf"
    assert params.user_name is None
    assert params.user_email is None

    assert params.dict(by_alias=True) == {
        "KeyId": "asdf",
        "StoreId": "qwerty",
        "ExpectedCollectionUserEmail": None,
        "ExpectedCollectionUserName": None,
    }

    # response = call(store_id="qwerty")
    # assert response
    # assert response.id
    # assert response.name


def test_partial_dict_match():
    response = {
        "id": 123,
        "email": "user@email.com",
        "project": {"name": "Project One", "is_active": True},
    }

    expected = {
        "id": 123,
        "email": "user@email.com",
    }

    assert response.items() >= expected.items()
