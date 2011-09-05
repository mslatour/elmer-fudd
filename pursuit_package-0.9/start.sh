#!/bin/bash

trap kill_programs INT

kill_programs()
{
    echo "Killing Program"
    killall -q predator
    killall -q prey
    killall -q pursuit_monitor
    killall -q pursuit
    exit 0
}

echo "*****************************************************************"
echo "* Pursuit Domain - University of Amsterdam, The Netherlands     *"
echo "* Created by Jelle Kok                                          *"
echo "* Copyright 2002-2003.  All rights reserved.                    *"
echo "*****************************************************************"

pursuit_dir="/opt/stud/mas/bin"

pursuit_dir="pursuit/src"
pursuit="$pursuit_dir/pursuit"
pursuit_conf="$pursuit_dir/pursuit.conf"
monitor_dir="monitor/src"
monitor="$monitor_dir/pursuit_monitor"
monitor_conf="$monitor_dir/monitor.conf"
predator="skeletons/predator/src/predator"
prey="skeletons/prey/src/prey"

${pursuit} -conf ${pursuit_conf} &    # start the server (no visualization yet)
sleep 1
${predator}   &                       # start clients, only output info pred. 1
sleep 1
#${predator} > /dev/null & 
#sleep 1
#${predator} > /dev/null & 
#sleep 1
#${predator} > /dev/null & 
#sleep 1
#${prey}     > /dev/null & 
#sleep 1
${prey}     > /dev/null & 

${monitor} -conf ${monitor_conf}       # start visualization

wait
