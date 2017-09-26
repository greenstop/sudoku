#!/Users/jason/anaconda3/envs/aind/bin/python
# -*- coding: utf-8 -*-
"""
Solutions
"""
import re, sys

def cross(str_a, str_b):
    """
    Cross product of elements in A and elements in B."""
    return [s+t for s in str_a for t in str_b];

#Global Constants
assignments = []
rows = 'ABCDEFGHI';
cols = '123456789';
boxes = cross( rows, cols);
row_units = [ cross(r, cols) for r in rows ];
column_units  =  [ cross(rows, c) for c in cols ];
square_units =  [ cross( rs, cs) for rs in ( 'ABC', 'DEF', 'GHI' )
                  for cs in ( '123', '456', '789')];
diagonal_units = [[ "%s%d"%("ABCDEFGHI"[x-1],x*z+y) for x in range(1,10)] for y,z in ((0,1),(10,-1))]
unitlist = row_units + column_units + square_units + diagonal_units
peers = { b:set(sum([ list(set(u)-{b}) for u in unitlist if b in u],[])) for b in boxes }

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        #collate 2 digits values
        pattern=re.compile(r'^\d{2}$');
        duodigits=[ values[box] for box in unit if pattern.match(values[box])];
        if duodigits:
            #count them
            freq={ v:0 for v in duodigits };
            for v in duodigits: freq[v]+=1;
            #eliminite values in unit not a twin
            for twin in [ v for v in freq if freq[v] == 2 ]:
                for c in twin: #each char in twin
                    for box in unit:
                        if values[box] != twin and c in values[box]:
                            assign_value(values,box,
                                         values[box].replace(c,'')
                                        );
    return values;

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    gridmap = {boxes[i]:grid[i] for i in range(len(boxes))};
    for k in gridmap:
        if gridmap[k] == '.': gridmap[k]='123456789';
    return gridmap

def display(values):
    '''
    Purpose: Pretty print sudoku map
    Args: map of sudoku
    Returns: none
    '''
    if values is False:
        print("No Solution");
        return False;
    width=max({len(values[k]) for k in values})
    sys.stdout.write(" _ ");
    for i in range(1,10):
        sys.stdout.write("%s%d "%("_"*(width-1),i));
        if i in (3,6): sys.stdout.write("_ ");
    sys.stdout.write("\n");
    for k,v in values.items():
        if k[1] is '1': sys.stdout.write("%s| " % (k[0]));
        sys.stdout.write("%*d " % (width,int(v)));
        if k[1] in ('3','6'): sys.stdout.write("| ");
        if k[1] is '9':
            sys.stdout.write("\n");
            if k[0] in "CF":
                dash="-"*(3*width+3)
                sys.stdout.write(" | %s+ %s+ %s\n"%(dash,dash,dash));
    sys.stdout.write(" ` ");
    for i in range(1,10):
        sys.stdout.write("%s%d "%("`"*(width-1),i));
        if i in (3,6): sys.stdout.write("` ");
    sys.stdout.write("\n");

def eliminate(values):
    '''
    Purpose.
        eliminate duplicates in peer group
    Args:
        values (dict): values in the sudoku puzzle
    Returns:
        sudoku values in map form
    '''
    #start
    pattern=re.compile(r"^\d$");
    for key in values:
        if not pattern.match(values[key]): continue;
        current_value = values[key];
        for unit in unitlist:
            if key in unit:
                for unitkey in unit:
                    if unitkey != key:
                        assign_value(values,unitkey,
                                     values[unitkey].replace(current_value,'')
                                    );
    return values;

def only_choice(values):
    '''
    Purpose.
        assign value if unique
    Args:
        map of sudoku
    Returns:
        map of sudoku
    '''
    pattern=re.compile(r'^\d$');
    for unit in unitlist:
        numbers = { str(k):0 for k in range(1,10) };
        for k in numbers:
            for box in unit:
                if k in values[box]:
                    numbers[k]+=1;
        choices=[ k for k,v in numbers.items() if v==1];
        for choice in choices:
            for box in unit:
                if pattern.match(values[box]): continue;
                if choice in values[box]:
                    assign_value(values,box,choice);
    return values;

def reduce_puzzle(values):
    '''
    Purpose: apply constraint propagation until stalled
    Args: map
    Returns: reduced map
    '''
    stalled=False;
    while not stalled:
        pre=0;
        post=0;
        for box in values:
            if len(values[box]) == 1: pre += 1;
        eliminate(values);
        only_choice(values);
        naked_twins(values);
        for box in values:
            if len(values[box]) == 1: post += 1;
        if pre == post: stalled = True;
    return values;

def checkDictforNoNulls(values):
    '''
    Purpose.
    Args:
    Returns:
    '''
    for box in values:
        if len(values[box]) is 0:
            return False;
    return True;

def checkifSolved(values):
    '''
    Purpose.
    Args:
    Returns:
    '''
    for box in values:
        if len(values[box]) is not 1:
            return False;
    return True;

def search(values):
    '''
    Purpose. search
    Args:
    Returns:
    '''
    reduce_puzzle(values);
    if checkifSolved(values) is True: return values;
    if checkDictforNoNulls(values) is False: return False;
    searchset=[ (len(v),k) for k,v in values.items() if len(v) > 1 ];
    box=min(searchset)[1];
    for c in values[box]:
        assign_value(values,box,c);
        result=search({ k:v for k,v in values.items() });
        if result:
            return result;

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    gridmap = grid_values(grid);
    values=search(gridmap);
    if values: return values;
    else: return False;

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    solution=solve(diag_sudoku_grid)
    display(solution);

    try:
        #pass
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
