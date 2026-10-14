
class Dictionary:
    def __init__(self):
        self.size = 10
        self.table = [None] * self.size

    def hash_function(self, word):
        return sum(ord(ch) for ch in word) % self.size

    def add_word(self, word, meaning):
        index = self.hash_function(word)

        while self.table[index] is not None:
            if self.table[index][0] == word:
                self.table[index] = (word, meaning)
                print("Meaning updated!")
                return
            index = (index + 1) % self.size

        self.table[index] = (word, meaning)
        print("Word added successfully!")

    def search_word(self, word):
        index = self.hash_function(word)
        start = index

        while self.table[index] is not None:
            if self.table[index][0] == word:
                print("Meaning:", self.table[index][1])
                return
            index = (index + 1) % self.size
            if index == start:
                break

        print("Word not found!")

    def display(self):
        for i in range(self.size):
            print(i, ":", self.table[i])


d = Dictionary()

while True:
    print("\n1. Add Word")
    print("2. Search Word")
    print("3. Display Dictionary")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        word = input("Enter word: ").lower()
        meaning = input("Enter meaning: ")
        d.add_word(word, meaning)

    elif choice == "2":
        word = input("Enter word to search: ").lower()
        d.search_word(word)

    elif choice == "3":
        d.display()

    elif choice == "4":
        print("Exiting Dictionary Application")
        break

    else:
        print("Invalid choice!")
