# logic-circuit-truth-table
Python module including a variety of logic gate classes, and a truth table class
to automatically generate truth tables of logic circuits.

###############################################################################

This module includes a variety of classes to define logic gates and other
related components. A logic circuit can be built by instantiating gate objects
linked to each other. Most logic gates require one or more output gates,
meaning that the circuit must generally be built beginning with the outputs and
working backwards.

Most gates are instantiated in the same way, and require defining a list of
output gates (one for each output). Gates which accept multiple inputs maintain
these inputs in a list. The keyword 'out_ports' argument accepts a list of port
indices corresponding to the output gates. The keyword 'name' argument accepts
a name for the gate to use in truth tables.

For example, if we already have two XOR gate objects called Xor1 and Xor2, then
instantiating a SPLIT gate with SPLIT([Xor1, Xor2], out_ports=[1, 0]) would
connect the SPLIT gate to port 1 of Xor1 and port 0 of Xor2. Note that even
gates with a single output must be given their output gates in list form.

Most gates also include a process() method which causes it to evaluate its
boolean inputs and calculate the appropriate boolean outputs, and a send_out()
method which sends its outputs to all output gates and prompts them to also
evaluate their process() methods. This may lead to infinite loops if there are
cycles in the logic circuit.

The IN and SWITCH gates both include a toggle() method which can be used to set
their internal state. For IN, this means setting it to True or False, and for
SWITCH, this means either transferring its output to its first ('left') or its
second ('right') output gate.

The OUT gate has no output, and is mostly meant for use in defining truth table
entries.

The TruthTable class can store sets of variable inputs, constant inputs, and
outputs, and cycle through every possible setting of the variable inputs to
generate a complete truth table of the resulting outputs via the
generate_table() method.

###############################################################################

The following logic gates are included:

    Inputs (0 Inputs, 1 Output):
        IN -- Simply outputs a signal. Includes a toggle() method which sets
            its signal as True or False. Can be used as a truth table input.
        TRUE -- Like IN, but outputs a constant True signal.

    Outputs (1 Input, 0 Outputs):
        OUT -- Simply stores its input signal. Meant for use in defining the
            truth table outputs.

    Unary Gates (1 Input, 1 Output):
        DIODE -- Outputs a copy of its own input signal.
        NOT -- Outputs negation of input signal.

    Binary Gates (2 Inputs, 1 Output):
        AND -- Outputs True if both inputs are True, and False otherwise.
        NAND -- Outputs True if both inputs are False, and False otherwise.
        OR -- Outputs True if at least one input is True, and False otherwise.
        NOR -- Outputs True if at least one input is False, and False
            otherwise.
        XOR -- Outputs True if exactly one input is True, and False otherwise.
        XNOR -- Outputs True if both inputs are the same, and False otherwise.

    Splitters (1 Input, 2 Outputs):
        SPLIT -- Outputs a copy of its own input signal to both outputs.
        SWITCH -- Outputs a copy of its own input signal to one output gate,
            outputting False to the other gate. Includes a toggle() method
            which selects which gate is selected. False indicates gate 0
            ('left') while True indicates gate 1 ('right'). Can be used as a
            truth table input.
