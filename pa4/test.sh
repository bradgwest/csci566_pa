#!/bin/bash
interactive=
while [ "$1" != "" ]; do
    case $1 in
        -f | --file )           shift
                                filename=$1
                                ;;
        -i | --interactive )    interactive=1
                                ;;
        -h | --help )           echo "hello"
                                exit
                                ;;
        * )                     echo "no command"
                                exit 1
    esac
    shift
done
if [ "$interactive" = "1" ]; then
	response=
	echo "Interactive mode is on"
	echo -n "Enter output file name >"
	read response
	if [ -n "$response" ]; then
		echo "+++++"
		echo $response
	fi

	if [ -f $response ]; then
		echo -n "output file exists, Overite? (y/n) > "
		echo $response
		read response
		if [ "$response" != "y" ]; then
			exit 1
		fi
	fi
fi
