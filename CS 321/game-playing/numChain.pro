% To run in swipl:
% solve(final),show(final).
% Has singleton variable warning (works anyways).
% Will print multiple solutions. 
% See first solution printed for desired output.
% It takes a second (or ten, but not a minute).

board_size(9).

init(2,3,46).
init(2,4,45).
init(2,6,55).
init(2,7,74).
init(3,2,38).
init(3,5,43).
init(3,8,78).
init(4,2,35).
init(4,8,71).
init(5,3,33).
init(5,7,59).
init(6,2,17).
init(6,8,67).
init(7,2,18).
init(7,8,64).
init(8,3,24).
init(8,4,21).
%init(8,6,1).
init(8,7,2).

show(Soln) :-
    reverse(Soln, Forwards),
    write('\n'),
    member(Row, [1,2,3,4,5,6,7,8,9]),
    write('\n'),
    member(Col, [1,2,3,4,5,6,7,8,9]),
    nth1(Value, Forwards, [Row, Col]),
    write(Value),
    write('\t'),
    fail. 

% Neighbor above
adjacent(A,B,X,Y):-
    A > 1,
    X is A-1,
    Y is B.

% Neighbor below
adjacent(A,B,X,Y):-
    board_size(S),
    A < S,
    X is A+1,
    Y is B.

% Neighbor right
adjacent(A,B,X,Y):-
    board_size(S),
    B < S,
    X is A,
    Y is B+1.

% Neighbor left  
adjacent(A,B,X,Y):-
    A > 1,
    X is A,
    Y is B-1.

% solution list helper method
sol_list(1, [1]).
sol_list(I, [I|T]) :-
    I > 1,
    I1 is I-1,
    sol_list(I1, T).

solve(Final):-
    board_size(N),
    sol_list(N,L),
    % check if 1 is initialized on the board
    (init(A,B,1) ->
        % if it is, add it to the partial solution and continue
        complete([[A,B]],Final);
        % if it's not, iterate through all possible starting points
        findall(Partial, (member(A,L), member(B,L), \+ init(A,B,_), complete([[A,B]], Partial)), Partials),
        member(Final, Partials)).

% Recursive base case 
complete(Partial, Partial):-
    board_size(N),
    length(Partial,L),
    % if the below assertion is true, solution has been reached
    L is N*N.


% Case for encountering tiles initialized with numbers
complete(Partial,Finished):-
    Partial = [[X,Y]|T],
    adjacent(X,Y,A,B),
    not(member([A,B],Partial)),
    % check \/ for initialized value
    init(A,B,Value),
    length(Partial,ParLen),
    % length of list adjusted
    Value is ParLen+1,
    % initialized cell placed into correct slot in solution
    complete([[A,B]|Partial],Finished).

% Case for encountering tiles NOT initilized with numbers
complete(Partial, Finished):-
    Partial = [[X,Y]|T],
    adjacent(X,Y,A,B),
    not(member([A,B],Partial)),
    not(init(A,B,Value)),
    length(Partial, ParLen),
    V is ParLen+1,
    % assert next value up is not already in solution
    not(init(W, Z, V)),
    complete([[A,B]|Partial], Finished).


