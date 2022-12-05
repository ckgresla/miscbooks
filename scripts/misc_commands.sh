# Previously had in a ZSHRC -- nice ones to reference (originally ran these on MacOS)

#finds all files in dir and sub-dirs that match with provided REGEX string
find . -type f -name "*Gym*"   

#Unzips all files recursively from current dir down
find . -name "*.zip" | xargs -P 5 -I FILENAME sh -c 'unzip -o -d "$(dirname "FILENAME")" "FILENAME"'   

#removes all .zip files recursively from dir down
find . -depth -name '*.zip' -exec rm {} \;    

#list all of the directories in the current dir (vertical placement)
ls -ld */

#find all files in dir and subdir that contain a REGEX match with string specified
grep -rl "*TOKEN*" *  

#displays a visualization of the history of the current git repo (main|master branch?)
git log --graph --decorate --oneline  

#displays same viz as above but with all remote branches as well
git log --graph --oneline --branches --all    

# Below copies the content of a file and sends to clipboard on MacOS
cat README-561.txt | pbcopy

# Command below displays system colors real nicely
msgcat --color=test

# Print out Just file names for all files in dir
alias ll="ls -Al | tr -s ' ' | cut -f9- -d'



