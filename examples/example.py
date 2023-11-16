from rito import rito
import json
from datetime import datetime


# Here's a quick example of utilizing the validator and outputting the result to a txt file
def main():
    validator: rito.Validator = rito.Validator.r4()
    resource = open("../test/data/invalid_r4_patient.json", 'r').read()

    json_resource = json.loads(resource)
    output = validator.verbose_validate(json_resource, 'invalid_r4_patient')
    # output = validator.file_validate("../test/data/invalid_r4_patient.json", verbose=True)

    filename = "output" + datetime.now().strftime("%m%d-%H%M-%S") + ".txt"
    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
        file.close()


main()
