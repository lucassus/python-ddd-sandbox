class SuperClassA:
    def __init__(self):
        self.a = 1


class SuperClassB:
    def __init__(self):
        self.b = 1


class SubClass(SuperClassA, SuperClassB):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    c = SubClass()
    print(c.a)
    # print(c.b)
