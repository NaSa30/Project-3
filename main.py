import struct

# Node class: This objects would hold the index file's keys and values
#             along with the id number and the parent id
class Node:
    def __init__(self, degree, leaf):
        self.degree = degree
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []
        self.id = None
        self.parent = None

    # full() : Checks if the current nodes' childrens are full
    def full(self):
        return len(self.keys) == (2 * self.degree - 1)
    
# BTree class: Sorts the index file's keys and values into a BTree
class BTree:
    def __init__(self, degree):
        self.root = Node(degree, True)
        self.degree = degree

    # insert() : Inserts a node into the tree
    def insert(self, id, key, value):
        # If the root is at its limit, then it will split
        if self.root.full():
            newRoot = Node(self.degree, False)
            newRoot.children.append(self.root)
            self.split_child(newRoot, 0)
            self.root = newRoot
        self.insert_non_full(self.root, key, value)

    # insert_non_full() : Inserts the node, if the current node is not full
    #                     with their children node
    def insert_non_full(self, node, key, value):
        if node.leaf:
            # Adds the keys and values into the arrays
            node.keys.append(key)
            node.values.append(value)

            # Pairs the keys and values arrays together when sorting
            # Sorts based off keys
            sort_together = sorted(zip(node.keys, node.values))
            # Splits back into individual arrays
            node.keys, node.values = zip(*sort_together)
            node.keys = list(node.keys)
            node.values = list(node.values)

        else:
            # Find the child that should receive the key
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # If the children array does end up being full -> Split
            if node.children[i].full():
                self.split_child(node, i)
                # Picks either the side of the splitted array as the new key
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key, value)
        
    # split_child() : Process of spliting the child array
    def split_child(self, parent, i):
        child = parent.children[i]
        new_child = Node(self.degree, child.leaf)

        # Middle key/values moves as the parent
        mid = self.degree - 1
        parent.keys.insert(i, child.keys[mid])
        parent.values.insert(i, child.values[mid])
        parent.children.insert(i + 1, new_child)

        # Split keys/values and children
        new_child.keys = child.keys[mid + 1:]
        new_child.values = child.values[mid + 1:]
        child.keys = child.keys[:mid]

        # Checks if the child is a leaf
        if not child.leaf:
            new_child.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

    # printTree() : Prints out the BTree in order of the Key
    def printTree(self, node=None):
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            # Output the left child
            if not node.leaf:
                self.printTree(node.children[i])
            # Print the current key
            print(str(node.keys[i]) + "-" + str(node.values[i]) + " ")
        # Output the last child if the node has children
        if not node.leaf:
            self.printTree(node.children[-1])
    
    # search() : Search for a specific key in the BTree
    def search(self, key, node=None):
        if node is None:
            node = self.root

        # Find the first key 
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # Check if the key is found
        if i < len(node.keys) and key == node.keys[i]:
            return True
        # If the key is not found throughout all of the nodes
        if node.leaf:
            return False
        # Continue searching through other nodes
        return self.search(key, node.children[i])

# outputMenu() : Prints out the command options for the user the choose from
#                    Will add the index name when necessary
def outputMenu(fileName):
    # Checks if fileName contains a name
    currFile = ""
    if fileName != "":
        currFile = " (" + fileName + ")"
    
    # Output options
    print(" --- MENU" + currFile + " ---")
    print("  create     Create new index")
    print("  open       Set current index")
    print("  insert     Insert a new key/value pair into current index")
    print("  search     Search for a key in current index")
    print("  load       Insert key/value pairs from a file into current index")
    print("  print      Print all key/value pairs in current index in key order")
    print("  extract    Save all key/value pairs in current index into a file")
    print("  quit       Exit the program")

# integerCheck() : Checks if the user entered an ineteger input
def integerCheck(type):
    while True:
        try:
            num = int(input("Enter the " + type + " to insert: "))
            return num
        except:
            print("     !! Invalid input !!")

# fileExist() : Checks if the specific file name exist
def fileExist(fileName):
    try:
        with open(fileName, 'rb') as file:
            return True
    except IOError:
        return False
    
