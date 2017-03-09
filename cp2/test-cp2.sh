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

if [ -x $SUBMIT/parse_re ]; then
  for REGEXP in "(ab|a)*" "(a|b)*aba" "" "a" "@" "a*" "ab" "a|b" "a*b*" "(ab)*" "ab|cd" "(ab)|(cd)" "a*|b*" "(a|b)*" "(a)" "((a))" "()" "|" "(|)"; do
    echo -n 'parse_re "'"$REGEXP"'": '
    test $($BIN/parse_re "$REGEXP") = $($SUBMIT/parse_re "$REGEXP")
    assert_true
  done
else
  echo "parse_re: SKIPPED"
fi

for OP in union concat; do
  if [ -x $SUBMIT/${OP}_nfa ]; then
    for NFA1 in $EXAMPLES/sipser-n{1,2,3,4}.nfa; do
      for NFA2 in $EXAMPLES/sipser-n{1,2,3,4}.nfa; do

        echo -n "${OP}_nfa $(basename $NFA1) $(basename $NFA2): "
        $BIN/compare_nfa <($BIN/${OP}_nfa $NFA1 $NFA2) <($SUBMIT/${OP}_nfa $NFA1 $NFA2) >/dev/null
        assert_true
      done
    done
  else
    echo "${OP}_nfa: SKIPPED"
  fi
done

if [ -x $SUBMIT/star_nfa ]; then
  for NFA in $EXAMPLES/sipser-n{1,2,3,4}.nfa; do
    echo -n "star_nfa $(basename $NFA): "
    $BIN/compare_nfa <($BIN/star_nfa $NFA) <($SUBMIT/star_nfa $NFA) >/dev/null
    assert_true
  done
else
  echo "star_nfa: SKIPPED"
fi

if [ -x $SUBMIT/mere ]; then
  echo -n 'mere "(ab|a)*": '
  cat <<EOF >$TMPDIR/input

a
b
aa
ab
ba
bb
aaa
aab
aba
abb
baa
bab
bba
bbb
EOF
  diff <($BIN/mere "(ab|a)*" <$TMPDIR/input) <($SUBMIT/mere "(ab|a)*" <$TMPDIR/input)
  assert_true

  echo -n 'mere "(a|b)*aba": '
  cat <<EOF >$TMPDIR/input

a
b
aa
ab
ba
bb
aba
abaa
abab
aaba
baba
aaaba
ababa
baaba
bbaba
EOF
  diff <($BIN/mere "(a|b)*aba" <$TMPDIR/input) <($SUBMIT/mere "(a|b)*aba" <$TMPDIR/input)
  assert_true

  echo -n 'mere "": '
  cat <<EOF >$TMPDIR/input

a
EOF
  diff <($BIN/mere "" <$TMPDIR/input) <($SUBMIT/mere "" <$TMPDIR/input)
  assert_true

  echo -n 'mere "@": '
  cat <<EOF >$TMPDIR/input

a
EOF
  diff <($BIN/mere "@" <$TMPDIR/input) <($SUBMIT/mere "@" <$TMPDIR/input)
  assert_true

else
  echo "mere: SKIPPED"
fi
