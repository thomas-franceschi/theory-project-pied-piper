#!/bin/bash

ROOT="$(cd "$(dirname $0)" && pwd)"/..
BIN=$ROOT/bin
SUBMIT=$ROOT/cp3
EXAMPLES=$ROOT/examples
TMPDIR=${TMPDIR:-/tmp}/test-cp3.$$
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

assert_true_or_maybe () {
  RES=$?
  if [ $RES -eq 0 ]; then
    echo PASSED
  elif [ $RES -eq 1 ]; then
    echo UNKNOWN
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

if [ -x $SUBMIT/parse_rte ]; then
  for REGEXP in "(ab|a)*" "" "a" "@" "a*" "ab" "a|b" "a*b*" "(ab)*" "ab|cd" "(ab)|(cd)" "a*|b*" "(a|b)*" "(a)" "((a))" "()" "|" "(|)"; do
    echo -n 'parse_rte "'"$REGEXP"'": '
    test $($BIN/parse_rte "$REGEXP") = $($SUBMIT/parse_rte "$REGEXP")
    assert_true
  done
  for REGEXP in "a:b" "ab:cd" "a|b:c|d" "(a:b)(c:d)" "(a:b)|(c:d)" ":"; do
    echo -n 'parse_rte "'"$REGEXP"'": '
    test $($BIN/parse_rte "$REGEXP") = $($SUBMIT/parse_rte "$REGEXP")
    assert_true
  done
else
  echo "parse_rte: SKIPPED"
fi

if [ -x $SUBMIT/singleton_nft ]; then
  for STRING in "aba" ""; do
    echo -n 'singleton_nft "'$STRING'": '
    $BIN/compare_nft <($BIN/singleton_nft "$STRING") <($SUBMIT/singleton_nft "$STRING") >/dev/null
    assert_true_or_maybe
  done
else
  echo "singleton_nft: SKIPPED"
fi

NFTS=$(echo $EXAMPLES/{sipser-t1,sipser-t2,increment,double,halve}.nft)

# Optional tests
for OP in union concat; do
  if [ -x $SUBMIT/${OP}_nft ]; then
    for NFA1 in $NFTS; do
      for NFA2 in $NFTS; do
        echo -n "${OP}_nft $(basename $NFA1) $(basename $NFA2): "
        $BIN/compare_nft <($BIN/${OP}_nft $NFA1 $NFA2) <($SUBMIT/${OP}_nft $NFA1 $NFA2) >/dev/null
        assert_true_or_maybe
      done
    done
  fi
done

if [ -x $SUBMIT/star_nft ]; then
  for NFA in $NFTS; do
    echo -n "star_nft $(basename $NFA): "
    $BIN/compare_nft <($BIN/star_nft $NFA) <($SUBMIT/star_nft $NFA) >/dev/null
    assert_true_or_maybe
  done
fi

for OP in transduce compose; do
  if [ -x $SUBMIT/${OP}_nft ]; then
    for NFA1 in $NFTS; do
      for NFA2 in $NFTS; do
        echo -n "${OP}_nft $(basename $NFA1) $(basename $NFA2): "
        $BIN/compare_nft <($BIN/${OP}_nft $NFA1 $NFA2) <($SUBMIT/${OP}_nft $NFA1 $NFA2) >/dev/null
        assert_true_or_maybe
      done
    done
  else
    echo "${OP}_nft: SKIPPED"
  fi
done

if [ -x $SUBMIT/output_nft ]; then
    # Run the example NFTs on example inputs, and use output_nft to get an output.
    # The NFT must have a unique output for this test to work.

    for W in "2212011" "011" "211" "121" "0202"; do
      $BIN/compose_nft <($BIN/singleton_nft "$W") $EXAMPLES/sipser-t1.nft >$TMPDIR/composed
      echo -n "run sipser-t1.nft on \"$W\": "
      test "$($BIN/output_nft $TMPDIR/composed)" = "$($SUBMIT/output_nft $TMPDIR/composed)"
      assert_true
    done

    for W in "abbb" "b" "bbab" "bbbbbb" ""; do
      $BIN/compose_nft <($BIN/singleton_nft "$W") $EXAMPLES/sipser-t2.nft >$TMPDIR/composed
      echo -n "run sipser-t2.nft on \"$W\": "
      test "$($BIN/output_nft $TMPDIR/composed)" = "$($SUBMIT/output_nft $TMPDIR/composed)"
      assert_true
    done

else
    echo "output_nft: SKIPPED"
fi

if [ -x $SUBMIT/more ]; then

  for EXPR in "0:1" "(0:1)|(1:0)" "((0:1)|(1:0))*"; do
    echo -n "more \"$EXPR\": "
    cat <<EOF >$TMPDIR/input
0
1
000
101
EOF
    diff <($BIN/more "$EXPR" <$TMPDIR/input) <($SUBMIT/more "$EXPR" <$TMPDIR/input)
    assert_true
  done
  
  echo -n 'more "(0|1)*(0:1)(1:0)*": '
  cat <<EOF >$TMPDIR/input
000
001
010
011
100
101
110
EOF
  diff <($BIN/more "(0|1)*(0:1)(1:0)*" <$TMPDIR/input) <($SUBMIT/more "(0|1)*(0:1)(1:0)*" <$TMPDIR/input)
  assert_true

  echo -n 'more "(1(1:))*": '
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
  diff <($BIN/more "(1(1:))*" <$TMPDIR/input) <($SUBMIT/more "(1(1:))*" <$TMPDIR/input)
  assert_true

else
  echo "more: SKIPPED"
fi
