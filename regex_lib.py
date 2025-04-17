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

        # — NEW — Add . between postfix operators and '(' (e.g., a*( -> a*.()
        if i + 1 < n and regex[i] in "*+?" and regex[i + 1] == '(':
            result.append('.')

    return ''.join(result)


def regex_postfix(expression, precedence=None):
    if precedence is None:
        precedence = {
            '?': 4,
            '*': 3,
            '+': 3,   # you can bump '+' to the same level as '*'
            '.': 1,
            '|': 0,
            '(': -1
        }

    expression = insert_concatenation_operator(expression)
    output, stack = [], []
    for sym in expression:
        if sym.isalnum():
            output.append(sym)
        else:
            if sym == '(':
                stack.append(sym)
            elif sym == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # discard '('
            else:
                # pop higher‑precedence operators first
                while stack and precedence[stack[-1]] >= precedence[sym]:
                    output.append(stack.pop())
                stack.append(sym)

    while stack:
        output.append(stack.pop())

    return output
