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
    to_int = lambda listing: [int(x) for x in listing]
    summ = lambda x, y, z: x+y+z
    for plate in plates:
        value = extract_numbers(plate).zfill(4)
        input = to_int(list(value))
        output = input.pop(-1)
        if summ(*input) == output:
            print(plate, "plate is Dory's summation!")
