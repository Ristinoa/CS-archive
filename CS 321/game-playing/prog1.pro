prereq(introCS,dataStructs).
prereq(dataStructs,progLangs).
prereq(dataStructs,graphics).
prereq(linAlg,graphics).

 required(Course, NextCourse) :-
         prereq(Course, NextCourse).

     required(Course,NextCourse) :-
         required(SomeOtherCourse, NextCourse),
         prereq(Course, SomeOtherCourse).
