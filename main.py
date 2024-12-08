# def outputMenu() : Prints out the command options for the user the choose from
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

### MAIN ###
command = ""
fileName = ""

# Loop until user enter's quit
while command != "quit":
    outputMenu(fileName)
    print()
    command = input("Enter command: ")
    command.lower
    
    # Identify the chosen command
    if command == "create":
        print("CREATE")
    elif command == "open":
        print("OPEN")
    elif command == "insert":
        print("INSERT")
    elif command == "search":
        print("SEARCH")
    elif command == "load":
        print("LOAD")
    elif command == "print":
        print("PRINT")
    elif command == "extract":
        print("EXTRACT")
    elif command == "quit":
        print("EXIT")
    else:
        print("Invalid choice. Try again.")
    print()