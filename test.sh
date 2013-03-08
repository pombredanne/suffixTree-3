#!/bin/bash
if [[ $# == 0 ]]
then
  testString="mississippi"
else
  testString="$1"
fi

./ST.py -s "$testString" 

dot -Tpng -O sty.dot
open sty.dot.png


