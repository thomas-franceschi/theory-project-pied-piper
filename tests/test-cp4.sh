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

if [ -x $SUBMIT/parse_program ]; then
  for REGEXP in "(ab|a)*" "" "a" "@" "a*" "ab" "a|b" "a*b*" "(ab)*" "ab|cd" "(ab)|(cd)" "a*|b*" "(a|b)*" "(a)" "((a))" "()" "|" "(|)"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    test $($BIN/parse_program "$REGEXP") = $($SUBMIT/parse_program "$REGEXP")
    assert_true
  done
  for REGEXP in "a:b" "ab:cd" "a|b:c|d" "(a:b)(c:d)" "(a:b)|(c:d)" ":"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    test $($BIN/parse_program "$REGEXP") = $($SUBMIT/parse_program "$REGEXP")
    assert_true
  done
  for REGEXP in "a:b;c:d" "{a:b};{c:d}"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    diff -q <($BIN/parse_program "$REGEXP")  <($SUBMIT/parse_program "$REGEXP")
    assert_true
  done
else
  echo "parse_program: SKIPPED"
fi

if [ -x $SUBMIT/mire ]; then
  echo -n 'mire "(0|1)*(0:1)(1:0)*": '
  cat <<EOF >$TMPDIR/input
000
001
010
011
100
101
110
EOF
  diff <($BIN/mire "(0|1)*(0:1)(1:0)*" <$TMPDIR/input) <($SUBMIT/mire "(0|1)*(0:1)(1:0)*" <$TMPDIR/input)
  assert_true

  echo -n 'mire "(1(1:))*": '
  cat <<EOF >$TMPDIR/input

1
11
111
1111
11111
111111
1111111
11111111
EOF
  diff <($BIN/mire "(1(1:))*" <$TMPDIR/input) <($SUBMIT/mire "(1(1:))*" <$TMPDIR/input)
  assert_true

  echo -n 'mire "(1(1:))*;(1(1:))*": '
  cat <<EOF >$TMPDIR/input

1
11
111
1111
11111
111111
1111111
11111111
EOF
  diff <($BIN/mire "(1(1:))*;(1(1:))*" <$TMPDIR/input) <($SUBMIT/mire "(1(1:))*;(1(1:))*" <$TMPDIR/input)
  assert_true

  echo -n 'mire "{(1(1:))*};1": '
  cat <<EOF >$TMPDIR/input
1
11
111
1111
11111
111111
1111111
11111111
EOF
  diff <($BIN/mire "{(1(1:))*};1" <$TMPDIR/input) <($SUBMIT/mire "{(1(1:))*};1" <$TMPDIR/input)
  assert_true
fi