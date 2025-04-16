import automat
import regex_lib


def regex_to_dfa(regex):
    stack, created = [], 0
    alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ''}

    regex = regex_lib.regex_postfix(regex)
    for sym in regex:
        if sym.isalnum():
            stack.append(automat.AF({created, created + 1}, alphabet, {(created, sym) : [created + 1]}, created, {created + 1}))
            created += 2
        elif sym == "?":
            for finale in stack[-1].final_states:
                stack[-1].add_transition(((stack[-1].start_state, ""), finale))
        elif sym == ".":
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif sym == "*":
            for finale in stack[-1].final_states:
                stack[-1].add_transition(((stack[-1].start_state, ""), finale))
                stack[-1].add_transition(((finale, ""), stack[-1].start_state))
        elif sym == "+":
            for finale in stack[-1].final_states:
                stack[-1].add_transition(((finale, ""), stack[-1].start_state))

        elif sym == "|":
            b, a = stack.pop(), stack.pop()
            transitions = a.transitions
            transitions.update(b.transitions)
            transitions[(created, "")] = [a.start_state, b.start_state]
            stack.append(automat.AF(a.states | b.states | {created}, a.alphabet | b.alphabet, transitions, created, a.final_states | b.final_states))
            created += 1

    #print(stack[0])
    stack[0].eliminate_epsilon()
    #print(stack[0])
    stack[0].convert_to_dfa()
    #print(stack[0])
    return stack[0]



