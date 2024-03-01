#!/bin/bash

echo "reading user input"

read -p "Please enter your password: " user_pwd

echo "Your password is $user_pwd"

echo "user $1"
echo "group $2"


for param in $*
 do
	 if [ -d "$param" ]
 	 then
		 echo "executing srcipts in the config folder"
		 ls -l "$param"
	 else
		 echo "not a directory"
	 fi
 done

sum=0
while true
do
	read -p "enter a score: " score

	if [ "$score" == "q" ] 
	then
		break
	fi
	sum=$(($sum+$score))
	echo "total score: $sum"
done

