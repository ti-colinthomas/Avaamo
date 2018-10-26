#!/usr/bin/env python3
import pandas as pd
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_intent_name(name):
    newname = ""
    seperator = ["_", " "]
    for pos, char in enumerate(name):
        if pos == 0 & char.islower():
            if (char == "_"):
                newname += ""
            else:
                newname += char.upper()
        else:
            if char.isupper():
                if pos+1 < len(name):
                    if name[pos+1].isupper():
                        newname += char
                    else:
                        if name[pos+1] in seperator:
                            newname += char
                        else:
                            if newname[len(newname) - 1] == " ":
                                newname += char
                            else:
                                newname += " " + char
                else:
                    newname += char
            else:
                if char == "_":
                    newname += " "
                else:
                    newname += char

    if name != newname:
        print("Formatting name: %s => %s" % (name, newname))
    return newname


def remove_duplicates(values, name):
    output = []
    for value in values:
        if value not in output:
            output.append(value.capitalize())
        else:
            print(bcolors.WARNING + "Removing duplicate variation: %s => Intent: %s" %
                  (value, name) + bcolors.ENDC)
    output.sort()
    output.sort(key=len, reverse=True)

    first = True
    variation = ""
    for value in output:
        if first:
            variation += value
            first = False
        else:
            variation += "," + value
    return variation


def main(argv):
    data = pd.read_csv(argv[0])
    all_intents = []
    duplicates = []

    for index, row in data.iterrows():
        intent_name = row["name"]
        data.iloc[index, data.columns.get_loc("training_data")] = remove_duplicates(
            row["training_data"].split(","), intent_name)
        new_name = format_intent_name(intent_name).capitalize()
        data.iloc[index, data.columns.get_loc("name")] = new_name

        if new_name not in all_intents:
            all_intents.append(new_name)
        else:
            duplicates.append(new_name)

    if len(duplicates) > 0:
        print(bcolors.FAIL +
              "Review below duplicate intent(s) before importing to designer")
    for item in duplicates:
        print(item + bcolors.ENDC)
    data.to_csv("processed_intents.csv")


if __name__ == "__main__":
    main(sys.argv[1:])
