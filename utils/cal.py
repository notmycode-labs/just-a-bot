import re

def dynamic_calc(expression):
    tokens = re.findall(r'\d+|\S', expression)
    numbers = [float(token) if token.isdigit() or '.' in token else token for token in tokens]
    result = numbers[0]
    current_operator = None

    for token in numbers[1:]:
        if isinstance(token, str):
            current_operator = token
        elif current_operator:
            if current_operator == '+':
                result += token
            elif current_operator == '-':
                result -= token
            elif current_operator == '*':
                result *= token
            elif current_operator == '/':
                if token != 0:
                    result /= token
                else:
                    return "Error: Division by zero"

    return result
