from typing import Union
import re

runningTotal = 0
run = True


def intro_message():
    print("Our Magical Calculator")
    print("Supported operations: ** + - * /")
    print("SPACES ARE NOT ALLOWED")
    print("Please use expressions such as 2*3 to get a result")
    print("To continue using the previous total you can simple do *2")
    print("to multiple the existing total by 2 for example")
    print("Type 'clear' to reset the calculator to 0")
    print("Type 'quit' to exit\n")


def parse_command(running_total: float, command: str) -> Union[None, list]:
    # This will hold the final command list
    command_list = []

    # First check to make sure only the allowed characters are present
    if re.match(r"[^0-9./*+\-]", command):
        return None

    # Then check that no operations or decimals are next to each other
    doubles = re.findall(r"[./*+\-]{2,}", command)
    for double in doubles:
        if double not in ["**-", "**", "*-", "/-", "+-", "--"]:
            return None

    # Now collect all operations in the order of their usage
    operations = re.findall(r"\*\*-|\*-|\+-|--|/-|\*\*|\*|/|\+|-", command)

    # Then replace all operations with a placeholder
    replaced_command = re.sub(r"\*\*-|\*-|\+-|--|/-|\*\*|\*|/|\+|-", "$", command)

    # Now split by the placeholder
    values = replaced_command.split("$")

    # Merge the operations list into the command_list
    for i in range(len(values)):
        if values[i] == '':
            command_list.append(running_total)
        else:
            command_list.append(values[i])

        if i < len(operations):
            command_list.append(operations[i])

    return command_list


def do_math(val1: float, operation: str, val2: float):
    if len(operation) > 1 and operation[-1:] == "-":
        operation = operation[:-1]
        val2 = -1 * val2

    if operation == '**':
        return val1 ** val2
    elif operation == '*':
        return val1 * val2
    elif operation == '/':
        return val1 / val2
    elif operation == '+':
        return val1 + val2
    elif operation == '-':
        return val1 - val2


def compute(algorithm: list) -> Union[None, float]:
    # Do operations in order
    for operation in ["**-", "**", "*-", "*", "/-", "/", "--", "-", "+-", "+"]:
        while operation in algorithm:
            # Get the location of the operator
            index = algorithm.index(operation)

            # Select the two numbers on either side with the operator
            operation_set = algorithm[index-1:index+2]

            # Do the calculation
            calculated_value = do_math(float(operation_set[0]), operation_set[1], float(operation_set[2]))

            # Now remove two of the elements and replace the last one with the new value
            del algorithm[index:index+2]
            algorithm[index-1] = calculated_value

    # The final remaining item is the answer, as index 0 of a single item list
    return float(algorithm[0])


'''
    The return of this function is formatted as RUNNINGTOTAL: float, ERROR: bool, RUN: true
'''


def process_command(running_total: float, command: str) -> tuple:
    if command == 'quit':
        return None, None, False
    elif command == 'help':
        intro_message()
        return None, None, True
    elif command == 'clear':
        return 0, None, True
    else:
        # Validate and turn command into a list
        parsed_command = parse_command(running_total, command)

        if parsed_command is None:  # If an error happened here
            return running_total, True, True

        # Attempt Calculation
        result = compute(parsed_command)

        if result is None:  # If an error happened here
            return running_total, True, True
        else:
            return result, False, True


# Starting Calculator


intro_message()

while run:
    statement = input("Total: " + str(runningTotal) + " :")
    runningTotal, error, run = process_command(runningTotal, statement)

    if error is True:
        print("The expression you used is not valid, please try again")
        print("Type 'help' to learn more about how this calculator works")
