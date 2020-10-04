from __future__ import annotations
import datetime
from typing import Optional, Union, Any, TYPE_CHECKING

from django.db import models
from rest_framework import ISO_8601
from rest_framework.fields import DateTimeField as BaseDateTimeField, UUIDField
from rest_framework.relations import HyperlinkedIdentityField as BaseHyperlinkedIdentityField
from rest_framework.request import Request
from rest_framework.settings import api_settings

from restdoctor.rest_framework.reverse import preserve_resource_params

if TYPE_CHECKING:
    import uuid
    from django.db.models import Model, QuerySet


class DateTimeField(BaseDateTimeField):
    def to_representation(
        self, value: datetime.datetime,
    ) -> Union[Optional[str], datetime.datetime]:
        if not value:
            return None

        output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

        if output_format is None or isinstance(value, str):
            return value

        value = self.enforce_timezone(value)

        if output_format.lower() == ISO_8601:
            value = value.isoformat(timespec='microseconds')
            return value
        return value.strftime(output_format)


class HyperlinkedIdentityField(BaseHyperlinkedIdentityField):
    def get_url(self, obj: models.Model, view_name: str, request: Request, *args: Any, **kwargs: Any) -> str:
        url = super().get_url(obj, view_name, request, *args, **kwargs)
        return preserve_resource_params(url, request)


class ModelFromUUIDField(UUIDField):
    def __init__(self, queryset: QuerySet, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.queryset = queryset

    def to_representation(self, uuid: uuid.UUID) -> Optional[Model]:
        return self.queryset.filter(uuid=uuid).first()
