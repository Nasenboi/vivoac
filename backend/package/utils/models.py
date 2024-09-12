"""########################################################################################
Name: utils/models.py
Description: This file contains useful functions that are used throughout the project.
Imports:
"""

from typing import Optional

from pydantic import BaseModel, model_validator, Field, ConfigDict

from datetime import datetime

"""
########################################################################################"""

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class CreatedUpdatedAt:
    """Created and updated at mixin that automatically updates updated_at field.
        Thanks to: martintrapp [https://stackoverflow.com/questions/73128975/pydantic-created-at-and-updated-at-fields]
    """    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        validate_assignment=True,
    )

    @model_validator(mode="after")
    @classmethod
    def update_updated_at(cls, obj: "CreatedUpdatedAt") -> "CreatedUpdatedAt":
        """Update updated_at field."""
        # must disable validation to avoid infinite loop
        obj.model_config["validate_assignment"] = False

        # update updated_at field
        obj.updated_at = datetime.now()

        # enable validation again
        obj.model_config["validate_assignment"] = True
        return obj