# checkMagicNum() : Checks if the file contains the magic number
def checkMagicNum(fileName):
    magicNum = ""
    with open(fileName, 'rb') as file:
        num = file.read(8)
        string = num.rstrip(b'\x00')
        magicNum = string.decode()
        
    if magicNum == "4337PRJ3":
        return True
    else:
        return False

    
# createFile() : Creates a binary file where it automatically
#                create and store the magic number, root node, amd id of the
#                next block.
#                It would also automatically create a BTree
def createFile(fileName):
    # File information
    num = "4337PRJ3"
    root = 0
    next = 1

    # Convert to binary where each is 8 bytes
    magicNum = num.encode()
    magicNum = magicNum[:8]
    rootID = root.to_bytes(8, 'big')
    nextID = next.to_bytes(8, 'big')
    
    # Store into a binary file
    with open(fileName, 'wb') as file:
        file.write(magicNum)
        file.write(rootID)
        file.write(nextID)

# insertFile() : Update the id number and add the key and value to the file
def insertFile(fileName, key, value, total):
    magicNum = ""
    root = None
    next = None
    values = []
    keys = []
    # Read file to locate the id for the next id
    with open(fileName, 'rb') as file:
        binaryData = file.read(8)
        string = binaryData.rstrip(b'\x00')
        magicNum = string.decode()

        binaryData = file.read(8)
        root = int.from_bytes(binaryData, 'big')

        binaryData = file.read(8)
        next = int.from_bytes(binaryData, 'big')

        if total != 0:
            for i in range(total):
                binaryData = file.read(8)
                num = int.from_bytes(binaryData, 'big')
                keys.append(num)

            for i in range(total):
                binaryData = file.read(8)
                num = int.from_bytes(binaryData, 'big')
                values.append(num)

    next += 1

    # Update file
    # Convert to binary where each is 8 bytes
    magicNum = num.encode()
    magicNum = magicNum[:8]
    rootID = root.to_bytes(8, 'big')
    nextID = next.to_bytes(8, 'big')
    
    # Store into a binary file
    with open(fileName, 'wb') as file:
        file.write(magicNum)
        file.write(rootID)
        file.write(nextID)

        if total != 0:
            for i in range(total):
                k = keys[i].to_bytes(8, 'big')
                file.write(k)
        k = key.to_byte(8, 'big')
        file.write(k)

        if total != 0:
            for i in range(total):
                v = values[i].to_bytes(8, 'big')
                file.write(v)
        v = value.to_byte(8, 'big')
        file.write(v)
    
# convertBTree() : Converts the binary file into BTRee

### MAIN ###
command = ""
fileName = ""
total = 0

# Loop until user enter's quit
while command != "quit":
    outputMenu(fileName)
    print()
    command = input("Enter command: ")
    command.lower
    
    # Identify the chosen command
    # CREATE Command
    if command == "create":
        fileName = input("Enter filename: ")
        
        # Check if file exist
        if fileExist(fileName):
            print("This file already exists")
            # Ask user if they want to overwrite it
            choice = input("Overwrite the existing file (Y/N): ")
            choice.lower()
            if choice == "y":
                createFile(fileName)
                print("     Index " + fileName + " created.")
            else:
                # Clear fileName
                fileName = ""

        else:
            createFile(fileName)
            print("     Index " + fileName + " created.")

    # OPEN command
    elif command == "open":
        fileName = input("Enter filename: ")
        
        # Check if file exist
        if not fileExist(fileName):
            print("     !! Index file does not exist !!")
            # Clear fileName
            fileName = ""

        else:
            # Check if the file contains the magic number
            if checkMagicNum(fileName):
                print("     Index " + fileName + " opened.")
            else:
                print("     !! The file does not have a magic number !!")
                # Clear fileName
                fileName = ""

    # INSERT command
    elif command == "insert":
        # Check if the user is currently in an open file
        if fileName == "":
            print("     !! No index are currently open !!")
        else:
            # Checks if the user input an integer
            key = integerCheck("key")
            value = integerCheck("value")
            insertFile(fileName, key, value, total)
            total += 1
            


    elif command == "search":
        print("SEARCH")
    elif command == "load":
        print("LOAD")


    elif command == "print":
        print("PRINT")
        # convertBTree()



    elif command == "extract":
        print("EXTRACT")
    elif command == "quit":
        print("EXIT")
    else:
        print("Invalid choice. Try again.")
    print()