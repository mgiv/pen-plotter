import turtle

# Code modified from https://www.geeksforgeeks.org/python/heighways-dragon-curve-python/
def dragon(iter, width):
    r = 'r'
    l = 'l'

    # assign our first iteration a right so we can build off of it
    old = r
    new = old

    # for inputs
    iteration = int(input('Enter iteration:'))

    # set the number of times we have been creating
    # the next iteration as the first
    cycle = 1

    # keep on generating the next iteration until desired iteration is reached
    while cycle < iteration:
        # add a right to the end of the old iteration and save it to the new
        new = (old) + (r)
        # flip the old iteration around(as in the first character becomes last)
        old = old[::-1]
        # cycling through each character in the flipped old iteration:
        for char in range(0, len(old)):
            # if the character is a right:
            if old[char] == r:
                # change it to a left
                old = (old[:char]) + (l) + (old[char + 1:])
            # otherwise, if it's a left:
            elif old[char] == l:
                # change it to a right
                old = (old[:char]) + (r) + (old[char + 1:])
                # add the modified old to the new iteration
        new = (new) + (old)

        # save the new iteration to old as well for use next cycle
        old = new

        # advance cycle variable to keep track of the number of times it's been done
        cycle = cycle + 1

    # Now we have it in l/r notation, we need to convert that into steps
    print(new)

