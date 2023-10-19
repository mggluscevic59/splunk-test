import argparse
import re
import operator
import math
import csv

# resource: https://stackoverflow.com/a/47163546/2475919
def plate_with_numbers(plate_case:str):
    # Pattern which must plate match to be correct.
    # It says that your input must consist of
    #    two letters -> [a-zA-Z]{2}
    #    two numbers -> [0-9]{2}
    #    three letters -> [a-zA-Z]{3}
    # Number in {} says exactly how much occurrences of symbols in
    # in [] must be in string to have positive match.
    plate_format = re.compile('[0-9]{4}|[0-9]{3}-[0-9]{1}')
    return plate_format.match(plate_case) is not None


def extract_numbers(full_plate:str):
    # returns a substring containing only numbers
    return "".join(re.findall("[0-9]+", full_plate))


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
    "/": operator.truediv,
    "^": operator.pow,
    "√": lambda b, a: operator.pow(a, 1/b)
} # etc.
singular_ops = {
    # HACK: on emtpy, return self
    " ": lambda x: x,
    "!": math.factorial,
    "-": operator.neg,
}



def combine_algorithm(values:list[int], operators:list[str]):
    if len(values) != 3 and len(operators) != 2:
        raise ValueError("Wrong number of inputs")
    for op_tuple in operators:
        first_op, second_op = list(op_tuple)
        try:
            # FIXME: operators hierarchy not valued!
            new_value = ops[first_op](values[0], values[1])
            final_value = ops[second_op](new_value, values[2])
        except ZeroDivisionError:
            # TODO: ignore edge cases
            continue
        yield final_value, op_tuple



def nice_solution_comment(_singular_op:str, _bi_op:str):
    arguments = ["(a", "b", "c"]
    singular_operators = list(_singular_op)
    binary_operators = list(_bi_op)
    # add singular operator
    for index, _ in enumerate(arguments):
        val = singular_operators[index]
        arguments[index] += "" if val == " " else val
        if index == 1:
            arguments[index] += ")"

    # add binary operator
    output = []
    for index, _ in enumerate(arguments):
        output.append(arguments[index])
        if index in [0, 1]:
            output.append(binary_operators.pop())

    return " ".join(output)



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


OPERATOR_COMBINATIONS = generate_combinations(2, ["+", "-", "*", "/"])
SINGULAR_COMBINATIONS = generate_combinations(3, [" ", "!", "-"])

def run_algorithms(plate_full):
    counter = 0
    first_text = ''
    value = extract_numbers(plate_full)
    if len(value) != 4:
        raise ValueError(f"plate number {value} not compatible with Dora's game!")
    input_values = list(turn_to_ints(list(value)))
    output_value = input_values.pop(-1)
    for new_values, singular_algorithm in combine_singular_algorithm(
        input_values,
        SINGULAR_COMBINATIONS
        ):
        for result, algorithm in combine_algorithm(new_values, OPERATOR_COMBINATIONS):
            if result == output_value:
                counter += 1
                if len(first_text) == 0:
                    first_text = nice_solution_comment(singular_algorithm, algorithm)
    return first_text, counter


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

    # data rows of csv file
    rows = []

    for plate in plates:
        flare, solution_counter = run_algorithms(plate)
        rows.append([plate, flare, solution_counter])

    # field names
    fields = ['plate_num', 'solution', 'total_num']

    with open("registration.csv", 'w', encoding="UTF-8") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
