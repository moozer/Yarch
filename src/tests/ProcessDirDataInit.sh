#!/bin/sh

TESTDIR="./tests"
DATADIR="data"
TEMPDIR="data_tmp"

echo Initialising test data
cd $TESTDIR
mkdir $TEMPDIR
cd $DATADIR
tar cf - * --exclude=\.svn | (cd ../$TEMPDIR; tar xvf -)
