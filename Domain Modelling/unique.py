#!/usr/bin/env python3
import pandas as pd


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
    print("Formatting: %s => %s" % (name, newname))
    return newname


def remove_duplicates(values):
    output = []
    for value in values:
        if value not in output:
            output.append(value.capitalize())
        else:
            print("Removing duplicate: %s" % value)
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


if __name__ == '__main__':
    data = pd.read_csv("intents.csv")

    for index, row in data.iterrows():
        data.iloc[index, data.columns.get_loc("training_data")] = remove_duplicates(
            row["training_data"].split(","))
        data.iloc[index, data.columns.get_loc("name")] = format_intent_name(
            row["name"]).capitalize()
    data.to_csv("processed_intents.csv")
