#!/bin/bash

#ad_attack_list=(\
#        "Evasion: Rate"\
#        "Evasion: Payload"\
#        "Evasion: Pairflow"\
#        "Evasion: Rate+Payload"\
#        "Evasion: Rate+Pairflow"\
#        "Evasion: Payload+Pairflow"\
#        "Evasion: Evasion: Payload+Pairflow")

ad_attack_list=("Evasion: Payload+Pairflow")

for ad_attack in "${ad_attack_list[@]}"
do
    echo ${ad_attack}
    sudo python3 App/TestManager/main.py "${ad_attack}"
done
