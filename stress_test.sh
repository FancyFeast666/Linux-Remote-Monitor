#!/bin/bash

#stress cpu for 10 seconds

stress-ng --cpu 6 --timeout 10s &
sleep 15 #waiting for the stress to finish


#stress drives for 10s
stress-ng --hdd 4 --timeout 10s &
sleep 15 #waiting for stress to finish

#stress swap memory for 10s
stress-ng --vm 4 --timeout 10s &
sleep 15

#overall stress
stress-ng -r 0 --timeout 10s &
sleep 15
