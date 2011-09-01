#!/bin/sh

TESTDIR="./tests"
DATADIR="data"
TEMPDIR="data_tmp"

echo Removing temporary test data
cd $TESTDIR
rm -Rv $TEMPDIR
