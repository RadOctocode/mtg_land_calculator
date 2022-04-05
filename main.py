# main.py
import sys

def find_card_cmc(card_name):
    """
        returns the cmc of the card given the name
    """
    return 0

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


def find_total_cmc(decklist):
    """
        takes decklist
        returns dict of color pips and their totals
    """
    with open(decklist,'r') as file:
        deck_lines = remove_sideboards(file.readlines())
        for line in deck_lines:
                card_name = line.split(" ",1)[1]
        print("finished")

        return decklist
    


if __name__ == "__main__":
    try:
        decklist_path = sys.argv[1]
        format_limit = int(sys.argv[2])
        find_total_cmc(sys.argv[1])
    except IndexError:
        print("python3 main.py <decklist_path> <format_card_limit>")
        exit()




