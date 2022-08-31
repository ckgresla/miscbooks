#!/bin/bash


# Function to Add Things to my Things3 Inbox from the Command Line

things () {

    open "things:///add?title=$1&notes=$2" ;

}



