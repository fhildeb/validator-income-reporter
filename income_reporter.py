# System libraries
from datetime import datetime
import sys

# Internal library imports
from utility.terminal_outputs import printLine, printHead, printFoot, printIntro

def generate_income_report():
    # Generates the income report.

    # Start terminal outputs
    printHead()
    printIntro()

# Execute report when script is called
if __name__ == '__main__':
    try:
        generate_income_report()
    # Script gets exited
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully. \n")
        sys.exit(0)