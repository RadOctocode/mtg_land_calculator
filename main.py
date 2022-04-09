# main.py
from math import inf
import re
import sys
import requests
from time import sleep

VALID_COLOR = {"W": "Plains", "U": "Island", "B": "Swamp",
               "R": "Mountain", "G": "Forest", "C": "Wastes"}


def find_colored_pips(card_name):
    """
        returns a dict of colored pips
    """
    response = requests.get(
        "https://api.scryfall.com/cards/named?exact="+card_name)

    mana_cost = response.json()['mana_cost'].strip()
    mana_cost = mana_cost.replace("{", " ")
    mana_cost = mana_cost.replace("}", " ")
    mana_cost = mana_cost.replace("/", " ")
    mana_cost = mana_cost.replace("P", " ")
    mana_cost_list = mana_cost.split(" ")

    return_dict = dict()
    return_total = 0

    for value in mana_cost_list:
        if value in VALID_COLOR:
            if value in return_dict:
                return_dict[value] += 1
            else:
                return_dict[value] = 1
            return_total += 1

    return return_total, return_dict


def remove_sideboards(line_list):
    """
        takes a list of lines
        returns a stripped list of lines without sideboards
    """
    return_value = []
    for line in line_list:
        stripped_line = line.strip()
        if stripped_line == "Maybeboard" or stripped_line == "Sideboard" or stripped_line == "":
            return return_value
        return_value.append(line.strip())

    return return_value


def find_total_cmc(decklist, format_limit):
    """
        takes decklist
        returns dict of color pips and their totals
    """
    try:
        with open(decklist, 'r') as file:
            deck_lines = remove_sideboards(file.readlines())
            total_deck_pips = 0
            total_deck_dict = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "C": 0}
            land_count_dict = dict()

            for line in deck_lines:
                card_name = line.split(" ", 1)[1]
                card_total_pips, card_pip_dict = find_colored_pips(card_name)
                for key in card_pip_dict:
                    total_deck_dict[key] += card_pip_dict[key]
                    total_deck_pips += card_total_pips
                sleep(0.1)

            land_slots_remaining = format_limit - len(deck_lines)
            found_lands = 0
            for key in total_deck_dict:

                land_num = int(
                    (total_deck_dict[key] / total_deck_pips) * land_slots_remaining)
                found_lands += land_num
                if land_num != 0:
                    land_count_dict[key] = land_num

            remainder = land_slots_remaining - found_lands
            if remainder != 0:
                # remove an even amount from every color favor the color with the most amount

                total_colors = len(land_count_dict)
                additional_cards = remainder//total_colors
                extra_rm = remainder % total_colors

                if remainder > 0:
                    # add an equal amount to every color favor the color with the least amount
                    min_lands = inf
                    min_key = ""
                    for key in land_count_dict:
                        land_count_dict[key] += additional_cards
                        if land_count_dict[key] < min_lands:
                            min_lands = land_count_dict[key]
                            min_key = key
                    land_count_dict[min_key] += extra_rm

                elif remainder < 0:
                    # remove an even amount from every color favor the color with the most amount
                    max_lands = 0
                    max_key = ""

                    for key in land_count_dict:
                        land_count_dict[key] -= additional_cards
                        if land_count_dict[key] > max_lands:
                            max_lands = land_count_dict[key]
                            max_key = key
                    land_count_dict[max_key] -= extra_rm
            return land_count_dict
    except FileNotFoundError:
        print("filepath incorrect")
        exit()


if __name__ == "__main__":
    try:
        decklist_path = sys.argv[1]
        format_limit = int(sys.argv[2])
        return_value = find_total_cmc(decklist_path, format_limit)
        for key in return_value:
            print(VALID_COLOR[key] + ": " + str(return_value[key]))
    except IndexError:
        print("python3 main.py <decklist_path> <format_card_limit>")
        exit()
