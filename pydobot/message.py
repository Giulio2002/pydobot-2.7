class Message:
    def __init__(self, b=None):
        if b is None:
            self.header = bytes([0xAA, 0xAA])
            self.len = 0x00
            self.ctrl = 0x00
            self.params = bytes([])
            self.checksum = None
        else:
            self.header = b[0:2]
            self.len = b[2]
            self.id = b[3]
            self.ctrl = b[4]
            self.params = b[5:-1]
            self.checksum = b[-1:][0]

    def __repr__(self):
        return "Message()"

    def __str__(self):
        self.refresh()
        ret = "%s:%d:%d:%d:%s:%s" % (self.header.hex(), self.len, self.id, self.ctrl, self.params.hex(), self.checksum)
        return ret.upper()

    def refresh(self):
        if self.checksum is None:
            self.checksum = self.id + self.ctrl
            for i in range(len(self.params)):
                self.checksum += self.params[i]
            self.checksum = self.checksum % 256
            self.checksum = 2 ** 8 - self.checksum
            self.checksum = self.checksum % 256
            self.len = 0x02 + len(self.params)

    def bytes(self):
        self.refresh()
        if len(self.params) > 0:
            command = bytearray([0xAA, 0xAA, self.len, self.id, self.ctrl])
            command.extend(self.params)
            command.append(self.checksum)
        else:
            command = bytes([0xAA, 0xAA, self.len, self.id, self.ctrl, self.checksum])
        return command

