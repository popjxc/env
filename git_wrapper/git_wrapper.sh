#!/bin/bash

git=/usr/bin/git

$git config --global push.default current

. ~/.git_wrapper
base_branch=master

if [[ $master == *$PWD* ]]; then
  base_branch=master
fi

if [[ $develop == *$PWD* ]]; then
  base_branch=develop
fi

echo "==== Base git branch: [$base_branch] ===="

case "$1" in
    "newb")
        if [ -z $2 ]
        then
            echo "git <base_branch> newb <branch_name>"
            exit 1
        fi
        $git checkout $base_branch
        $git pull
        $git branch feature/$2
        $git checkout feature/$2
        $git branch
        ;;
    "delb")
        $git checkout $base_branch
        $git pull
        branchs=(`$git branch | tr "*" "\n"`)
        for b in "${branchs[@]}"
        do
            if [ $b != $base_branch -a $b != 'master' ]
            then
                $git branch -d $b
            fi
        done
        $git branch
        ;;
    *)
        $git $@
        ;;
esac
