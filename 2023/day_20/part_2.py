# Start time: 14:16
# End time:

import aocd

data = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

data = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

data = aocd.get_data(year=2023, day=20)

LOW = 0
HIGH = 1


class Module:
    low_pulses: int = 0
    high_pulses: int = 0
    destinations: list[str]
    name: str

    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations

    def update_pulses(self, pulse_type: int):
        if pulse_type == LOW:
            self.low_pulses += 1
        elif pulse_type == HIGH:
            self.high_pulses += 1
        else:
            raise Exception(f"Unknown pulse type: {pulse_type}")

        # print(f"{self.name}: {self.low_pulses} low | {self.high_pulses} high")

    def activate(
        self, pulse_type: int, from_module: str, debug: bool
    ) -> list[tuple[str, int, str]]:
        raise NotImplementedError


class Broadcaster(Module):
    def activate(
        self, pulse_type: int, from_module: str, debug: bool
    ) -> list[tuple[str, int, str]]:
        self.update_pulses(pulse_type)

        if debug:
            for dest in self.destinations:
                print(f"{self.name} -0-> {dest}")

        return [(dest, 0, self.name) for dest in self.destinations]

    def __str__(self):
        return f"Broadcaster -> {self.destinations}"


class FlipFlop(Module):
    current_state = LOW

    def activate(
        self, pulse_type: int, from_module: str, debug: bool
    ) -> list[tuple[str, int, str]]:
        self.update_pulses(pulse_type)
        if pulse_type == HIGH:
            return []

        self.current_state = 1 - self.current_state

        if debug:
            for dest in self.destinations:
                print(f"{self.name} -{self.current_state}-> {dest}")

        return [(dest, self.current_state, self.name) for dest in self.destinations]

    def __str__(self):
        return f"FlipFlop {self.name} ({self.current_state}) -> {self.destinations}"


class Conjunction(Module):
    inputs: dict[str, int] = None

    def activate(
        self, pulse_type: int, from_module: str, debug: bool
    ) -> list[tuple[str, int, str]]:
        if from_module not in self.inputs:
            raise Exception(
                f"Conj. {self.name} sent pulse from {from_module}, which is not an input: {self.inputs.keys()}"
            )

        self.update_pulses(pulse_type)
        self.inputs[from_module] = pulse_type
        output_pulse_type = LOW if all(self.inputs.values()) else HIGH

        if debug:
            # print(f"Conj. {self.name} inputs: {self.inputs}")
            for dest in self.destinations:
                print(
                    f"{self.name} -{output_pulse_type}-> {dest}\t(inputs: {self.inputs})"
                )

        return [(dest, output_pulse_type, self.name) for dest in self.destinations]

    def __str__(self):
        return f"Conjunction {self.name} ({self.inputs}) -> {self.destinations}"


class Output(Module):
    def activate(
        self, pulse_type: int, from_module: str, debug: bool
    ) -> list[tuple[str, int, str]]:
        self.update_pulses(pulse_type)

        # if self.name == "rx":
        #     print(f"rx received pulse: {pulse_type}")

        return []

    def __str__(self):
        return f"Output {self.name}"


def build_module_map(data: str) -> dict[str, Module]:
    module_map = {}
    for line in data.splitlines():
        # print(line)
        module_info, destinations_str = line.split(" -> ")
        destinations = destinations_str.split(", ")

        module_class, name = Broadcaster, "broadcaster"
        if module_info[0] == "%":
            module_class = FlipFlop
            name = module_info[1:]
        if module_info[0] == "&":
            module_class = Conjunction
            name = module_info[1:]

        module = module_class(name, destinations)
        module_map[name] = module

    # Add output modules
    output_names = set()
    for module in module_map.values():
        for dest_name in module.destinations:
            if dest_name not in module_map:
                output_names.add(dest_name)
    for output_name in output_names:
        output_module = Output(output_name, [])
        module_map[output_name] = output_module

    # Add the Conjunction inputs
    for input_name, input_module in module_map.items():
        for dest_name in input_module.destinations:
            dest_module = module_map[dest_name]
            if isinstance(dest_module, Conjunction):
                if not dest_module.inputs:
                    dest_module.inputs = {}
                dest_module.inputs[input_name] = LOW

    return module_map


def push_button(module_map: dict[str, Module], debug: bool = False) -> None:
    next_modules = [("broadcaster", LOW, "button")]
    while next_modules:
        next_name, pulse_type, input_name = next_modules.pop(0)
        next_module = module_map[next_name]
        next_next_modules = next_module.activate(pulse_type, input_name, debug)
        next_modules.extend(next_next_modules)


def get_pulse_counts(module_map: dict[str, Module]) -> dict[int, int]:
    pulse_counts = {LOW: 0, HIGH: 0}
    for module in module_map.values():
        pulse_counts[LOW] += module.low_pulses
        pulse_counts[HIGH] += module.high_pulses
        # print(pulse_counts)
    return pulse_counts


module_map = build_module_map(data)
rx = module_map["rx"]
num_presses = 0
while rx.low_pulses == 0:
    num_presses += 1
    if num_presses % 10000 == 0:
        print(f"Presses so far: {num_presses}")
    # push_button(module_map, debug=True)
    push_button(module_map)

print(num_presses)
