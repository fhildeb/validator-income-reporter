# STYLES TERMINAL OUTPUT

def printLine(text=None, offset=False):
    """
    Prints a line in a formatted box with optional centered text.

    :param text (str, optional): The text to print within the box. Defaults to None.
    :param offset (bool, optional): Emoji offset the text to the left. Defaults to False.
    """

    # Terminal box width
    box_width = 76

    # If there was no text input
    if text is None:
        
        # Prints a separator line
        print("├" + "─" * (box_width - 2) + "┤")
    else:
        text = f" {text} "
        text_length = len(text)
        padding = box_width - 3 - text_length

        # Calculate Emoji offset
        if offset:
            padding = max(padding - 1, 0)
            
        # Prints text line
        print("|" + " " + text + " " * padding + "|")

def printHead():
    # Prints the header line of the terminal report box.
    print("\n┌──────────────────────────────────────────────────────────────────────────┐")

def printIntro():
    # Prints the introduction section of the terminal view, including the title and author.
    printLine()
    print("|                         VALIDATOR INCOME REPORTER                        |")
    print("|                            by Felix Hildebrandt                          |")
    printLine()

def printFoot():
    # Prints the footer line of the terminal report box.
    print("└──────────────────────────────────────────────────────────────────────────┘ \n")