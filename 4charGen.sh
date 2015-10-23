#!/bin/bash

for i in {a..z};do
	echo $i >> a.txt
	for j in {a..z};do
		echo $i$j >> a.txt
		for k in {a..z};do
			echo $i$j$k >>a.txt
			for l in {a..z};do
				echo $i$j$k$l >> a.txt;
			done
		done
	done
done
