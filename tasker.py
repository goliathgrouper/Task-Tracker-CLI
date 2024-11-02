import sys, json

def main():
    arguments = sys.argv[1:]
    argc = len(arguments)
    if argc == 0:
        sys.exit('No arguments provided')
    elif argc > 3:
        sys.exit('Too many arguments provided')

    # Create tasklist.json if doesn't exist
    try:
        tasklist = open('tasklist.json', 'x')
        tasklist.close()
    except FileExistsError:
        pass



if __name__ == '__main__':
    main()