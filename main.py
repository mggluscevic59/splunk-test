import argparse
import re
import operator
import math

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


def turn_to_ints(value_holder:list[str]):
    # simple function accepts list of strings, returns list of integers
    for number in value_holder:
        yield int(number)


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


# TODO: single operand operators
# resource: https://stackoverflow.com/a/1740759/2475919
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
} # etc.
singular_ops = {
    "!": math.factorial,
    "^": lambda x: math.pow(x, 2),
    "√": math.sqrt,
}



def combine_algorithm(values:list[int], operators:list[str]):
    if len(values) != 3 and len(operators) != 2:
        raise ValueError("Wrong number of inputs")
    for op_tuple in operators:
        first_op, second_op = list(op_tuple)
        try:
            new_value = ops[first_op](values[0], values[1])
            final_value = ops[second_op](new_value, values[2])
        except ZeroDivisionError:
            # TODO: re-raise error
            continue
        yield final_value, op_tuple


# def combine_singular(number:int, singular_operator:str):
#     return singular_ops[singular_operator](number)



def combine_singular_algorithm(values:list[int], operators:list[str]) -> list[int]:
    if len(values) != 3 and len(operators) != 3:
        raise ValueError("Wrong number of inputs")

    for op_triple in operators:
        new_val = []
        for index, val in enumerate(values):
            operation = op_triple[index]
            # yield singular_ops[operation](val)

            new_val.append(singular_ops[operation](val))
        yield new_val, op_triple



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
    operator_combination = generate_combinations(2, ["+", "-", "*", "/"])
    singular_operator_combination = generate_combinations(3, ["!", "^", "√"])
    for plate in plates:
        value = extract_numbers(plate).zfill(4)
        input_values = list(turn_to_ints(list(value)))
        output_value = input_values.pop(-1)
        for result, algorithm in combine_algorithm(input_values, operator_combination):
            if result == output_value:
                if algorithm == "++":
                    print(plate, "plate is Dory's summation!")
                elif algorithm == "--":
                    print(plate, "plate is Dory's negation!")
                elif algorithm == "**":
                    print(plate, "plate is Dory's multiplication!")
                else:
                    print(plate, "plate is in Dory's algorithms! Combination: ", algorithm)
                # FIXME: if only first value accepted, uncomment next line
                # break

        for new_values, singular_algorithm in combine_singular_algorithm(input_values, singular_operator_combination):
            for result, algorithm in combine_algorithm(new_values, operator_combination):
                if result == output_value:
                    if singular_algorithm == "!!!":
                        print(plate, "plate is in Dory's factoriel algorithm!")
                    elif singular_algorithm == "^^^":
                        print(plate, "plate is in Dory's square algorithm!")
                    elif singular_algorithm == "√√√":
                        print(plate, "plate is in Dory's root algorithm!")
                    else:
                        print(plate, "plate is in Dory's algorithms! Combination: ", algorithm, singular_algorithm)
