from qubits import QubitPair
import string


class one_way_comm(object):

    def __init__(self, message_length, alphabet=string.printable):
        self.msg_len = message_length
        self.alphabet = alphabet  # all ascii characters
        self.qubit_pairs = {}
        self.qubits_per_symbol = 8 // 2  # 8 bits in byte, 2 qubits per pair
        self.num_of_qubit_pairs = self.qubits_per_symbol * message_length
        self.qubit_pair_pointer = 0

    def create_qubits(self):
        for i in range(self.num_of_qubit_pairs):
            self.qubit_pairs[i] = QubitPair()

    def create_entanglements(self):
        for i in range(self.num_of_qubit_pairs):
            self.qubit_pairs[i].hgate()
            self.qubit_pairs[i].cnot()

    def balvis_travels(self):
        '''Happens inside of pair class (it has both qubits)
           Balvis has access to his single qubit over that class '''
        pass

    def asja_get_message(self, text=""):
        ''' Take user input for asja's message '''

        msg = None

        while msg == None:
            msg = input("\n$ Please input the message: ")

            if any([c not in self.alphabet for c in msg]) or len(msg) != self.msg_len:
                print("\n$ Input must contain only ascii characters!")
                print("$ Input length must be {} !".format(self.msg_len))
                msg = None

        self.msg = msg

    def asja_prepares_qubits(self):
        ''' Conver each symbol of the message to byte representation,
            later it will be transmited over superdense protocol
            with 4 qubit pairs each containing 2 bits of information '''

        for c in self.msg:
            ascii = ord(c)
            byte = '{0:08b}'.format(ascii)

            for i in range(0, 8, 2):
                x = int(byte[i])
                y = int(byte[i + 1])

                if x == 0 and y == 0:
                    # For 00, the I (Identity) gate is applied
                    pass
                elif x == 0 and y == 1:
                    # For 01, the X (NOT) gate is applied
                    self.qubit_pairs[self.qubit_pair_pointer].xgate()
                elif x == 1 and y == 0:
                    # For 10, the Z gate is applied
                    self.qubit_pairs[self.qubit_pair_pointer].zgate()
                else:
                    # For 11, the X and Z gates are applied
                    self.qubit_pairs[self.qubit_pair_pointer].xgate()
                    self.qubit_pairs[self.qubit_pair_pointer].zgate()

                self.qubit_pair_pointer += 1

    def asja_sends_qubits(self, the_number_of_qubits=0):
        '''Happens inside of pair class (it has both qubits)
           Balvis has access to his single qubit over that class '''
        pass

    def balvis_prepares_qubits(self):
        ''' Determine what information was inserted by asja '''
        for i in range(self.num_of_qubit_pairs):
            self.qubit_pairs[i].cnot()
            self.qubit_pairs[i].hgate()

    def balvis_measures_qubits(self):
        ''' Determine what information was inserted by asja '''
        self.measures = []
        for i in range(self.num_of_qubit_pairs):
            res = self.qubit_pairs[i].measure()
            self.measures.append(res)

    def balvis_prints_message(self):
        ''' Decode raw bytes to readable ascii chars and recover whole message '''

        msg = ""
        byte = ""

        for m in self.measures:
            x, y = m
            byte += (str(x) + str(y))

            if len(byte) != 8:
                continue

            ascii = int(byte, 2)
            symbol = chr(ascii)
            msg += symbol
            byte = ""

        print(f"\n$ Balvins decoded message: {msg}")

    def main(self):
        ''' Main sequence, launching methods in correct order '''

        self.create_qubits()
        self.create_entanglements()
        self.balvis_travels()
        text_receiving = "text input is generated inside the method"
        self.asja_get_message(text_receiving)
        self.asja_prepares_qubits()
        the_number_of_qubits = 10  # number is known for balvis too
        self.asja_sends_qubits(the_number_of_qubits)
        self.balvis_prepares_qubits()
        self.balvis_measures_qubits()
        self.balvis_prints_message()


