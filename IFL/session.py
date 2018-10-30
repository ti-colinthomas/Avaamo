#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import sys


class User:
    def __init__(self, id, timestamp):
        self.id = id
        self.timestamp = timestamp


def main(argv):
    input_file = argv[0]
    output_file = argv[1]

    all_insights = pd.read_csv(input_file, usecols=([3, 15]))
    insight_dict = {}
    columns = ["User", "Sessions"]
    try:
        # Check if output file exists
        pd.read_csv(output_file)
    except FileNotFoundError as error:
        # Create file with headers if file not found
        df = pd.DataFrame(columns=columns)
        df.to_csv(output_file, index=False)

        print("No output file found. Creating " +
              output_file + " for printing.")

        # Loop through raw insights and structure data using key: user
    for index, row in all_insights.iterrows():
        try:
            time = datetime.strptime(row["Created At"], "%Y-%m-%d %H:%M:%S %Z")
            user_id = row["User Id"]
            current_user = User(user_id, time)
            # Add or Append to structure using User Id as key
            # This will be looped through later to get a consecutive list of user chats
            if current_user.id in insight_dict:
                insight_dict[current_user.id].append(current_user)
            else:
                insight_dict[current_user.id] = [current_user]

        except ValueError as error:
            print(index)
            print(error)
            return

    stats_collection = []
    # Loop through the data structured by key: user
    for chats in insight_dict.values():
        i = 0
        session_count = 1
        # Define the break duration here
        break_duration = datetime.strptime("00:02:00", "%H:%M:%S")
        # Loop through the chats for a single user
        while i != len(chats) - 1:
            diff = chats[i].timestamp - chats[i+1].timestamp
            try:
                diff_time = datetime.strptime(str(diff), "%H:%M:%S")
                diff_time = datetime.strptime(str(diff), "%H:%M:%S")
                # Check break between two successive chats for the same user
                if diff_time > break_duration:
                    # Increase count
                    session_count += 1
            except:
                session_count += 1
            i += 1
        # Add to structure to be exported
        session_data = {"Sessions": session_count, "User": chats[0].id}
        stats_collection.append(session_data)

    # Save data to csv
    df = pd.DataFrame(stats_collection, columns=columns)
    df.to_csv(output_file, mode="a", header=False, index=False)


# Go nuts
if __name__ == "__main__":
    try:
        inp = sys.argv[1]
        oup = sys.argv[2]
    except IndexError as error:
        print("No parameters provided")
        print("Provide input and output file")
        print("E.g: session.py insights.csv session.csv")
        sys.exit()
    main(sys.argv[1:])
