CS 321 A* Search project

Given the two heuristics, manhattan distance's tests took far less time to complete than
did the num_wrong_tiles tests. This is unsurprising as the manhattan distance is a much
stronger heuristic and a better indicator of proximity to solution than simply listing off
the number of off tiles, which is apparent given the outcome of the test case results.

When compared with the itdeep variant of this problem, given the small 'world' size, a 3x3 grid, the performance 
difference isn't noticeable, really (anywhere between 1 - 2 seconds difference). Though, it should be noted that 
itdeep beats a* searched when a* is being used used with the weaker heurisitic, number of wrong tiles, which I 
found to be interesting. 