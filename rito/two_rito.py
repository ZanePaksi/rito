from jsonschema import Draft6Validator
from pathlib import Path
import fastjsonschema
import json
import os
import glob
import re
from typing import Union


class Validator:

    SUPPORTED_VERSIONS = [
        'r5', 'r4', 'stu3'
    ]

    def __init__(self, schema_version: str) -> None:
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema_version = schema_version

        if schema_version in Validator.SUPPORTED_VERSIONS:
            self.schema_name = self.base + f'/fhir.{schema_version}.schema.json'
        else:
            raise LookupError(f'Unsupported schema version: {schema_version}')

        self.schema = json.loads(open(self.schema_name, encoding="utf8").read())

        self.validator = Draft6Validator(self.schema)
        self.fast_validator = fastjsonschema.compile(self.schema)

    @staticmethod
    def normalize_file_name(file_path: str) -> str:
        return re.split(r"/\\", file_path)[-1]

    @staticmethod
    def validate_json(file: str) -> Union[dict, str]:
        json_resource: Union[dict, str] = {}
        try:
            json_resource = json.loads(file)
        except json.JSONDecodeError as json_error:
            json_resource = str(json_error)
        except TypeError as type_error:
            json_resource = str(type_error)
        finally:
            return json_resource

    def file_validate(self, file_path: str) -> dict:
        results = {}
        file = open(file_path, encoding="utf8").read()
        file_name = self.normalize_file_name(file_path)
        json_resource = self.validate_json(file)

        # if str, JSON is invalid, return json validation issues
        if isinstance(json_resource, str):
            results.update({file_name: json_resource})
        else:
            results.update(self.fast_validate(json_resource, file_name))

        return results

    def dir_validate(self, directory_path: str) -> dict:
        results = {}
        files = self.build_file_index(directory_path)

        for file in files:
            results.update(self.file_validate(file))

        return results

    @staticmethod
    def build_file_index(directory_path: str) -> list:
        files_in_dir = []

        if Path.is_dir(Path(directory_path)):
            for file in glob.iglob(directory_path + "**/*.json", recursive=True):
                files_in_dir.append(file)
        else:
            raise LookupError("The path provided is not a directory")

        return files_in_dir

    def fast_validate(self, json_resource: dict, file_name: str) -> dict:
        results = {}

        # Fast validation passes silently, fails loudly
        try:
            self.fast_validator(json_resource)
            results.update({file_name: True})
        except fastjsonschema.JsonSchemaException:
            results.update({file_name: False})

        return results

    def verbose_validate(self, resource: dict):
        results = {}
        schema_refs = self.schema.get('oneOf', [])
        schema_definitions = [ref['$ref'] for ref in schema_refs]
        if 'resourceType' in resource:
            ref = f"#/definitions/{resource['resourceType']}"
            if ref in schema_definitions:
                schema_index = schema_definitions.index(ref)


