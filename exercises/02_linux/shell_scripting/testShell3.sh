#!/bin/bash
#function score_sum {
#	sum=0
#	while true
#	do
#		read -p "enter a score: " score
#
#		if [ "$score" == "q" ] 
#		then
#			break
#		fi
#		sum=$(($sum+$score))
#		echo "total score: $sum"
#	done
#}
#score_sum

function create_file() {
	file_name=$1
	is_shell_script=$2
	touch $file_name
	echo "file $file_name created"
	
	if [ "$is_shell_script" = true ]
	then
		chmod u+x $file_name
		echo "added execute permission to $file_name"
	fi
	
	return 0
}

create_file test.txt true
create_file test2.txt false

function sum() {
	return $(($1+$2))
}

sum 2 10
result1=$? #<-- capture value returned by last command

echo "$result1"
#result2=$(sum 1 2) <-- not working, no exact idea why
#echo "$result1 $result2"
