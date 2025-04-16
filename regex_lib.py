def insert_concatenation_operator(regex):
    result = []
    n = len(regex)

    for i in range(n):
        result.append(regex[i])

        # Add . between two literals (e.g., ab -> a.b)
        if i + 1 < n and regex[i].isalnum() and regex[i + 1].isalnum():
            result.append('.')

        # Add . between a literal and ( (e.g., a( -> a.()
        if i + 1 < n and regex[i].isalnum() and regex[i + 1] == '(':
            result.append('.')

        # Add . between ) and a literal (e.g., )a -> ).a)
        if i + 1 < n and regex[i] == ')' and regex[i + 1].isalnum():
            result.append('.')

        # Add . between ) and ( (e.g., )( -> ).()
        if i + 1 < n and regex[i] == ')' and regex[i + 1] == '(':
            result.append('.')

        # Add . between postfix operators (*, +, ?) and literals (e.g., a*b -> a*.b)
        if i + 1 < n and regex[i] in "*+?" and regex[i + 1].isalnum():
            result.append('.')

    return ''.join(result)

def regex_postfix(expression, precedence=None):
    if precedence is None:
        precedence = {
            '?': 4,
            '*': 3,
            '+': 2,
            '.': 1,
            '|': 0,
            '(': -69
        }


    expression = insert_concatenation_operator(expression)
    output, stack = [], []
    for sym in expression:
        if sym.isalnum():
            output.append(sym)
        else:
            if sym == '(':
                stack.append('(')
            elif sym == ')':
                while len(stack) != 0 and stack[-1] != '(':
                    output.append(stack.pop())
                if len(stack) == 0:
                    raise RuntimeError("Invalid regex")
                stack.pop()
            else:
                while len(stack) != 0 and precedence[stack[-1]] > precedence[sym]:
                    output.append(stack.pop())
                stack.append(sym)
    while len(stack) != 0:
        output.append(stack.pop())
    return output
