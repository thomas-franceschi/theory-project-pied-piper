#!/bin/bash

ROOT="$(cd "$(dirname $0)" && pwd)"/..
BIN=$ROOT/bin
SUBMIT=$ROOT/cp2
EXAMPLES=$ROOT/examples
TMPDIR=${TMPDIR:-/tmp}/test-cp2.$$
mkdir -p $TMPDIR
cleanup() { 
  rm -rf $TMPDIR 
}
trap cleanup EXIT

echo -e "n\tperl\tours\tyours"
for N in $(seq 1 30); do
    echo "n $N" 1>&2
    R=$(perl -e "print '(a|)'x$N, 'a'x$N")
    W=$(perl -e "print 'a'x$N")
    echo $W | time -p perl -ne "print if (/^$R\$/);"
    echo $W | time -p $BIN/mere $R
    echo $W | time -p $SUBMIT/mere $R
done 2>&1 >/dev/null | perl -ne '
    BEGIN { $q = 0; }
    if ($q == 0 && /^n (.*)/) { $n = $1; $q = 1; }
    elsif ($q == 1 && /^user (.*)/) { $t1 += $1; }
    elsif ($q == 1 && /^sys (.*)/)  { $t1 += $1; $q = 2; }
    elsif ($q == 2 && /^user (.*)/) { $t2 += $1; }
    elsif ($q == 2 && /^sys (.*)/)  { $t2 += $1; $q = 3; }
    elsif ($q == 3 && /^user (.*)/) { $t3 += $1; }
    elsif ($q == 3 && /^sys (.*)/)  { $t3 += $1; $q = 0; print "$n\t$t1\t$t2\t$t3\n"; $t1 = $t2 = $t3 = 0; }
'
