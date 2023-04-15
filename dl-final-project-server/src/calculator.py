from abc import ABC
from numpy import double
from abc import ABC,abstractmethod

class Expression(ABC):
    @abstractmethod
    def calc(self)->double:
        pass


class Num(Expression):
    def __init__(self, x) -> None:
        self.__x = x
    def calc(self) -> double:
        return self.__x


class BinExp(Expression):
    def __init__(self, right, left) -> None:
        self.__right = right
        self.__left = left
    def calc(self) -> double:
        pass


class Plus(BinExp):
    def __init__(self, right, left) -> None:
        self.__right = right
        self.__left = left
    def calc(self) -> double:
        return self.__right.calc() + self.__left.calc()


class Minus(BinExp):
    def __init__(self, right, left) -> None:
        self.__right = right
        self.__left = left
    def calc(self) -> double:
        return  self.__right.calc() - self.__left.calc()


class Mul(BinExp):
    def __init__(self, right, left) -> None:
        self.__right = right
        self.__left = left
    def calc(self) -> double:
        return  self.__right.calc() * self.__left.calc()


class Div(BinExp):
    def __init__(self, right, left) -> None:
        self.__right = right
        self.__left = left
    def calc(self) -> double:
        return  self.__right.calc() / self.__left.calc()


def parser(expression)->double:
    expression = expression.replace(" ", "")
    expression = expression.split("=")[0]
    stack = []
    queue = []
    current_token = ""
    prev_token = ""
    for c in expression:
        if (c.isnumeric()):
            current_token += c
        elif (current_token != ""):
            queue.append(current_token)
            current_token = ""
        if (c == '-' and prev_token == "("):
            current_token = "-"
        elif (c == '*' or c == 'x' or c == '/' or c == ":"):
            stack.append(c)
        elif (c == '+' or c == '-'):
            while (stack and (stack[-1] == '*' or stack[-1] == 'x' or stack[-1] == '/' or stack[-1] == ':')):
                queue.append(stack.pop())
            if (stack and (stack[-1] == '+' or stack[-1] == '-')):
                queue.append(stack.pop())
            stack.append(c)
        if (c == '('):
            stack.append(c)
        if (c == ')'):
            while (stack[-1] != '('):
                queue.append(stack.pop())
            stack.pop()
        prev_token = c
    if current_token:
        queue.append(current_token)
    while (stack and (stack[-1] == '*' or stack[-1] == 'x' or stack[-1] == '/' or stack[-1] == ':' or stack[-1] == '+' or stack[-1] == '-')):
        queue.append(stack.pop())
    return evaluate_postfix(queue)


def evaluate_postfix(postfix_expr):
    stack = []
    for token in postfix_expr:
        if token.lstrip('-').isdigit():
            stack.append(Num(int(token)))
        else:
            opL = stack.pop()
            opR = stack.pop()
            result = 0
            if token == '+':
                result = Plus(opR, opL).calc()
            elif token == '-':
                result = Minus(opR, opL).calc()
            elif token == '*' or token == 'x':
                result = Mul(opR, opL).calc()
            elif token == '/' or token == ":":
                result = Div(opR, opL).calc()
            stack.append(Num(int(result)))
    return stack.pop().calc()