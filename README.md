# Logic Circuit Truth Table

_Python_ module including a variety of logic gate classes, and a truth table class to automatically generate truth tables of logic circuits.

Click [here](https://github.com/adam-rumpf/logic-circuit-truth-table/releases/tag/v0.4) for the latest (pre-)release.

## Overview

This module includes a variety of classes to define logic gates and other related components. A logic circuit can be built by instantiating gate objects linked to each other. Most logic gates require one or more output gates, meaning that the circuit must generally be built beginning with the outputs and working backwards.

Most gates are instantiated in the same way, and require defining a list of output gates (one for each output). Gates which accept multiple inputs maintain these inputs in a list. The keyword `out_ports` argument accepts a list of port indices corresponding to the output gates. The keyword `name` argument accepts a name for the gate to use in truth tables.

For example, if we already have two `XOR` gate objects called `Xor1` and `Xor2`, then instantiating a `SPLIT` gate with `SplitGate([Xor1, Xor2], out_ports=[1, 0])` would connect the `SPLIT` gate to port `1` of `Xor1` and port `0` of `Xor2`. Note that even gates with a single output must be given their output gates in list form.

Most gates also include a `process()` method which causes it to evaluate its boolean inputs and calculate the appropriate boolean outputs, and a `_send_out()` method which sends its outputs to all output gates and prompts them to also evaluate their `process()` methods. This may lead to infinite loops if there are cycles in the logic circuit.

The `IN` and `SWITCH` gates both include a `toggle()` method which can be used to set their internal state. For `IN`, this means setting it to `True` or `False`, and for `SWITCH`, this means either transferring its output to its first ("left") or its second ("right") output gate.

The `OUT` gate has no output, and is mostly meant for use in defining truth table entries.

The `TruthTable` class can store sets of variable inputs, constant inputs, and outputs, and cycle through every possible setting of the variable inputs to generate a complete truth table of the resulting outputs via the `generate_table()` method.

The `circuit_load()` function can be used to load a circuit defined in an external text file in the `circuits/` folder. The format for a circuit file is described in the included `_template` file. As the input file is read, gate objects are created and linked to each other, and then used to instantiate a `TruthTable` object. The function returns a dictionary of the created gate objects as well as the created `TruthTable` object.

## Logic Gate Classes

* Inputs (0 Inputs, 1 Output):
    * `InGate` -- Simply outputs a signal. Includes a `toggle()` method which sets its signal as `True` or `False`. Can be used as a truth table input.
    * `TrueGate` -- Like `InGate`, but outputs a constant `True` signal.
    * `FalseGate` -- Like `InGate`, but outputs a constant `False` signal.

* Outputs (1 Input, 0 Outputs):
    * `OutGate` -- Simply stores its input signal. Meant for use in defining the truth table outputs.

* Unary Gates (1 Input, 1 Output):
    * `DiodeGate` -- Outputs a copy of its own input signal.
    * `NotGate` -- Outputs negation of input signal.

* Binary Gates (2 Inputs, 1 Output):
    * `AndGate` -- Outputs `True` if both inputs are `True`, and `False` otherwise.
    * `NandGate` -- Outputs `True` if both inputs are `False`, and `False` otherwise.
    * `OrGate` -- Outputs `True` if at least one input is `True`, and `False` otherwise.
    * `NorGate` -- Outputs `True` if at least one input is `False`, and `False` otherwise.
    * `XorGate` -- Outputs `True` if exactly one input is `True`, and `False` otherwise.
    * `XnorGate` -- Outputs `True` if both inputs are the same, and `False` otherwise.

* Splitters (1 Input, 2 Outputs):
    * `SplitGate` -- Outputs a copy of its own input signal to both outputs.
    * `SwitchGate` -- Outputs a copy of its own input signal to one output gate, outputting `False` to the other gate. Includes a `toggle()` method which selects which gate is selected. `False` indicates gate `0` ("left") while `True` indicates gate `1` ("right"). Can be used as a truth table input.

## Logic Circuit File Format

A logic circuit can be defined as a tab-separated table in a text file. Each row corresponds to a gate in the circuit. The main module's `circuit_load()` method will attempt to create a `TruthTable` object with the specified gates, in the order of their listing in the circuit file. Since gates always require their output gates to already be defined, the gates must be listed in reverse topological order, beginning with the outputs and working backwards to the inputs. That is, nothing should be listed as an `OutGate` unless it has already been defined in a previous row as an ID.

The column order is:
1. `Name` -- Name string for the gate. Must be unique for each gate, and must not contain any whitespace characters.
1. `Type` -- String name of gate type. Case insensitive. Must be chosen from the following list:
    * `OUT`
    * `IN`
    * `TRUE`
    * `FALSE`
    * `AND`
    * `OR`
    * `XOR`
    * `NAND`
    * `NOR`
    * `XNOR`
    * `NOT`
    * `DIODE`
    * `SPLIT`
    * `SWITCH`
1. `OutGates` -- Tab-separated list of output gate names. The length of the list must be appropriate for the given type of gate.
1. `OutPorts` -- Tab-separated list of output port IDs. The length of the list must be appropriate for the given type of gate.

Comment lines may be included if preceded by a "`#`" symbol.
