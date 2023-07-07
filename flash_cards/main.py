import logging
import logging.handlers
import sys
import shutil
import argparse

cards = []
definitions = []
mistakes_count = []

# --------------------------------------SET UP LOGGING HANDLERS--------------------------------#
temp_file = "temp_log.txt"

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
console_handler.addFilter(lambda record: not hasattr(record, 'user_input'))

file_handler = logging.FileHandler(temp_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


def log_input(prompt):
    user_input = input(prompt + "\n").lower().strip()
    logging.info("%s: \n%s", prompt, user_input, extra={"user_input": user_input})
    return user_input


# --------------------------------------ACTIONS THAT ARE POSSIBLE TO PERFORM--------------------------------#
def add():
    global cards, definitions, mistakes_count

    card = log_input("The card:")
    while card in cards:
        card = log_input(f"The card \"{card}\" already exists. Try again:")
    definition = log_input("The definition for card:")
    while definition in definitions:
        definition = log_input(f"The definition \"{definition}\" already exists. Try again:")
    cards.append(card)
    definitions.append(definition)
    mistakes_count.append(0)
    logging.info(f"The pair (\"{card}\":\"{definition}\") has been added")


def remove():
    global cards, definitions, mistakes_count

    card = log_input("Which card?")
    if card in cards:
        definitions.remove(definitions[cards.index(card)])
        mistakes_count.remove(mistakes_count[cards.index(card)])
        cards.remove(card)
        logging.info("The card has been removed")
    else:
        logging.info(f"Can't remove \"{card}\". There is no such card.")


def import_from_file(file_name):
    global cards, definitions, mistakes_count
    try:
        with open(file_name, 'r') as file:
            file_cards = file.readlines()
            logging.info(f"{len(file_cards)} cards have been loaded.")
            for file_card in file_cards:
                pair = file_card.split(":")
                if len(pair) < 2:
                    continue
                card = pair[0].lower().strip()
                definition = pair[1].lower().strip()
                if card in cards:
                    definitions[cards.index(card)] = definition
                else:
                    cards.append(card)
                    definitions.append(definition)
                if len(pair) > 2:
                    mistakes_count.append(int(pair[2].strip()))
                else:
                    mistakes_count.append(0)
    except FileNotFoundError:
        logging.error("File not found!")


def export_to_file(file_name):
    with open(file_name, 'a+') as file:
        for card, definition, mistakes in zip(cards, definitions, mistakes_count):
            file.write(f"{card} : {definition} : {mistakes}\n")
        logging.info(f"{len(cards)} cards have been saved.")


def ask():
    global mistakes_count
    ask_times = int(log_input("How many times to ask?"))
    for i in range(ask_times):
        if i >= len(cards):
            logging.info("There is no more cards")
            return
        a = log_input(f"The definition for \"{cards[i]}\"")
        if a == definitions[i]:
            logging.info("Correct!")
        else:
            mistakes_count[i] += 1
            if a in definitions:
                card_for_a = cards[definitions.index(a)]
                logging.info(
                    f"Wrong. The right answer is \"{definitions[i]}\", but your definition is correct for \"{card_for_a}\".")
            else:
                logging.info(f"Wrong. The right answer is \"{definitions[i]}\".")


def exit_program():
    logging.info("Bye Bye!")
    exit()


def log(file_name):
    shutil.copy(temp_file, file_name)
    logging.info("The log has been saved.")
    logging.shutdown()


def get_hardest_card():
    try:
        highest_mistake_count = max(mistakes_count)
    except ValueError:
        logging.info("There are no cards with errors.")
        return
    if highest_mistake_count == 0:
        logging.info("There are no cards with errors.")
        return
    hardest_cards = [card for card, mistakes in zip(cards, mistakes_count) if mistakes == highest_mistake_count]
    if len(hardest_cards) == 1:
        logging.info(
            f"The hardest card is \"{hardest_cards[0]}\". You have {highest_mistake_count} errors answering it.")
    else:
        logging.info("The hardest cards are:")
        for card in hardest_cards:
            logging.info(f"\"{card}\", ")
        logging.info(f"You have {highest_mistake_count} errors answering them.")


def reset_stats():
    global mistakes_count
    mistakes_count = [0] * len(mistakes_count)
    logging.info("Card statistics have been reset.")


actions = {
    "add": add,
    "remove": remove,
    "import": import_from_file,
    "export": export_to_file,
    "ask": ask,
    "exit": exit_program,
    "log": log,
    "hardest card": get_hardest_card,
    "reset stats": reset_stats
}


# --------------------------------------SET UP ARG PARSER FOR COMMAND LINE ARGS--------------------------------#
parser = argparse.ArgumentParser(prog="Flash Cards",
                                 description="Save cards and definitions to assist learning and test memory")
parser.add_argument(
    "-i", "--import_from",
    help="You need to specify a valid file path to import from."
)
parser.add_argument(
    "-e", "--export_to",
    help="You need to specify a valid file path (existing or new) to export to."
)

args = parser.parse_args()
if args.import_from:
    import_from_file(args.import_from)


# --------------------------------------RUN PROGRAM--------------------------------#
while True:
    try:
        action = log_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        if action == "log" or action == "import" or action == "export":
            f_name = log_input("File name:")
            actions[action](f_name)
        else:
            if action == "exit":
                if args.export_to:
                    export_to_file(args.export_to)
            actions[action]()
    except KeyError:
        logging.error("Action is invalid")
    except KeyboardInterrupt:
        logging.info("Exiting gracefully...")
        exit()
