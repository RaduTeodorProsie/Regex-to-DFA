# Regex to DFA project
- This project contains 4 python modules:
  - `automat.py` : contains a finite automata class
  - `regex_lib.py` : used for handling regular expressions
  - `regex_to_dfa.py` : used for taking a regex and turns it to a dfa
  - `tester.py` : used for testing the automata converter on the tests in tests.json

## Automata class
- Has a basic constructor, as well as some interesting methods. The most important are :
  - `eliminate_epsilon()` : converts an epsilon-nfa to an nfa
  - `convert_to_dfa()` : converts an nfa (without epsilon transitions!) to a dfa by subset construction
- If you want epsilon transitions, you need to use the symbol "".
- If you want to check if the automata accepts a given string, you NEED to remove all epsilon transitions by calling the above method

## Regex lib
- The supported regex symbols are :
  
   **`*` (Kleene Star)**:
   - **Formal Name**: *Kleene Star* (or *Kleene Closure*)  
   - **Meaning**: Represents zero or more repetitions of the preceding expression. If `R` is a regex, then `R*` matches `ε` (empty string) or any number of `R` (like `RR...`).

   **`+` (Kleene Plus)**:
   - **Formal Name**: *Kleene Plus*  
   - **Meaning**: Represents one or more repetitions of the preceding expression. It's similar to `*` but must match at least one occurrence of the expression. `R+` is equivalent to `RR*`.

   **`.` (Concatenation)**:
   - **Formal Name**: *Concatenation* (or *Sequencing*)  
   - **Meaning**: Represents the sequential combination of two regular expressions. For example, `ab` means "match `a` followed by `b`". Concatenation is often implicit in regex and doesn't require a symbol in some regex              engines, but is often represented by `.` in formal descriptions.

   **`|` (Alternation)**:
   - **Formal Name**: *Alternation* (or *Union*)  
   - **Meaning**: Represents a choice between two expressions. For example, `a|b` means "match `a` or `b`". It's equivalent to set union in formal language theory.

   **`?` (Optional)**:
   - **Formal Name**: *Optionality* (or *Zero or One*)  
   - **Meaning**: Represents zero or one occurrence of the preceding expression. `R?` means "match `R` once or not at all". This is equivalent to the union of `ε` and `R` (i.e., `ε ∪ R`).

- Functions inside the lib :
  - insert_concatenation_operator() : inserts `.` between ALL subexpressions. This makes the regex manageble by the postfix function.
  - regex_postfix : writes the transformed regex into postfix notation. For example, `(ab?)*` becomes `(a.b?)*` by calling the above function, and then becomes `a b ? . *` in postfix notation.

## Regex_to_dfa.py
This module has a single function, regex_to_dfa(). It uses a modified version of thompson's algorithm, 
however I handle the compounding of NFAs a little differently: As usual, we keep a stack of NFAs and
traverse the regex in postfix order. When we encounter :
  - A symbol : I push the NFA that only accepts that symbol onto the stack
  - `?` : I put epsilon transitions from the starting state of the NFA on top of the stack to all its final states.
  - `+` : I put epsilon transitions from the ending states of the NFA on top of the stack to its starting state
  - `*` : Do the operations for `+` and `?`
  - `.` : Let A and B be the NFAs second from the top and topmost respectively. I add an epsilon transition from the final states of A to the starting state of B, and then I unmark A's final states as final.
  - `|` : Create a new start state. Put epsilon transitions from it to the starting states of A and B. 

Because of the way we modified the expression, at the end there will be a single element on the stack. That is the final NFA. After that, we call the methods inside of the AF object to convert it to a DFA.
## Prerequisites

- Python 3.x
- git version control

## Installation and running

1. Clone the repository:
   
   ```bash
   git clone https://github.com/RaduTeodorProsie/Regex-to-DFA
   ```

2. Use it however you want! For example, you can run the tester:
   ```bash
   python3 tester.py
   ```
   
## License

This project is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to use, modify, and redistribute it—even commercially—**as long as proper credit is given**(a github link would be great!).

   
   
