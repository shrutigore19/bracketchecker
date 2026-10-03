# PROBLEM: Check if brackets in code are balanced.(stack using linked list)
#shruti gore 
# roll no: 51

class Node:
    """One box in the chain: holds a value and points to the next box."""
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top = None          

    def is_empty(self):
        return self.top is None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top  
        self.top = new_node        

    def pop(self):
        value = self.top.value     
        self.top = self.top.next   
        return value


MATCH = {")": "(", "]": "[", "}": "{"}


def is_balanced(code, show_steps=False):
    stack = Stack()

    for ch in code:
        if ch in "([{":                   
            stack.push(ch)
            if show_steps:
                print(f"  see '{ch}'  -> push it")

        elif ch in ")]}":                 
            if stack.is_empty():
                if show_steps:
                    print(f"  see '{ch}'  -> stack empty, nothing to match!")
                return False

            top = stack.pop()
            if top != MATCH[ch]:
                if show_steps:
                    print(f"  see '{ch}'  -> top was '{top}', no match!")
                return False
            if show_steps:
                print(f"  see '{ch}'  -> matches '{top}', pop it")

    
    if not stack.is_empty():
        if show_steps:
            print("  end of input -> some bracket was never closed!")
        return False

    return True


print("Bracket Checker (type 'quit' to exit)")
print("-" * 40)

while True:
    code = input("\nEnter code: ")

    if code.strip().lower() == "quit":
        print("Bye!")
        break

    show = input("Show steps? (y/n): ").strip().lower() == "y"

    if is_balanced(code, show_steps=show):
        print("Result: Balanced")
    else:
        print("Result: NOT balanced")