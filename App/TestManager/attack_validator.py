#################################################################################
# File: attack_validator.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Used to validate that an acceptable attack name has been passed.
#################################################################################

#################################################################################
# validate_attack(self, config_dict)
#
# Validates the name of the adversarial attack.
# Args:
#    attack: the name of the attack
#
# Usage:
#    Used in TestManager main() to verify the used has passed a valid attack that
#    will be used to attack Neptune. Also used in the NidsConfigValidator class to
#    validate the attack_feature_selection field.
#
# Exception:
#

def validate_attack(attack):
    acceptable_attacks = [
            "Standard",
            "Evasion: Rate",
            "Evasion: Payload",
            "Evasion: Pairflow",
            "Evasion: Rate+Payload",
            "Evasion: Payload+Pairflow",
            "Evasion: Rate+Pairflow",
            "Evasion: Payload+Rate+Pairflow"]
    if attack not in acceptable_attacks:
        raise Exception("Invalid attack: " + str(attack) + ", valid attacks: " + str(acceptable_attacks))
