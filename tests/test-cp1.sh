#!/bin/bash

ROOT="$(cd "$(dirname $0)" && pwd)"/..
BIN=$ROOT/bin
SUBMIT=$ROOT/cp1
EXAMPLES=$ROOT/examples
TMPDIR=${TMPDIR:-/tmp}/test-cp1.$$
mkdir -p $TMPDIR
cleanup() { 
  rm -rf $TMPDIR 
}
trap cleanup EXIT

assert_true () {
  if [ $? -eq 0 ]; then
    echo PASSED
  else
    echo FAILED
  fi
}

assert_false () {
  if [ $? -eq 1 ]; then
    echo PASSED
  else
    echo FAILED
  fi
}

if [ -x $SUBMIT/singleton_nfa ]; then
  for STRING in "aba" ""; do
    echo -n 'singleton_nfa "'$STRING'": '
    $BIN/compare_nfa <($BIN/singleton_nfa "$STRING") <($SUBMIT/singleton_nfa "$STRING") >/dev/null
    assert_true
  done

else
  echo "singleton_nfa: SKIPPED"
fi

if [ -x $SUBMIT/empty_nfa ]; then
  for NFA in $EXAMPLES/sipser-n{1,2,3,4}.nfa $EXAMPLES/nonempty1.nfa; do
    echo -n "empty_nfa $(basename $NFA): "
    $SUBMIT/empty_nfa $NFA >/dev/null
    assert_false
  done

  for NFA in $EXAMPLES/empty{1,2}.nfa; do
    echo -n "empty_nfa $(basename $NFA): "
    $SUBMIT/empty_nfa $NFA >/dev/null
    assert_true
  done

else
  echo "empty_nfa: SKIPPED"
fi

if [ -x $SUBMIT/intersect_nfa ]; then
  for NFA1 in $EXAMPLES/sipser-n{1,2,3,4}.nfa; do
    for NFA2 in $EXAMPLES/sipser-n{1,2,3,4}.nfa; do

      echo -n "intersect_nfa $(basename $NFA1) $(basename $NFA2): "
      $BIN/compare_nfa <($BIN/intersect_nfa $NFA1 $NFA2) <($SUBMIT/intersect_nfa $NFA1 $NFA2) >/dev/null
      assert_true
    done
  done

else
  echo "intersect_nfa: SKIPPED"
fi

if [ -x $SUBMIT/run_nfa ]; then
  echo -n 'run_nfa sipser-n1.nfa: '
  cat <<EOF >$TMPDIR/input
010110
010
EOF
  diff <($BIN/run_nfa $EXAMPLES/sipser-n1.nfa <$TMPDIR/input) <($SUBMIT/run_nfa $EXAMPLES/sipser-n1.nfa <$TMPDIR/input)
assert_true

  echo -n 'run_nfa sipser-n3.nfa: '
  cat <<EOF >$TMPDIR/input

0
00
000
0000
00000
000000
EOF
  diff <($BIN/run_nfa $EXAMPLES/sipser-n3.nfa <$TMPDIR/input) <($SUBMIT/run_nfa $EXAMPLES/sipser-n3.nfa <$TMPDIR/input)
  assert_true

  echo -n 'run_nfa sipser-n4.nfa: '
  cat <<EOF >$TMPDIR/input

a
baba
baa
b
bb
babba
EOF
  diff <($BIN/run_nfa $EXAMPLES/sipser-n4.nfa <$TMPDIR/input) <($SUBMIT/run_nfa $EXAMPLES/sipser-n4.nfa <$TMPDIR/input)
  assert_true

else
  echo "run_nfa: SKIPPED"
fi
