from Domain.Item import Item
from Domain.LR0Table import LR0Table
from Domain.Production import Production
from Domain.State import State


class Test:
    @staticmethod
    def test_states1():
        lr0table = LR0Table("t1.txt")
        productions = [Production(0, "S", ["A", "A"]), Production(1, "A", ["a", "A"]),
                       Production(2, "A", ["b"]), Production(-1, "S'", "S")]
        states = [State(0, items=[Item(productions[-1], 0), Item(productions[0], 0),
                                     Item(productions[1], 0), Item(productions[2], 0)]),
                  State(1, items=[Item(productions[-1], 1)]),
                  State(2, items=[Item(productions[0], 1), Item(productions[1], 0), Item(productions[2], 0)]),
                  State(3,items=[Item(productions[1], 1), Item(productions[1], 0), Item(productions[2], 0)]),
                  State(4, items=[Item(productions[2], 1)]),
                  State(5, items=[Item(productions[0], 2)]),
                  State(6, items=[Item(productions[1], 2)])]

        for s in states:
            if s not in lr0table.states:
                raise AssertionError(f"Test and loaded states do not match! State {s} not in loaded table.")

    @staticmethod
    def test_states2():
        lr0table = LR0Table("t2.txt")
        productions = [Production(0, "S", ["a", "A"]), Production(1, "A", ["b", "A"]),
                       Production(2, "A", ["c"]), Production(-1, "S'", "S")]
        states = [State(0, items=[Item(productions[-1], 0), Item(productions[0], 0)]),
                  State(1, items=[Item(productions[-1], 1)]),
                  State(2, items=[Item(productions[0], 1), Item(productions[1], 0), Item(productions[2], 0)]),
                  State(3, items=[Item(productions[1], 1), Item(productions[1], 0), Item(productions[2], 0)]),
                  State(4, items=[Item(productions[2], 1)]),
                  State(5, items=[Item(productions[0], 2)]),
                  State(6, items=[Item(productions[1], 2)])]

        for s in states:
            if s not in lr0table.states:
                raise AssertionError(f"Test and loaded states do not match! State {s} not in loaded table.")

    @staticmethod
    def test_goto():
        lr0table = LR0Table("t2.txt")

        productions = [Production(0, "S", ["a", "A"]), Production(1, "A", ["b", "A"]),
                       Production(2, "A", ["c"]), Production(-1, "S'", "S")]
        state = State(0, items=[Item(productions[-1], 0), Item(productions[0], 0)])
        s1 = lr0table.goto(state, "ksge")
        s2 = State(-1, items=[])
        # should return empty state
        assert s1 == s2, f"States {s1} and {s2} do not match!"
        s1 = lr0table.goto(state, "S")
        s2 = State(-1, items=[Item(productions[-1], 1)])
        # check to return correct states
        assert s1 == s2, f"States {s1} and {s2} do not match!"
        s1 = lr0table.goto(state, "a")
        s2 = State(2, items=[Item(productions[0], 1), Item(productions[1], 0), Item(productions[2], 0)])
        assert s1 == s2, f"States {s1} and {s2} do not match!"

    @staticmethod
    def test_closure():
        lr0table = LR0Table("t1.txt")
        productions = [Production(0, "S", ["A", "A"]), Production(1, "A", ["a", "A"]),
                       Production(2, "A", ["b"]), Production(-1, "S'", "S")]

        # test developed
        s1 = lr0table.closure(State(-1, items=[Item(productions[-1], 0)]))
        s2 = State(-1, items=[Item(productions[-1], 0), Item(productions[0], 0),
                                     Item(productions[1], 0), Item(productions[2], 0)])
        assert s1 == s2, f"Closure {s1} and expected output {s2} do not match!"

        # test one that stops in one pass
        s1 = lr0table.closure(State(-1, items=[Item(productions[-1], 1)]))
        s2 = State(-1, items=[Item(productions[-1], 1)])
        assert s1 == s2, f"Closure {s1} and expected output {s2} do not match!"


try:
    Test.test_closure()
    print("Closure test passed!")
except AssertionError as e:
    print(e)

try:
    Test.test_goto()
    print("Goto test passed!")
except AssertionError as e:
    print(e)

try:
    Test.test_states1()
    print("State test 1 passed!")
except AssertionError as e:
    print(e)

try:
    Test.test_states2()
    print("State test 2 passed!")
except AssertionError as e:
    print(e)
