import argparse
import re


# resource: https://stackoverflow.com/a/47163546/2475919
def plate_with_numbers(plate):
    # Pattern which must plate match to be correct.
    # It says that your input must consist of
    #    two letters -> [a-zA-Z]{2}
    #    two numbers -> [0-9]{2}
    #    three letters -> [a-zA-Z]{3}
    # Number in {} says exactly how much occurrences of symbols in
    # in [] must be in string to have positive match.  
    # plate_format = re.compile('^[a-zA-Z]{2}[0-9]{2}[a-zA-z]{3}$')
    # Croatian plates
    plate_format = re.compile('^[a-zA-Z]{2}[0-9]{3,4}-[a-zA-z]{1,2}$')
    return True if plate_format.match(plate) is not None else False

def extract_numbers(plate):
    return re.search("[0-9]+", plate).group()


# resource: https://stackoverflow.com/a/73521378/2475919
def getCharPower(stringLength, charRange):
    charpowers = []
    for x in range(0, stringLength):
            charpowers.append(len(charRange)**(stringLength - x - 1))
    return charpowers

def Generator(stringLength, charRange):
    workbench = []
    results = []
    charpowers = getCharPower(stringLength, charRange)
    for x in range(0, stringLength):
            while len(workbench) < len(charRange)**stringLength:
                    for char in charRange:
                            for z in range(0, charpowers[x]):
                                    workbench.append(char)
            results.append(workbench)
            workbench = []
    results = ["".join(result) for result in list(zip(*results))]
    return results


def init_args():
    # Initializing Parser
    parser = argparse.ArgumentParser(description ="Dora's plate numbers game.")
    # Adding Argument
    parser.add_argument("plate_numbers",
                        metavar ='plate numbers',
                        type = str,
                        nargs ='+',
                        help ='Enter vehicle plate numbers separated with space')
    return parser.parse_args()


if __name__ == "__main__":
    argsv = init_args()
    plates = filter(plate_with_numbers, argsv.plate_numbers)
    for plate in plates:
        value = extract_numbers(plate).zfill(4)
        # commutative operations
        # FIXME: 1 value, one time generated!
        input = list(value)
        input.pop(-1)
        print(value, Generator(3, list(input)))
