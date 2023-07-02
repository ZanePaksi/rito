from pathlib import Path
from rito import rito
import logging
import pytest
import os


LOGGER = logging.getLogger(__name__)
TEST_VALIDATORS = [rito.Validator.r5(), rito.Validator.r4(), rito.Validator.stu3()]
TEST_RESOURCES = ['patient', 'organization', 'observation']
RESOURCE_PATH = os.path.join(os.path.dirname(__file__), Path('resources'))


@pytest.fixture(name='resource', scope='module', params=TEST_RESOURCES)
def fixture_resource(request):
    return request.param


@pytest.fixture(name='validator', scope='module', params=TEST_VALIDATORS)
def fixture_validator(request):
    return request.param


def test_single_resource_valid(validator, resource):
    fhir_version = validator.get_fhir_version()
    resource_name = f'{fhir_version}_{resource}.json'
    LOGGER.info(f'Validator Version :: {fhir_version}')
    LOGGER.info(f'Resource File :: {resource_name}')

    result = validator.fhir_validate(RESOURCE_PATH + f'\\{resource_name}')
    assert result[resource_name] is True
