

class Memory:
    def __init__(self, name):
        self.name = name
        self.memory = {}
        pass

    def has_key(self, name):
        return name in self.memory

    def get(self, name):
        return self.memory[name]

    def put(self, name, value):
        self.memory[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None):
        self.stack = [memory] if memory else []

    def get(self, name):
        for memory in reversed(self.stack):
            if memory and memory.has_key(name):
                return memory.get(name)
            
        return None # It shouldn't be reached because typeChecker throws "Out of scope"

    def insert(self, name, value):
        if self.stack:
            self.stack[-1].put(name, value)

    def set(self, name, value):
        for memory in reversed(self.stack):
            if memory and memory.has_key(name):
                memory.put(name, value)
                return

        self.insert(name, value)


    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        if self.stack:
            return self.stack.pop()

