"""A module for generating truth tables of arrangements of logic gates.

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
"""

import math

###############################################################################
# Global Functions
###############################################################################

#==============================================================================
def number_to_boolean(num, bound):
    """Converts a number to a boolean representation of the binary expansion.

    Converts a decimal value to binary, and then the binary digits to a boolean
    vector. For example, number_to_boolean(5) would return [True, False, True]
    since 5 in binary is 101, and [1, 0, 1] in boolean is [True, False, True].
    """

    fstring = "{0:0"+str(math.ceil(math.log(bound, 2)))+"b}"

    return [bool(int(c)) for c in fstring.format(num)]

###############################################################################
# Gate Classes
###############################################################################

#==============================================================================
class Gate:
    """Generic gate template for use as a parent class."""

    #--------------------------------------------------------------------------
    def __init__(self, ports, out_gates, out_ports=[0], name="<gate>"):
        """Constructor links gate to a given output gate.

        Requires a number of input ports and a list of output gate pointers.
        Optionally can specify port IDs of output gates and a name.
        """

        self.out_gates = out_gates # list of output gates
        self.out_ports = out_ports # indices of output gate ports
        self.name = name # name for use in string output
        self.inputs = [False for i in range(ports)] # list of input values
        self.outputs = [False for i in range(len(out_gates))] # output values

    #--------------------------------------------------------------------------
    def __str__(self):
        """Default string is simply name."""

        return self.name

    #--------------------------------------------------------------------------
    def process(self):
        """Placeholder input processor, overwritten by specific gates."""

        pass

    #--------------------------------------------------------------------------
    def send_out(self):
        """Sends internal state to output gate and prompts it to process."""

        for i in range(len(self.outputs)):
            self.out_gates[i].inputs[self.out_ports[i]] = self.outputs[i]
            self.out_gates[i].process()

    #--------------------------------------------------------------------------
    def state_name(self):
        """String to represent internal state in truth tables."""

        if self.inputs[0] == False:
            return "F"
        elif self.inputs[0] == True:
            return "T"
        else:
            return "?"

#==============================================================================
class OUT(Gate):
    """OUTput which simply stores its input value."""

    #--------------------------------------------------------------------------
    def __init__(self, name="<gate>"):
        """Constructor initializes several internal variables."""

        self.name = name
        self.inputs = [False]
        self.outputs = [False]

    #--------------------------------------------------------------------------
    def process(self):
        """Input processor simply sets state to only input."""

        self.outputs[0] = self.inputs[0]

    #--------------------------------------------------------------------------
    def send_out(self):
        """Placeholder output sender to overwrite standard gate."""

        pass

#==============================================================================
class IN(Gate):
    """INput which simply outputs its input value."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """IN simply sends its own state to its output gate."""

        self.send_out()

    #--------------------------------------------------------------------------
    def toggle(self, state):
        """Sets own internal state and sends to output."""

        self.inputs[0] = state
        self.outputs[0] = state
        self.send_out()

#==============================================================================
class TRUE(Gate):
    """Outputs a constant True signal."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports and sets input/output to True."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

        self.inputs[0] = True
        self.outputs[0] = True

    #--------------------------------------------------------------------------
    def process(self):
        """IN simply sends its own state to its output gate."""

        self.send_out()

#==============================================================================
class FALSE(Gate):
    """Outputs a constant False signal."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports and sets input/output to True."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

        self.inputs[0] = False
        self.outputs[0] = False

    #--------------------------------------------------------------------------
    def process(self):
        """IN simply sends its own state to its output gate."""

        self.send_out()

#==============================================================================
class AND(Gate):
    """AND gate. Outputs True if both inputs are True."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = self.inputs[0] and self.inputs[1]
        self.send_out()

#==============================================================================
class OR(Gate):
    """OR gate. Outputs True if at least one input is True."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = self.inputs[0] or self.inputs[1]
        self.send_out()

#==============================================================================
class XOR(Gate):
    """XOR gate. Outputs True if exactly one input is True."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = ((self.inputs[0] or self.inputs[1]) and not
                    (self.inputs[0] and self.inputs[1]))
        self.send_out()

#==============================================================================
class NAND(Gate):
    """NAND gate. Outputs True if both inputs are False."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = not (self.inputs[0] and self.inputs[1])
        self.send_out()

#==============================================================================
class NOR(Gate):
    """NOR gate. Outputs True if at least one input is False."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = not (self.inputs[0] or self.inputs[1])
        self.send_out()

#==============================================================================
class XNOR(Gate):
    """XNOR gate. Outputs True if both inputs are the same."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 2, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = not (((self.inputs[0] or self.inputs[1]) and not
                    (self.inputs[0] and self.inputs[1])))
        self.send_out()

#==============================================================================
class NOT(Gate):
    """NOT Gate. Negates input signal."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = not self.inputs[0]
        self.send_out()

