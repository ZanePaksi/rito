from pathlib import Path
from rito import rito
import logging
import pytest
import os

LOGGER = logging.getLogger(__name__)

TEST_DATA_PATH = os.path.join(Path(__file__).resolve().parent, Path('data'))

TEST_VALIDATORS = {
    'r3': rito.Validator.r3(),
    'r4': rito.Validator.r4(),
    'r4b': rito.Validator.r4b(),
    'r5': rito.Validator.r5()
}


def test_r3_file_validate_encounter():
    validator = TEST_VALIDATORS['r3']
    file_path = TEST_DATA_PATH + f'/{validator.fhir_version}/invalid/encounter.json'
    result = validator.file_validate(file_path)

    assert result == {
    "encounter.json": {
        "enum": "'complete' is not one of ['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown']",
        "additionalProperties": "Additional properties are not allowed ('subjec' was unexpected)"
    }
}


def test_r3_file_validate_medication():
    validator = TEST_VALIDATORS['r3']
    file_path = TEST_DATA_PATH + f'/{validator.fhir_version}/invalid/medication.json'
    result = validator.file_validate(file_path)


def test_r3_file_validate_procedure():
    validator = TEST_VALIDATORS['r3']
    file_path = TEST_DATA_PATH + f'/{validator.fhir_version}/invalid/procedure.json'
    result = validator.file_validate(file_path)


def test_r4_invalid_file_validate():
    validator = TEST_VALIDATORS['r4']


def test_r4b_invalid_file_validate():
    validator = TEST_VALIDATORS['r4b']


def test_r5_invalid_file_validate():
    validator = TEST_VALIDATORS['r5']

