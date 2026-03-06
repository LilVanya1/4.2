class Uzl:
    def __init__(self, data):
        self.data = data
        self.next = None


class Sruct:
    def __init__(self):
        self.tail = None
        self.size = 0

    def add(self, value):
        new_uzl = Uzl(value)

        if self.tail is None:
            new_uzl.next = new_uzl
            self.tail = new_uzl
        else:
            new_uzl.next = self.tail.next
            self.tail.next = new_uzl
            self.tail = new_uzl

        self.size += 1
        return 1

    def dequeue(self):
        if self.tail is None:
            return None

        head = self.tail.next
        value = head.data

        if self.tail == head:
            self.tail = None
        else:
            self.tail.next = head.next

        self.size -= 1
        return value

    def peek(self):
        if self.tail is None:
            return None

        return self.tail.next.data

    def clear(self):
        while self.size > 0:
            self.dequeue()

    def get_size(self):
        return self.size

    def get_elements(self):
        if self.tail is None:
            return []

        elements = []
        current = self.tail.next

        for _ in range(self.size):
            elements.append(current.data)
            current = current.next

        return elements