#==============================================================================
class DIODE(Gate):
    """Diode. Simply carries signal unchanged, but only in one direction."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = self.inputs[0]
        self.send_out()

#==============================================================================
class SPLIT(Gate):
    """Splits a signal into two outputs."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0, 0], name="<gate>"):
        """Constructor sets number of ports."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[0] = self.inputs[0]
        self.outputs[1] = self.inputs[0]
        self.send_out()

#==============================================================================
class SWITCH(Gate):
    """Splitter that toggles between which output gate to trigger."""

    #--------------------------------------------------------------------------
    def __init__(self, out_gates, out_ports=[0, 0], name="<gate>"):
        """Constructor sets number of ports and initializes direction."""

        Gate.__init__(self, 1, out_gates, out_ports=out_ports, name=name)

        self.direction = False # False for first output, True for second output

    #--------------------------------------------------------------------------
    def process(self):
        """Evaluates own boolean inputs and sends result to output gate."""

        self.outputs[int(self.direction)] = self.inputs[0] # selected gate
        self.outputs[(int(self.direction)+1)%2] = False # non-selected gate
        self.send_out()

    #--------------------------------------------------------------------------
    def toggle(self, state):
        """Sets direction and sends updated outputs."""

        self.direction = state
        self.process()

    #--------------------------------------------------------------------------
    def state_name(self):
        """State name corresponds to direction of switch."""

        if self.direction == False:
            return "L"
        elif self.direction == True:
            return "R"
        else:
            return "?"

###############################################################################
# Truth Table Generation Class
###############################################################################

#==============================================================================
class TruthTable:
    """Class for generating truth tables for a given logic circuit.

    Used to store a collection of logic gate inputs and outputs. Automatically
    checks every possible combination of inputs and displays the resulting
    outputs.
    """

    #--------------------------------------------------------------------------
    def __init__(self, inputs=[], constants=[], outputs=[]):
        """Empty TruthTable class constructor initializes lists.

        Accepts optional keyword arguments to set the sets of input, constant,
        and output gates.
        """

        self.inputs = inputs # list of toggleable input gates
        self.constants = constants # list of constant input gates
        self.outputs = outputs # list of output gates

    #--------------------------------------------------------------------------
    def get_outputs(self, input_values):
        """Returns all outputs for a given list of input values."""

        # Update each input and prompt all constant inputs to re-send signals
        for i in range(len(input_values)):
            self.inputs[i].toggle(input_values[i])
            for j in range(len(self.constants)):
                self.constants[j].process()

        # Return list of outputs
        return [out.state_name() for out in self.outputs]

    #--------------------------------------------------------------------------
    def generate_table(self):
        """Generates outputs for every possible input combination."""

        # Print label row
        row = ""
        for g in self.inputs:
            row += g.name + "\t"
        for g in self.outputs:
            row += g.name + "\t"
        print(row)

        for i in range(2**len(self.inputs)):
            # Use binary string to generate boolean vector
            input_set = number_to_boolean(i, 2**len(self.inputs))

            # Generate outputs from inputs
            output_set = self.get_outputs(input_set)

            # Print values
            row = ""
            for g in self.inputs:
                row += g.state_name() + "\t"
            for j in output_set:
                row += str(j) + "\t"
            print(row)

###############################################################################
# Execution
###############################################################################

# Example
if __name__ == "__main__":

    # Define a system of logic gates
    TestOut = OUT(name="OUT")
    TestAnd0 = AND([TestOut])
    TestAnd10 = AND([TestAnd0], out_ports=[0])
    TestAnd11 = AND([TestAnd0], out_ports=[1])
    TestSplit = SPLIT([TestAnd10, TestAnd11], out_ports=[1, 0])
    TestXor20 = XOR([TestAnd10], out_ports=[0])
    TestXor21 = XOR([TestSplit])
    TestAnd22 = AND([TestAnd11], out_ports=[1])
    TestSwitch0 = SWITCH([TestXor20, TestXor21], out_ports=[1, 0],
                         name="Switch1")
    TestSwitch1 = SWITCH([TestXor21, TestAnd22], out_ports=[1, 0],
                         name="Switch2")
    TestIn0 = IN([TestXor20], out_ports=[0], name="IN2")
    TestIn1 = IN([TestSwitch0], name="IN3")
    TestIn2 = IN([TestSwitch1], name="IN4")
    TestIn3 = IN([TestAnd22], out_ports=[1], name="IN5")

    # Define a truth table object
    TestTable = TruthTable(inputs=[TestIn0, TestIn1, TestIn2, TestIn3,
                                   TestSwitch0, TestSwitch1],
                                    outputs=[TestOut])

    # Generate and display truth table
    TestTable.generate_table()
