import json
from datetime import date, datetime, timezone
from typing import Optional

import pytest
from pydantic import BaseModel, Field, ValidationError


class KeynestStore(BaseModel):
    id: int = Field(..., alias="StoreId")
    name: str = Field(..., alias="StoreName")
    description: Optional[str] = Field(None, alias="StoreDescription")
    lat: float = Field(..., alias="Latitude")
    lng: float = Field(..., alias="Longtiude")  # A typo is intentional ;)
    created_at: datetime = Field(..., alias="CreatedAt")


def test_parse_json():
    data = json.dumps(
        {
            "StoreId": 123,
            "StoreName": "Tesco",
            "StoreDescription": None,
            "Latitude": "50.123",
            "Longtiude": "-0.123",
            "CreatedAt": "2021-02-01T18:09:00Z",
        }
    )

    store = KeynestStore.parse_raw(data)

    assert store
    assert store.id == 123
    assert store.name == "Tesco"
    assert store.lat == 50.123
    assert store.lng == -0.123
    assert store.created_at == datetime(2021, 2, 1, 18, 9, tzinfo=timezone.utc)

    def default(o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()

    assert (
        json.dumps(store.dict(by_alias=True), default=default)
        == '{"StoreId": 123, "StoreName": "Tesco", "StoreDescription": null, "Latitude": 50.123, "Longtiude": -0.123, "CreatedAt": "2021-02-01T18:09:00+00:00"}'  # noqa: E501
    )


def test_parse_json_with_missing_optional_fields():
    data = json.dumps(
        {
            "StoreId": 123,
            "StoreName": "Tesco",
            "Latitude": "50.123",
            "Longtiude": "-0.123",
        }
    )

    store = KeynestStore.parse_raw(data)

    assert store.description is None


def test_parse_raw_should_raise_validation_error():
    data = json.dumps(
        {
            # "StoreId": 123,
            "StoreName": "Tesco",
            "Latitude": "50.123",
            "Longtiude": "-0.123",
        }
    )

    with pytest.raises(ValidationError):
        KeynestStore.parse_raw(data)
