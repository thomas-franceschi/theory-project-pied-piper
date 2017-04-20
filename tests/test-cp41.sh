#!/bin/bash

ROOT="$(cd "$(dirname $0)" && pwd)"/..
BIN=$ROOT/bin
SUBMIT=$ROOT/cp4
EXAMPLES=$ROOT/examples
TMPDIR=${TMPDIR:-/tmp}/test-cp4.$$
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

cat <<EOF >$TMPDIR/input

a
b
aa
ab
ba
bb
aabb
abab
EOF

if [ -f $SUBMIT/reverse.mire ]; then
  echo -n "mire reverse.mire: "
  cat <<EOF >$TMPDIR/correct

a
b
aa
ba
ab
bb
bbaa
baba
EOF
  $BIN/mire -f $SUBMIT/reverse.mire <$TMPDIR/input >$TMPDIR/student
  diff $TMPDIR/correct $TMPDIR/student
  assert_true
else
  echo "reverse.mire: SKIPPED"
fi

if [ -f $SUBMIT/uncopy.mire ]; then
  echo -n "mire uncopy.mire: "
  cat <<EOF >$TMPDIR/correct

a
b
ab
EOF
  $BIN/mire -f $SUBMIT/uncopy.mire <$TMPDIR/input >$TMPDIR/student
  diff $TMPDIR/correct $TMPDIR/student
  assert_true
else
  echo "uncopy.mire: SKIPPED"
fi

if [ -f $SUBMIT/sort.mire ]; then
  echo -n "mire sort.mire: "
  cat <<EOF >$TMPDIR/correct

a
b
aa
ab
ab
bb
aabb
aabb
EOF
  $BIN/mire -f $SUBMIT/sort.mire <$TMPDIR/input >$TMPDIR/student
  diff $TMPDIR/correct $TMPDIR/student
  assert_true
else
  echo "sort.mire: SKIPPED"
fi
