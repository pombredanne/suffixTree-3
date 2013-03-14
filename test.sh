#!/bin/bash
prog="SuffixTree.py"
function test_correctness {
    if [[ $# == 0 ]]
    then
      testString="mississippi"
    else
      testString="$1"
    fi

    ./"$prog" -s $testString 

    dot -Tpng -O sty.dot
    open sty.dot.png
}

function plot {
#  aaa='mississipi#ssi$'
  javac ST.java
  echo 'mississipi#ssi$' | java ST
  dot -Tpng -O st.dot
  open st.dot.png
   "./$prog" -s -s 'mississipi#ssi$'
  dot -Tpng -O sty.dot
  open sty.dot.png

}
function test_findLongestStr(){
  "./$prog" -s missi ssi
  "./$prog" -s abchfefg ebcdabcefg
  "./$prog" -s mississipi  asssiasdf 
  "./$prog" -f Seq Seq2 
#    dot -Tpng -O sty.dot
#    open sty.dot.png

}

function test_substring {

 "./$prog" -s mississipi -q ssi
 "./$prog" -s mississipi -q asi
 "./$prog" -s mississipi -q 1234
 "./$prog" -s mississipi -q mississipi
 "./$prog" -s mississipi -q mississippi
}

function increase_size {
  tr -d '[ \n\t#$]' <SuffixTree.py >testfile
  echo now the size of testfile is: `awk '{print length()}' <testfile`
  for i in `jot - 1 7`
  do
      cat testfile >tmp
      cat tmp >>testfile
  done
  tr -d '[ \n\t#$]'  <testfile >tmp
  mv tmp testfile
  echo now the size of testfile is: `awk '{print length()}' <testfile`
}

function test_size {

  testdir="testdir"
  if [[ -d "$testdir" ]]
  then
      rm -rf "$testdir"
      mkdir "$testdir"
  else
      mkdir "$testdir"
  fi

  result="result"
  if [[ -f "$result" ]]
  then
      rm -f "$result"
  fi

  for i in `jot - 1 1000001 5000`;
#  for i in `jot - 1 5 1`;
  do
      filename=c"$i"
#      echo  cut -c1-"$i" testfile
      cut -c1-"$i" testfile >"$testdir/$filename"
     "./$prog" -f "$testdir/$filename" -r 2>>"$result"
  done
}

#test_correctness $*
#test_findLongestStr
#plot
#test_substring
#increase_size
test_size
