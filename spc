#!/bin/bash

if [[ "$1" = "config" ]]; then
    if [[ "$2" = "edit" ]]; then
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
elif [[ "$1" = "sync" ]]; then
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
    ctr=0 
    while read -r line
        do
            #echo $line
            if [[ $ctr -eq 0 ]]; then
                encr="$line"
            elif [[ $ctr -eq 1 ]]; then
                entr1="$line"
            elif [[ $ctr -eq 2 ]]; then
                entr2="$line"
            elif [[ $ctr -eq 3 ]]; then
                entr3="$line"
            fi
            ctr=$ctr+1
        done <"crypt"
    if [[ $encr = '1' ]]; then
    	python3 sync.py $name $pass $obs $encr $entr1
    elif [[ $encr = '2' ]]; then
    	python3 sync.py $name $pass $obs $encr $entr1 $entr2 
    elif [[ $encr = '3' ]]; then
    	python3 sync.py $name $pass $obs $encr $entr1 
    fi
    spc status

elif [[ "$1" = "status" ]]; then
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
    ctr=0
    while read -r line
        do
            #echo $line
            if [[ $ctr -eq 0 ]]; then
                encr="$line"
            elif [[ $ctr -eq 1 ]]; then
                entr1="$line"
            elif [[ $ctr -eq 2 ]]; then
                entr2="$line"
            elif [[ $ctr -eq 3 ]]; then
                entr3="$line"
            fi
            ctr=$ctr+1
        done <"crypt"
	python3 sync.py $name $pass $obs $1 $encr $entr1 $entr2

elif [[ "$1" = "en-de" ]]; then
    if [[ "$2" = "list" ]]; then
    	echo "Encryption schemas available are: "
    	echo "1. ARC4"
    	echo "2. AES"
    	echo "3. DES"
    
    elif [[ "$2" = "update" ]]; then
    	if [[ "$#" -eq 2 ]]; then
	    	read -p "Schema used: " schema
	    	if [[ "$schema" = "ARC4" ]]; then
	    		echo "1">crypt
	    		read -p "key: " k
	    		echo $k>>crypt
	    		echo ''>>crypt
	    		echo "Updated"
	    	elif [[ "$schema" = "AES" ]]; then
	    		echo "2">crypt
	    		read -p "key(length=16): " k
	    		read -p "iv(length=16): " iv
	    		echo $k>>crypt
	    		echo $iv>>crypt
	    		echo ''>>crypt
	    		echo "Updated"
	    	elif [[ "$schema" = "DES" ]]; then
	    		echo "3">crypt
	    		read -p "key(length=8): " k
	    		echo $k>>crypt
	    		echo ''>>crypt
	    		echo "Updated"
	    	fi
	    else
	    	cp $3 crypt
	    	echo ''>>crypt
	    	echo "Updated"
	    fi
	elif [[ "$2" = "dump" ]]; then
		echo "This exposes info"
		echo "Do you want to continue? (Y/N)"
		read v
		if [[ "$v" = "Y" ]]; then
			cp crypt $3
			echo "Info written"
		fi
	fi

elif [ "$1" = "server" ]; then
    echo "Server operating at http://127.0.0.1:8000/"
elif [ "$1" = "server" ]; then
    if [ "$2" = "set-url" ]; then
       echo $3 > ./server_url
    fi
elif [ "$1" = "observe" ]; then
    echo $2 > ./direct_name


elif [ "$1" = "help" ]; then
    echo "spc version :             Prints version"
    echo "spc server :              Shows ip of the server"
    echo "spc config edit :         To edit user credentials"
    echo "spc observe <dir-path>:   Choose the directory to observe"
    echo "spc sync :                For syncing directory with database"
    echo "spc status :              Compare directory with server's database"
    echo "spc en-de list :          list all encryption schemas"
    echo "spc end-de update :       Update encryption schema and key(s)"
    echo "spc en-de update <file>   Dump encryption schema from a file"
    echo "spc en-de dump <file>     Dump current schema to the file"

elif [ "$1" = "version" ]; then
    echo "VERSION 1"

elif [ "$1" = "startPsync" ]; then
    systemctl status cron
    var1=`pwd`
    var2=`echo "$var1/periodicSync.sh"`
    crontab -l ; echo "* * * * * export DISPLAY=:0 && bash $var2" | crontab -

elif [ "$1" = "endSync" ]; then
    crontab -r
else
    echo "Invalid command"
    echo "For details- spc help"
fi
