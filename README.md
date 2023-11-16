# Rito - FHIR Validator

[![Pythons](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-3810/)
![example workflow](https://github.com/ZanePaksi/rito/actions/workflows/flake8.yml/badge.svg)
![example workflow](https://github.com/ZanePaksi/rito/actions/workflows/pytest.yml/badge.svg)

---

## Limitations
Rito utilizes JSON Schemas provided by HL7.

A main caveat with this validation method is that *Rito is not connected to a terminology server*.
This means that codeable concept 'system' URIs are not checked if they resolve. The degree of validation
varies, but some FHIR servers will not accept unresolvable system URIs.

This could result in Rito returning valid results in regard to syntax, but the resource not being 
accepted by a FHIR server.

For further details please see:
[FHIR Validation Info](https://www.hl7.org/fhir/validation.html)

---

## Setup

Until I release this package on PyPI, here are some options for installing this library:

Direct installation using pip and git repo url  
```pip install git+https://github.com/{username}/rito.git```

Or

Clone the repo, and then install with pip in project root
```
git clone https://github.com/{username}/rito.git
cd path/to/rito
pip install .
```  

After installation I recommend running both pytest and flake8 to ensure everything is working correctly
```
# cmd in project root
pytest

# finally
flake8
```

---

## Examples
Always begin by importing rito  
`from rito import rito`

Validate a single file:  
```
validator = rito.Validator.r4()

output = validator.file_validate("../test/data/invalid_r4_patient.json", verbose=True)
print(output)

Output:
{
    "invalid_r4_patient.json": {
        "enum": "'males' is not one of ['male', 'female', 'other', 'unknown']",
        "additionalProperties": "Additional properties are not allowed ('activ' was unexpected)"
    }
}
```

Validating a whole directory (all files valid):
```
validator = rito.Validator.r4b()

# Directory validate, without verbose validation - values will only be boolean
output = validator.dir_validate("../test/data/r4b")
print(output)

Output:
{
    "observation.json": true,
    "organization.json": true,
    "patient.json": true
}
```

Directly invoke fast validation
```
validator = rito.Validator.r5()

resource = open("../test/data/r5/patient.json", 'r').read()
json_resource = json.loads(resource)

output = validator.fast_validate(json_resource, 'r5_patient')
print(output)

Output:
{
    "r5_patient": true
}
```

Directly invoke verbose validation
```
validator = rito.Validator.r4()

resource = open("../test/data/invalid_r4_patient.json", 'r').read()
json_resource = json.loads(resource)

output= validator.verbose_validate(json_resource, 'invalid_r4_patient')
print(output)

Output:
{
    "invalid_r4_patient": {
        "enum": "'males' is not one of ['male', 'female', 'other', 'unknown']",
        "additionalProperties": "Additional properties are not allowed ('activ' was unexpected)"
    }
}
```

---

## Built With

* [Python3](https://www.python.org/)
* [fastjsonschema](https://pypi.org/project/fastjsonschema/) - Validation framework
* [jsonschema](https://pypi.org/project/jsonschema/) - Validation framework
* [HL7 FHIR Specs](http://hl7.org/fhir/directory.html) - Documentation and schemas
