from numpy import double
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass


# implement the classes here
class Num(Expression):
    def __init__(self, num) -> None:
        # private instance attributes
        self.num = num

    def calc(self) -> double:
        return self.num


class BinExp(Expression, ABC):
    def __init__(self, left_expression, right_expression) -> None:
        # protected instance attributes
        self.right_expression = right_expression
        self.left_expression = left_expression


class Plus(BinExp):
    def __init__(self, right_expression, left_expression) -> None:
        super().__init__(right_expression, left_expression)

    def calc(self) -> double:
        return self.left_expression.calc() + self.right_expression.calc()


class Minus(BinExp):
    def __init__(self, right_expression, left_expression) -> None:
        super().__init__(right_expression, left_expression)

    def calc(self) -> double:
        return self.left_expression.calc() - self.right_expression.calc()


class Mul(BinExp):
    def __init__(self, right_expression, left_expression) -> None:
        super().__init__(right_expression, left_expression)

    def calc(self) -> double:
        return self.left_expression.calc() * self.right_expression.calc()


class Div(BinExp):
    def __init__(self, right_expression, left_expression) -> None:
        super().__init__(right_expression, left_expression)

    def calc(self) -> double:
        return self.left_expression.calc() / self.right_expression.calc()


def parser_equation(expression):
    if "=" in expression:
        side_index = expression.index("=")
        return parser(expression[:side_index]) == parser(expression[side_index + 1:])
    elif ">" in expression:
        side_index = expression.index(">")
        return parser(expression[:side_index]) > parser(expression[side_index + 1:])
    elif "<" in expression:
        side_index = expression.index("<")
        return parser(expression[:side_index]) < parser(expression[side_index + 1:])
    else:
        return parser(expression)


def parser(expression) -> double:
    formatted_expression = simplify_brackets(expression)

    expression_array = equation_to_array(formatted_expression)

    sign_dict = {'*': Mul,
                 'X': Mul,
                 ':': Div,
                 '/': Div}
    expression_array = calculate_sign(expression_array, sign_dict)

    sign_dict = {'+': Plus,
                 '-': Minus}
    expression_array = calculate_sign(expression_array, sign_dict)

    return expression_array[0].calc()


def calculate_sign(expression_array, sign_dict) -> list:
    key_count = 0
    for key in sign_dict.keys():
        key_count += expression_array.count(key)
    while key_count:
        index = len(expression_array)
        for key in sign_dict.keys():
            if expression_array.count(key) > 0:
                curr_index = expression_array.index(key)
                if curr_index < index:
                    index = curr_index

        expression_array[index - 1:index + 2] = [sign_dict[expression_array[index]](expression_array[index - 1],
                                                                                    expression_array[index + 1])]
        key_count -= 1

    return expression_array


def equation_to_array(formatted_expression) -> list:
    expression_array = []
    index = 0
    num = Num(0)
    while len(formatted_expression) > index:
        if formatted_expression[index].isdigit() or \
                (formatted_expression[index] in "+-" and not (
                        index != 0 and formatted_expression[index - 1].isdigit())):
            seperator_index = index + 1
            while len(formatted_expression) > seperator_index and formatted_expression[seperator_index] not in '-+*/)':
                seperator_index = seperator_index + 1
            num = Num(double(formatted_expression[index:seperator_index]))
            index = seperator_index
        else:
            expression_array.append(num)
            num = Num(0)
            expression_array.append(formatted_expression[index])
            index = index + 1
    expression_array.append(num)
    return expression_array


def simplify_brackets(expression) -> str:
    formatted_expression = expression
    index = formatted_expression.find("(")
    while index != -1:
        closer_index = formatted_expression.find(")", index + 1)
        next_index = formatted_expression.find("(", index + 1)
        temp_index = index
        next_temp_index = next_index
        while next_temp_index != -1 and next_temp_index < closer_index:
            temp_index = next_temp_index
            next_temp_index = formatted_expression.find("(", next_temp_index + 1)

        formatted_expression = formatted_expression.replace(formatted_expression[temp_index:closer_index + 1],
                                                            str(parser(
                                                                formatted_expression[temp_index + 1:closer_index])))
        index = formatted_expression.find("(")
    return formatted_expression
