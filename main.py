import argparse
import re
import operator

# resource: https://stackoverflow.com/a/47163546/2475919
def plate_with_numbers(plate_case:str):
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
    return plate_format.match(plate_case) is not None


def extract_numbers(full_plate:str):
    # returns a substring containing only numbers
    return re.search("[0-9]+", full_plate).group()


# resource: https://stackoverflow.com/a/73521378/2475919
def get_char_power(string_lenght, char_range):
    charpowers = []
    for x in range(0, string_lenght):
        charpowers.append(len(char_range)**(string_lenght - x - 1))
    return charpowers

def generate_combinations(string_lenght, char_range):
    workbench = []
    results = []
    charpowers = get_char_power(string_lenght, char_range)
    for x in range(0, string_lenght):
        while len(workbench) < len(char_range)**string_lenght:
            for char in char_range:
                for _ in range(0, charpowers[x]):
                    workbench.append(char)
        results.append(workbench)
        workbench = []
    results = ["".join(result) for result in list(zip(*results))]
    return results

# resource: https://stackoverflow.com/a/1740759/2475919
ops = { "+": operator.add, "-": operator.sub } # etc.



def combine_algorithm(values:list[int], operators:list[str]):
    if len(values) != 3 and len(operators) != 2:
        raise ValueError("Wrong number of inputs")
    for op_tuple in operators:
        first_op, second_op = list(op_tuple)
        new_value = ops[first_op](values[0], values[1])
        yield ops[second_op](new_value, values[2]), op_tuple


# source: https://stackoverflow.com/a/42619122/2475919
def compare_operators_used(input_operators:list[str], ethalon:list[str]):
    a = input_operators
    b = ethalon
    return (set(b) == set(a)  & set(b) and set(a) == set(a) & set(b))


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
    # summ = lambda x, y, z: x+y+z
    operator_combination = generate_combinations(2, ["+", "-"])
    for plate in plates:
        value = extract_numbers(plate).zfill(4)
        input_values = to_int(list(value))
        output_value = input_values.pop(-1)
        for result, algorithm in combine_algorithm(input_values, operator_combination):
            if result == output_value:
                if compare_operators_used(algorithm, ["+", "+"]):
                    print(plate, "plate is Dory's summation!")
                elif compare_operators_used(algorithm, ["-", "-"]):
                    print(plate, "plate is Dory's negation!")
                else:
                    print(plate, "plate is Dory's algorithm!")
                break
