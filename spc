#!/bin/bash

if [ "$1" = "config" ]; then
    if [ "$2" = "edit" ]; then
        read -p "Username: " user
        read -sp "Password: " pass
        echo ""
        read -sp "Confirm Password: " cpass
        echo ""
        if [ ! "$pass" = "$cpass" ]; then
            echo "password entered was not same"
        else
            echo $user > ./config
            echo $pass >> ./config
        fi
    fi
elif [ "$1" = "sync" ]; then
        ctr=0
        while read -r line
        do
            if [[ $ctr -eq 0 ]]; then
                name="$line"
            else
                pass="$line"
            fi
            ctr=$ctr+1
        done <"./config"
    while read -r line
        do
            obs=$line
        done <"./direct_name"
    python3 sync.py $name $pass $obs

elif [ "$1" = "server" ]; then
    if [ "$2" = "set-url" ]; then
       echo $3 > ./server_url
    fi
elif [ "$1" = "observe" ]; then
    echo $2 > ./direct_name
fi
