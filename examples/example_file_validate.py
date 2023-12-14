from datetime import datetime
from rito import rito
import json


# Here's a quick example of utilizing file_validate and outputting the result to a txt file
def main():
    validator: rito.Validator = rito.Validator.r4()

    output = validator.file_validate("../test/data/r4/graph_definition.json", verbose=True)

    filename = "output" + datetime.now().strftime("%m%d-%H%M-%S") + ".txt"
    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
        file.close()


main()
