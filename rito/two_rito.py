from referencing import Registry, Resource
from jsonschema.exceptions import ValidationError, RefResolutionError
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
        self.registry = Registry().with_resources(
            [
                ("http://hl7.org/fhir/json-schema/4.0", Resource.from_contents(self.schema))
            ],
        )

        self.validator = Draft6Validator(self.schema, registry=self.registry)
        self.fast_validator = fastjsonschema.compile(self.schema)

    @staticmethod
    def normalize_file_name(file_path: str) -> str:
        return re.split(r"/|\\", file_path)[-1]

    @staticmethod
    def validate_json(file: str) -> Union[dict, str]:
        json_resource = {}
        try:
            json_resource = json.loads(file)
        except json.JSONDecodeError as json_error:
            json_resource = str(json_error)
        except TypeError as type_error:
            json_resource = str(type_error)
        finally:
            return json_resource

    def file_validate(self, file_path: str, verbose: bool = False) -> dict:
        results = {}
        file = open(file_path).read()
        file_name = self.normalize_file_name(file_path)
        json_resource = self.validate_json(file)

        # if str, JSON is invalid, return json validation issues
        if isinstance(json_resource, str):
            results.update({file_name: json_resource})
        else:
            if verbose:
                results.update(self.verbose_validate(json_resource, file_name))
            else:
                results.update(self.fast_validate(json_resource, file_name))

        return results

    def dir_validate(self, directory_path: str, verbose: bool = False) -> dict:
        results = {}
        files = self.build_file_index(directory_path)

        for file in files:
            results.update(self.file_validate(file, verbose=verbose))

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

    def locate_sub_schema(self, json_resource: dict) -> list:
        schema_refs = self.schema.get('oneOf', [])
        schema_definitions = [ref['$ref'] for ref in schema_refs]
        schema_index = []

        if 'resourceType' in json_resource:
            ref = f"#/definitions/{json_resource['resourceType']}"
            print(f"calculated ref {ref}")
            if ref in schema_definitions:
                print(f"ref {ref} found in definitions")
                schema_index.append(schema_definitions.index(ref))

        return schema_index

    def fast_validate(self, json_resource: dict, file_name: str) -> dict:
        fast_results = {}

        # Fast validation passes silently, fails loudly
        try:
            self.fast_validator(json_resource)
            fast_results.update({file_name: True})
        except fastjsonschema.JsonSchemaException:
            fast_results.update({file_name: False})

        return fast_results

    @staticmethod
    def add_error_results(results: dict, identifier: str, error_type: str, error_msg: str) -> None:
        if identifier in results:
            results[identifier].update({error_type: error_msg})
        else:
            results.update({identifier: {error_type: error_msg}})

    def verbose_validate(self, json_resource: dict, identifier: str = '') -> dict:
        verbose_results = {}
        schema_index = self.locate_sub_schema(json_resource)

        if not identifier:
            identifier = f"{json_resource.get('resourceType', 'resourceType')}-{json_resource.get('identifier')}"

        if schema_index:
            # jsonschema validate returns noneType if valid, and raises ValidationError if invalid
            try:
                self.validator.check_schema(self.schema)
                self.validator.validate(json_resource)
                verbose_results.update({identifier: True})
            except ValidationError as error:
                for sub_error in error.context:
                    if sub_error.schema_path[0] == schema_index[0]:
                        error_type = sub_error.schema_path[-1]
                        self.add_error_results(verbose_results, identifier, error_type, sub_error.message)
        else:
            verbose_results.update({identifier: f"Unexpected resourceType: {json_resource['resourceType']}"})

        return verbose_results



