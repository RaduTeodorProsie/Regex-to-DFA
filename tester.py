import json
import regex_to_dfa
from regex_lib import regex_postfix

with open("tests.json", "r") as tests:
    data = json.load(tests)

test_id = 0
for test in data:
    dfa = regex_to_dfa.regex_to_dfa(test["regex"])
    correct = True; print()
    print(test["regex"])
    for unit in test["test_strings"]:
        string, expected = unit["input"], unit["expected"]
        if dfa.accepts(string) != expected:
            print(f"{string}   eu: {dfa.accepts(string)}")
            correct = False
    test_id += 1
    if not correct:
        print(f"\033[91m❌ Test {test_id} wrong!\033[0m")
    else:
        print(f"\033[92m✅ Test {test_id} correct!\033[0m")



