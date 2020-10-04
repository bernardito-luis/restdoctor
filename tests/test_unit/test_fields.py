import datetime

import pytest
import pytz
from django.utils.timezone import make_aware

from restdoctor.rest_framework.fields import DateTimeField, ModelFromUUIDField
from tests.stubs.models import MyModel


@pytest.mark.parametrize(
    'datetime_obj, expected_string_representation',
    (
        (datetime.datetime(2020, 7, 16), '2020-07-16T00:00:00.000000+03:00'),
        (datetime.datetime(2020, 7, 16, tzinfo=pytz.utc), '2020-07-16T03:00:00.000000+03:00'),
        (make_aware(datetime.datetime(2020, 7, 16)), '2020-07-16T00:00:00.000000+03:00'),
        (make_aware(datetime.datetime(2020, 7, 16, 18, 0, 0)), '2020-07-16T18:00:00.000000+03:00'),
        (make_aware(datetime.datetime(2020, 7, 16, 18, 0, 0, 48)), '2020-07-16T18:00:00.000048+03:00'),
    ),
)
def test_datetime_field_to_representation(
    datetime_obj, expected_string_representation,
):
    assert DateTimeField().to_representation(datetime_obj) == expected_string_representation


@pytest.mark.django_db
def test_model_from_uuid_field_to_representation(
    my_model,
):
    queryset = MyModel.objects.all()

    assert ModelFromUUIDField(queryset=queryset).to_representation(my_model.uuid) == my_model
