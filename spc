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
    read -p "1 for upload 2 for download" var
    if [ "$var" = "1" ]; then
        python uploade
    elif [ "$var" = "2" ]; then
        python downloade
    else
        echo "out of range"
    fi
elif [ "$1" = "server" ]; then
    if [ "$2" = "set-url" ]; then
       echo $3 > ./server_url
    fi
elif [ "$1" = "observe" ]; then
    echo $2 > ./direct_name
fi
