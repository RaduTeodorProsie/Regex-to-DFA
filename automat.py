class AF:
    def __init__(self, q, e, d, q0, f):
        self.states = q
        self.alphabet = e
        self.transitions = d
        self.start_state = q0
        self.final_states = f

    def __str__(self):
        return (
            f"AF(\n"
            f"  States: {self.states}\n"
            f"  Transitions: {self.transitions}\n"
            f"  Start State: {self.start_state}\n"
            f"  Final States: {self.final_states}\n"
            f")"
        )

    def __add__(self, other):
        transitions = self.transitions
        transitions.update(other.transitions)
        for finale in self.final_states:
            transitions[(finale, "")] = transitions.get((finale, ""), []) + [other.start_state]
        return AF(self.states | other.states, self.alphabet | other.alphabet, transitions, self.start_state, other.final_states)

    def add_transition(self, transition):
        if transition[0] not in self.transitions.keys():
            self.transitions[transition[0]] = []
        self.transitions[transition[0]].append(transition[1])

    def epsilon_closure(self, state):
        closure = {state}
        states_to_process = [state]
        while states_to_process:
            current_state = states_to_process.pop()
            for next_state in self.transitions.get((current_state, ''), []):
                if next_state not in closure:
                    closure.add(next_state)
                    states_to_process.append(next_state)
        return closure

    def eliminate_epsilon(self):

        epsilon_closures = {state: self.epsilon_closure(state) for state in self.states}
        new_transitions = {}

        for state in self.states:
            for symbol in self.alphabet:
                if symbol != '':
                    new_states = set()
                    for s in epsilon_closures[state]:
                        next_states = self.transitions.get((s, symbol), [])
                        for next_state in next_states:
                            new_states.update(epsilon_closures[next_state])
                    if new_states:
                        new_transitions[(state, symbol)] = list(new_states)

        new_final_states = set()
        for state in self.states:
            if self.final_states.intersection(epsilon_closures[state]):
                new_final_states.add(state)

        self.transitions = {key: value for key, value in new_transitions.items() if key[1] != ''}
        self.final_states = new_final_states

    def convert_to_dfa(self):
        from collections import deque

        states = set()
        alphabet = self.alphabet
        transitions = dict()
        start_state = frozenset({self.start_state})
        final_states = set()
        queue = deque([start_state])

        while queue:
            state = queue.popleft()
            if state in states:
                continue
            states.add(frozenset(state))
            if any(s in self.final_states for s in state):
                final_states.add(frozenset(state))

            for symbol in alphabet:
                new_state = {dest for substate in state for dest in self.transitions.get((substate, symbol), [])}
                if len(new_state) > 0:
                    transitions[(frozenset(state), symbol)] = [frozenset(new_state)]
                    if new_state not in states:
                        queue.append(new_state)


        self.states = states
        self.transitions = transitions
        self.final_states = final_states
        self.start_state = start_state
        self.check_dfa()


    def check_validity(self):
        dfa, eps = True, False
        for state in self.final_states:
            if state not in self.states:
                raise RuntimeError(f"{state} is not in states")
        if self.start_state not in self.states:
            raise RuntimeError(f"{self.start_state} is not in states")
        for state, symbol in self.transitions.keys():
            if state not in self.states:
                raise RuntimeError(f"{state} is not in states")
            if symbol not in self.alphabet:
                raise RuntimeError(f"Transition from {state} with invalid symbol {symbol}")
            if symbol == "":
                eps = True
            for destination in self.transitions.get((state, symbol), []):
                if destination not in self.states:
                    raise RuntimeError(f"Transition from {state} to {destination} with symbol {symbol} is not valid because {destination} is an invalid state")
                if len(self.transitions.get((state, symbol), [])) > 1:
                    dfa = False
        return dfa, eps

    def check_nfa(self):
        _, eps = self.check_validity()
        return eps == False

    def check_dfa(self):
        dfa, eps = self.check_validity()
        return dfa == True and eps == False

    def accepts(self, word):
        states = {self.start_state}
        for symbol in word:
            if symbol not in self.alphabet:
                return False
            new_states = set()
            for state in states:
                for destination in self.transitions.get((state, symbol), []):
                    new_states.add(destination)
            states = new_states
        for state in states:
            if state in self.final_states:
                return True
        return False

