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
  for REGEXP in "a//comment" " a " " a //comment"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    diff -q <($BIN/parse_program "$REGEXP")  <($SUBMIT/parse_program "$REGEXP")
    assert_true
  done
  for FILE in log2a.mire log2u.mire log2b.mire factor.mire; do
    echo -n "parse_program -f $FILE: "
    diff -q <($BIN/parse_program -f $EXAMPLES/$FILE) <($SUBMIT/parse_program -f $EXAMPLES/$FILE)
    assert_true
  done
  for REGEXP in "(ab|a)*" "" "a" "@" "a*" "ab" "a|b" "a*b*" "(ab)*" "ab|cd" "(ab)|(cd)" "a*|b*" "(a|b)*" "(a)" "((a))" "()" "|" "(|)"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    diff -q <($BIN/parse_program "$REGEXP") <($SUBMIT/parse_program "$REGEXP")
    assert_true
  done
  for REGEXP in "a:b" "ab:cd" "a|b:c|d" "(a:b)(c:d)" "(a:b)|(c:d)" ":"; do
    echo -n 'parse_program "'"$REGEXP"'": '
    diff -q <($BIN/parse_program "$REGEXP") <($SUBMIT/parse_program "$REGEXP")
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
  cat <<EOF >$TMPDIR/input
000
001
010
011
100
101
110
111
EOF

  for REGEXP in "(0|1)*(0:1)(1:0)*" "(0:1)|(1:0);(0|1)*(0:1)(1:0)*"; do
      echo -n "mire \"$REGEXP\": "
      diff <($BIN/mire "$REGEXP" <$TMPDIR/input) <($SUBMIT/mire "$REGEXP" <$TMPDIR/input)
      assert_true
  done

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

  echo -n 'mire "{(1(1:))*};1": '
  diff <($BIN/mire "{(1(1:))*};1" <$TMPDIR/input) <($SUBMIT/mire "{(1(1:))*};1" <$TMPDIR/input)
  assert_true

  cat <<EOF >$TMPDIR/input
1
11
111
1111
EOF

  echo -n 'mire -f log2u.mire: '
  diff <($BIN/mire -f $EXAMPLES/log2u.mire <$TMPDIR/input) <($SUBMIT/mire -f $EXAMPLES/log2u.mire <$TMPDIR/input)
  assert_true

  cat <<EOF >$TMPDIR/input
1
10
11
100
101
110
111
1000
EOF

  echo -n 'mire -f log2b.mire: '
  diff <($BIN/mire -f $EXAMPLES/log2u.mire <$TMPDIR/input) <($SUBMIT/mire -f $EXAMPLES/log2u.mire <$TMPDIR/input)
  assert_true
fi