class two_way_comm(one_way_comm):
    ''' Class extends basic one_way_comm by overriding methods by
        more general ones, which take as an input different users.
        But in the end it actually does the same job. '''

    def __init__(self, max_message_length, alphabet=string.printable):
        super().__init__(max_message_length, alphabet=alphabet)

        self.symbols_used_count = 0  # Symbols already used
        self.max_message_length = max_message_length  # How much text is preallocated
        self.qubit_read_pointer = 0  # Point to track which qubit to read first

    def get_message(self, sender, text=""):
        ''' Take user input for message '''

        msg = None

        while msg == None:
            msg = input(f"\n$ Please input {sender}s the message: ")

            if any([c not in self.alphabet for c in msg]) or (
                    (len(msg) + self.symbols_used_count) > self.max_message_length):
                print("\n$ Input must contain only ascii characters!")
                print(f"$ Input must be shorter than {self.max_message_length - self.symbols_used_count + 1}!")
                msg = None

        self.msg = msg
        self.symbols_used_count += len(msg)

    def reader_prepares_qubits(self, reader):
        ''' Read next message '''
        self.end_of_message_pointer = self.qubit_read_pointer + self.qubits_per_symbol * len(self.msg)
        for i in range(self.qubit_read_pointer, self.end_of_message_pointer):
            self.qubit_pairs[i].cnot()
            self.qubit_pairs[i].hgate()

    def reader_measures_qubits(self, reader):
        ''' Read next message '''
        self.measures = []
        for i in range(self.qubit_read_pointer, self.end_of_message_pointer):
            res = self.qubit_pairs[i].measure()
            self.measures.append(res)
            self.qubit_read_pointer += 1

    def print_measures(self, reader):
        msg = ""
        byte = ""

        for m in self.measures:
            x, y = m
            byte += (str(x) + str(y))

            if len(byte) != 8:
                continue

            ascii = int(byte, 2)
            symbol = chr(ascii)
            msg += symbol
            byte = ""

        print(f"\n$ {reader} decoded message: {msg}")

    def prepares_qubits(self, sender):
        for c in self.msg:
            ascii = ord(c)
            byte = '{0:08b}'.format(ascii)

            for i in range(0, 8, 2):
                x = int(byte[i])
                y = int(byte[i + 1])

                if x == 0 and y == 0:
                    # For 00, the I (Identity) gate is applied
                    pass
                elif x == 0 and y == 1:
                    # For 01, the X (NOT) gate is applied
                    self.qubit_pairs[self.qubit_pair_pointer].xgate()
                elif x == 1 and y == 0:
                    # For 10, the Z gate is applied
                    self.qubit_pairs[self.qubit_pair_pointer].zgate()
                else:
                    # For 11, the X and Z gates are applied
                    self.qubit_pairs[self.qubit_pair_pointer].xgate()
                    self.qubit_pairs[self.qubit_pair_pointer].zgate()

                self.qubit_pair_pointer += 1

    def sends_qubits(self, sender):
        pass

    def main(self):
        self.create_qubits()
        self.create_entanglements()
        self.balvis_travels()

        # Communicate until there are qubits available
        while self.symbols_used_count < self.max_message_length:
            # Asja initiates first message
            self.get_message(sender="Asja")
            self.prepares_qubits(sender="Asja")
            self.sends_qubits(sender="Asja")

            # Balvis reads and prints the message
            self.reader_prepares_qubits("Balvis")
            self.reader_measures_qubits("Balvis")
            self.print_measures(reader="Balvis")

            if self.symbols_used_count >= self.max_message_length:
                break

            # Balvis sends the message if there is any qubits left
            self.get_message(sender="Balvis")
            self.prepares_qubits(sender="Balvis")
            self.sends_qubits(sender="Balvis")

            # Asja reads and prints the message
            self.reader_prepares_qubits("Asja")
            self.reader_measures_qubits("Asja")
            self.print_measures(reader="Asja")

        print("\n$ Out of qubits !")


if __name__ == '__main__':
    # Start one way communication
    # comm = one_way_comm(message_length=5)
    # comm.main()

    # Start two way communication
    comm = two_way_comm(10)
    comm.main()
