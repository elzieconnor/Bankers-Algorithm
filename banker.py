#! /usr/bin/python

"""*******************************************************

Connor Elzie
CSC236: Operating Systems
Project 4: Banker Algorithm
Due Date: October 27th, 2020
Instructor: Dr. Siming, Liu

*******************************************************"""

import sys

"""*************************************************************

Matrix Initialization Function

This function splits the string items in the imported lists
and then converts them to integers to be used by the rest
of the program.

Return Value
------------
None

Value Parameters
----------------
matrix          list              list of imported values

*************************************************************"""

def matrixInitialize(matrix):

    # Split the string items into seperate lists
    for x in range(len(matrix)):
        split = matrix[x].split()
        matrix[x] = split

    # Convert list items to integers
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            matrix[x][y] = int(matrix[x][y])

"""*************************************************************

Calculate Need Function

This function calculates the need by subtracting the
allocation matrix from the maximum. The resulting matrix
is stored in need.

Return Value
------------
None

Value Parameters
----------------
P                 integer           Number of processes
R                 integer           Number of resources
need              list              Empty list
maximum           maximum list      list of maximum values
allocation        allocation list   list of allocation values

*************************************************************"""

def calculateNeed(P, R, need, maximum, allocation): 
  
    # Calculate the need values
    # Iterate maximum/allocation and subtract values
    for i in range(P): 
        for j in range(R): 
              
            # Need Matrix = Maximum Matrix - Allocated Matrix
            need[i][j] = maximum[i][j] - allocation[i][j]

"""*************************************************************

Safe State Function

This function determines if the system is in a safe state and
whether or not the request can be granted. If found is True, the
system displays that the request can be granted.

Return Value
------------
Bool              The function returns true or false

Value Parameters
----------------
P                 integer           Number of processes
R                 integer           Number of resources
avail             list              Available vectors list
maxm              maximum list      List of maximum values
allot             allocation list   List of allocation values
request           dictionary        Dictionary with request key/value

Local Variables
---------------
ch                character         Character for printed matrix labels
need              list              Empty list (filled in calculateNeed)
column            list              Where column labels are stored
row               string            Concatenation of row label/list values
increment         integer           Incrementing number for row labels
finish            list              List to determine process completion
safeSeq           list              List to store safe sequence
work              list              Copy of available vector list
count             integer           Generic incrementing number
found             boolean           Boolean to determine if process is finished
requestAvail      boolean           Boolean to determine if request is granted
difference        list              Resulting list of available - requested

*************************************************************"""

def isSafe(P, R, avail, maxm, allot, request):

    # Create an empty Need matrix of size PxR
    need = [] 
    for i in range(P): 
        l = [] 
        for j in range(R): 
            l.append(0) 
        need.append(l) 
          
    # Calculate Need matrix via calculateNeed function  
    calculateNeed(P, R, need, maxm, allot)

    # Print Need matrix with column/row labels
    print("\nThe Need Matrix is...")
    ch = 'A'
    column = ['   ']
    for x in range(len(need[0])):
        x = chr(ord(ch) + x)
        x = x + ' '
        column.append(x)
    print(''.join(column))
    
    increment = 0
    for x in range(len(need)):
        row = str(increment) + ': '
        increment = increment + 1
        print(row, end = '')
        print(*need[x], sep=' ')
  
    # Empty array to determine process completion 
    finish = [0] * P
      
    # Empty array to store safe sequence  
    safeSeq = [0] * P  
  
    # Create a copy of available vectors list, Work 
    work = [0] * R
    for i in range(R): 
        work[i] = avail[i]

    # Print Available Vectors with column/row labels
    print("\nThe Available Vector is...")
    ch = 'A'
    column = ['']
    for x in range(len(avail)):
        x = chr(ord(ch) + x)
        x = x + ' '
        column.append(x)
    print(''.join(column))

    for x in range(len(avail)):
        print(avail[x], end=' ')
  
    # While all processes are not finished, the system is NOT in safe mode
    # Create variable to increment
    count = 0
    while (count < P): 
          
        # Find a process that is not finished and needs to be satisfied
        # Create boolean value to deterine if all processes have been satisfied
        found = False
        for p in range(P):  
          
            # Determine if a process is finished  
            # if no, go for next condition  
            if (finish[p] == 0):  
              
                # Check if for all resource, values of Need matrix
                # are greater than those of Work matrix
                for j in range(R): 
                    if (need[p][j] > work[j]): 
                        break
                      
                # Check if all needs of P are satisfied
                if (j == R - 1):  
                  
                    # Add the allocated resources of P to Available resources 
                    for k in range(R):  
                        work[k] += allot[p][k]  
  
                    # Add this process to safe sequence list  
                    safeSeq[count] = p 
                    count += 1
  
                    # Determine that this P is finished  
                    finish[p] = 1
  
                    found = True
                  
        # If we could not find a next process, then
        # the system is not in a safe state
        if (found == False): 
            print("\n\nTHE SYSTEM IS NOT IN A SAFE STATE!") 
            return False
          
    # If system is in safe state then allow request to be granted 
    print("\n\nTHE SYSTEM IS IN A SAFE STATE!")
    print("\nThe Request Vector is...")

    # Extract the Request list from dictionary
    # Print request list with column/row label
    value = request["1"]
    ch = 'A'
    column = ['   ']
    for x in range(len(value)):
        x = chr(ord(ch) + x)
        x = x + ' '
        column.append(x)
    print(''.join(column))
    
    increment = 0
    for x in range(len(r_dict)):
        row = str(increment) + ':'
        increment = increment + 1
        print(row, end = ' ')
    
    for x in range(len(value)):
            print(value[x], end=' ')

    # Calculate difference of Available and Requested
    difference = []
    requestAvail = True
    for x in range(R):
        num = avail[x] - value[x]
        difference.append(num)
        if(num<0):
            requestAvail = False
            break

    # Display that request is granted and
    # Display new Available vector with column/row labels
    if(requestAvail):
        print("\n\nTHE REQUEST CAN BE GRANTED")
        print("\nThe Available Vector is...")
        ch = 'A'
        column = ['']
        for x in range(len(difference)):
            x = chr(ord(ch) + x)
            x = x + ' '
            column.append(x)
        print(''.join(column))

        for x in range(len(avail)):
            print(difference[x], end=' ')

    # Display that request cannont be granted
    else:
        print("\n\nTHE REQUEST CANNOT BE GRANTED")
  
    return True

