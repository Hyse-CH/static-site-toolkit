from sys import argv
from commands import *

def parseArgv(argv: list[str]):
    match argv[0]:
        case 'build': cmdBuild()
        case 'help': cmdHelp()
        case other: print('Use help to see STK\'s usage')

def main(args: list[str]) -> None:
    args.pop(0) # Remove file's name from arguments
    parseArgv(args)

if __name__ == '__main__':
    main(argv)