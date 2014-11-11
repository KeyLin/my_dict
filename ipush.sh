#!/bin/bash

git add --all
echo $1
msg="'"$1"'"
echo $msg
if [ $1 ]; then
	git commit -m msg
else
	git commit -m 'default'
fi
git push