"""*************************************************************

Main Function

This function extracts information from the file listed in the
command line argument. It intializes matrices and dictionaries, as
well as stores important values into variables.

Return Value
------------
None

Local Variables
---------------
filename          string            Name of file
ch                character         Character for printed matrix labels
need              list              Empty list (filled in calculateNeed)
column            list              Where column labels are stored
row               string            Concatenation of row label/list values
increment         integer           Incrementing number for row labels
available         list              Available vectors list
maximum           maximum list      List of maximum values
allocation        allocation list   List of allocation values
r_dict            dictionary        Dictionary with request key/value
key               string            Key value for dictionary
value             list              List containing request vectors(s)
split             list              List of split values from request
request           list              List containing request values/key from file

*************************************************************"""

if __name__ == "__main__":
    
    # Open input file to be read as determined by command line input
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        f = file.read()

    # Iterate through file and store values/matrices into variables
    f = f.split("\n\n")
    f = [lines.split('\n') for lines in f]

    P = int(''.join(f[0]))
    R = int(''.join(f[1]))

    # Split matrix strings and convert them to integer values
    matrixInitialize(f[2])
    matrixInitialize(f[3])
    matrixInitialize(f[4])

    # Assign each matrix/vector a variable to be used
    allocation = f[2]
    maximum = f[3]
    available = f[4]
    request = f[5]

    # Display process/request information extracted from file
    print("There are " + str(P) + " processes in the system.")
    print("\nThere are " + str(R) + " resource types.")

    # Display allocation matrix extracted from file
    # with column/row labels
    print("\nThe Allocation Matrix is...")
    ch = 'A'
    column = ['   ']
    for x in range(len(allocation[0])):
        x = chr(ord(ch) + x)
        x = x + ' '
        column.append(x)
    print(''.join(column))

    increment = 0
    for x in range(len(allocation)):
        row = str(increment) + ': '
        increment = increment + 1
        print(row, end = '')
        print(*allocation[x], sep=' ')

    # Display maximum matrix extracted from file
    # with column/row labels
    print("\nThe Max Matrix is...")
    ch = 'A'
    column = ['   ']
    for x in range(len(maximum[0])):
        x = chr(ord(ch) + x)
        x = x + ' '
        column.append(x)
    print(''.join(column))

    increment = 0
    for x in range(len(maximum)):
        row = str(increment) + ': '
        increment = increment + 1
        print(row, end = '')
        print(*maximum[x], sep=' ')

    # Create dictionary for Request key/value
    key = f[5][0][0]
    value = f[5][0][2:]
    split = value.split()
    for x in range(len(split)):
        split[x] = int(split[x])
    r_dict = {key: split}

    # Check system is in safe state or not  
    isSafe(P, R, available[0], maximum, allocation, r_dict) 
