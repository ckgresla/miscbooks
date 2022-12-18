#!/bin/bash
pmset -g batt | grep "[0-9][0-9]%" | awk "NR==1{print$3}" | cut -c 34-36
	#a Script to get the current battery percentage (mac specific utility)
