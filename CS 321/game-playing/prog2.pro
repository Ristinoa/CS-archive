partition([], _, [], []).

partition([Head | Tail], Value, [Head | Tail1], List2) :- 
    Head < Value, partition(Tail, Value, Tail1, List2).

partition([Head | Tail], Value,
            List1, [Head | Tail2]) :-
            Head > Value,
            partition(Tail, Value, List1, Tail2). 
        
median(List, M) :-
    append(Left, [M | Right], List),
    append(Left, Right, WithoutM),
    partition(WithoutM, M, A, B),
    length(A, L1),
    length(B, L2),
    L1 =:= L2.


% base case for empty list (to avoid infinite recursion)
valid_puzzle([]).
% base case for list with one item (always valid)
valid_puzzle([_]).
% recursive case:
valid_puzzle(List) :-
    select(X, List, Rest),
    (   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), valid_puzzle([Y|NewRest])
    ;   select(Y, Rest, NewRest), (Y is X-1 ; Y is X+1), valid_puzzle([X|NewRest])
    ).

