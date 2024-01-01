% base cases
valid_puzzle([], [], _).
valid_puzzle([_], [], _).

% recursive case
valid_puzzle(List, Sequence, Removed) :- 
    select(X, List, Rest),

    % Block breakdown:
    % Use select, predicated on two criteria this time:
    % A. removed number is +/- 1 from previous number.
    % B. removed number is not found in Removed list.
    % If passed, make a recursive call.
    % Finally, back-propagate using append to build the sequence.

    % 'Y' block:
    (   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), 
        \+ member(Y, Removed),
        valid_puzzle(NewRest, SubSequence, [X|Removed]), 
        append([Y|SubSequence], [X], Sequence)

    % 'X' block:
    ;   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), 
        \+ member(X, Removed),
        valid_puzzle(NewRest, SubSequence, [Y|Removed]), 
        append([X|SubSequence], [Y], Sequence)
    ).

valid_puzzle(List, Sequence) :- valid_puzzle(List, Sequence, []).