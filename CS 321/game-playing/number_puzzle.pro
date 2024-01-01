% recursive strategy, four scenarios:
%   A. Find X - 1, perform new search on list with X - 1 removed
%   B. Find X + 1, do the same thing but with X + 1 removed
%   C. function ends up in a situation where neither X - 1 or X + 1 can be found
%   D. base case

% base cases:
valid_puzzle([]). 
valid_puzzle([_]). 

% recursive case
valid_puzzle(List) :- 

    % here's where it gets interesting:

    select(X, List, Rest),
    (   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), valid_puzzle([Y|NewRest])
    ;   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), valid_puzzle([X|NewRest])
    ).
