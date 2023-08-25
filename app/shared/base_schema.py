from pydantic import BaseModel, ConfigDict

from app.shared.str_utils import camelize


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=camelize,
        populate_by_name=True,
    )
