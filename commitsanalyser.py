import sys
import matplotlib.pyplot as plt


def open_file(file_name):

    try:
        file = open(file_name, "r")  # Try to open the specified file in read mode
    except IOError:  # If an IOError occurs (file not found, permission issues, etc.)
        print("Error: could not open file: " + file_name)  # Print an error message
        sys.exit(1)  # Exit the program with a non-zero status code to indicate an error
    return file  # Return the file object if it was successfully opened


def read_committers_ids():
    global committers_ids, identities_file, commits  # Declare global variables used in this function

    # Read lines from the identities_file and remove the newline character '\n' from each line.
    committers_data = [x.replace("\n", "") for x in identities_file.readlines()][1:]

    # Iterate through the committers' data.
    for identity in committers_data:
        # Split each line into two parts using a comma as a separator.
        id_split = identity.split(",")
        # Store the committer's ID and name in the committers_ids dictionary.
        committers_ids[id_split[0]] = id_split[1]
        # Create an entry for the committer in the commits dictionary with specific tasks and their initial values.
        commits[id_split[1]] = {"SwM tasks": [0, 0, 0], "NFR Labeling": [0, 0, 0, 0, 0, 0],
                                "SoftEvol tasks": [0, 0, 0, 0]}


def read_commits():
    global committers_ids, commits, commits_file

    # Read lines from the commits_file, remove the newline character '\n' from each line, and skip the header.
    commits_data = [x.replace("\n", "") for x in commits_file.readlines()][1:]

    # Iterate through the commits' data.
    for commit in commits_data:

        # Split each line into 16 parts using a comma as a separator.
        commit_split = commit.split(",")

        # Store relevant data from the commit in variables.
        commit_id = commit_split[0]
        swm = commit_split[1:4]
        nfr = commit_split[4:10]
        soft_evol = commit_split[10:14]
        committer_id = commit_split[14]
        commit_msg = commit_split[15]

        # SWM
        for i in range(3):
            # Update the relevant task counts for the committer in the commits' dictionary.
            commits[committers_ids[committer_id]]["SwM tasks"][i] += int(swm[i])

        # NFR
        for i in range(6):
            # Update the relevant task counts for the committer in the commits' dictionary.
            commits[committers_ids[committer_id]]["NFR Labeling"][i] += int(nfr[i])

        # SoftEvol
        for i in range(4):
            # Update the relevant task counts for the committer in the commits' dictionary.
            commits[committers_ids[committer_id]]["SoftEvol tasks"][i] += int(soft_evol[i])


# Display the menu options and take the user's input.
def take_menu_input():
    print("\nMenu")
    print("1. Compare the number of commits done by a particular developer for a given classification scheme.")
    print("2. Compare the number of commits done by all developers, which are classified with a given "
          "feature (for example, developer X has Y commits, developer I has J commits, and developer A "
          "has B commits for a given feature).")
    print("3. Print the developer with the maximum number of commits for a given feature (for example, "
          "print the developer who has the maximum number of commits with Corrective Tasks).")
    print("4. Exit")
    try:
        menu_in = int(input("Enter your choice: "))
    except ValueError:
        print("Error: invalid input")
        return -1  # Return -1 to indicate an error if the input is not a valid integer

    return menu_in  # Return the user's choice as an integer


def compare_developer_commits():
    global commits, feature_names

    # Get input from the user for the developer's name and the classification scheme.
    dev_name = take_developer_name_input()
    classification_scheme = take_classification_input()

    # Plot a bar graph of the developer's commits for the chosen classification scheme.
    plot_bar_graph(feature_names[classification_scheme], commits[dev_name][classification_scheme], "Features",
                   "Commits", "Commits by " + dev_name + " for " + classification_scheme)


def compare_feature_commits():

    # Get input from the user for the classification scheme and the feature.
    classification_scheme = take_classification_input()
    feature = take_feature_input(classification_scheme)
    # Get the commits for the chosen feature and classification scheme.
    feature_commits = get_feature_commits(feature, classification_scheme)

    # Plot a bar graph of the commits for the chosen feature and classification scheme.
    plot_bar_graph(feature_commits.keys(), feature_commits.values(), "Developers", "Commits", "Commits for " + feature)


def print_max_commits():
    # Get input from the user for the classification scheme and the feature.
    classification_scheme = take_classification_input()
    feature = take_feature_input(classification_scheme)

    # Get the commits for the chosen feature and classification scheme.
    feature_commits = get_feature_commits(feature, classification_scheme)

    # Print the developer with the maximum number of commits for the chosen feature and classification scheme.
    print("Max commits for " + feature + ": " + max(feature_commits, key=feature_commits.get))


def take_developer_name_input():
    global commits

    # Create a list to store the developers' names, to easily access them by index by input.
    dev_names_list = []

    # Iterate through the developers' names in the commits dictionary.
    print("List of developers: ")
    i = 0
    for dev_name in commits.keys():
        dev_names_list.append(dev_name)
        i += 1
        print(str(i) + ": " + dev_name)

    # Take input from the user for the developer's name.
    dev_input = -1
    while dev_input < 1 or dev_input > i:
        try:
            dev_input = int(input("Please choose a developer: "))
        except ValueError:
            print("Error: invalid input")

    # Return the developer's name from the list of developers' names.
    return dev_names_list[dev_input - 1]


def take_classification_input():
    classification_input = ""

    # Take input from the user for the classification scheme.
    print("1. Swanson's Maintenance Tasks")
    print("2. NFR Labeling")
    print("3. Software Evolution Tasks")

    while not (classification_input == "1" or classification_input == "2" or classification_input == "3"):
        classification_input = input("Please choose the classification scheme: ")

    if classification_input == "1":
        return "SwM tasks"
    elif classification_input == "2":
        return "NFR Labeling"
    elif classification_input == "3":
        return "SoftEvol tasks"

    return ""


def take_feature_input(classification_scheme):
    global feature_names

    # Print the list of features for the chosen classification scheme.
    print("List of features: ")
    i = 0
    for feature in feature_names[classification_scheme]:
        i += 1
        print(str(i) + ": " + feature)

    # Take input from the user for the feature.
    feature_input = -1
    while feature_input < 1 or feature_input > i:
        try:
            feature_input = int(input("Please choose a feature: "))
        except ValueError:
            print("Error: invalid input")

    # Return the feature name from the list of features.
    return feature_names[classification_scheme][feature_input - 1]


def get_feature_commits(feature, classification_scheme):
    global commits, feature_names

    # Create a dictionary to store the commits for the chosen feature and classification scheme, for each developer.
    feature_commits = {}

    # Iterate through the developers' names in the commits dictionary and store the commits for the chosen feature
    for dev_name, dev_data in commits.items():
        feature_commits[dev_name] = dev_data[classification_scheme][feature_names[classification_scheme].index(feature)]

    return feature_commits


# Plot a bar graph with the given data.
def plot_bar_graph(x, y, x_label, y_label, title):
    plt.bar(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python commitsanalyser_ahmed.py <commits_file> <identities_file>")
        sys.exit(1)

    # Open the commits and identities files.
    commits_file = open_file(sys.argv[1])
    identities_file = open_file(sys.argv[2])
    # Declare global variables for commits, committers' IDs, and feature names.
    committers_ids = {}
    commits = {}
    feature_names = {}

    # Read the committers' IDs and commits from the files.
    read_committers_ids()
    read_commits()

    # Set the feature names for each classification scheme.
    feature_names["SwM tasks"] = ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"]
    feature_names["NFR Labeling"] = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency",
                                     "Portability"]
    feature_names["SoftEvol tasks"] = ["Forward Engineering", "Re-Engineering", "Corrective", "Code Management"]

    # Take input from the user for the menu options and call the relevant functions.
    menu_input = -1
    while menu_input != 4:
        menu_input = take_menu_input()

        if menu_input == 1:
            compare_developer_commits()
        elif menu_input == 2:
            compare_feature_commits()
        elif menu_input == 3:
            print_max_commits()

    # Close the files.
    commits_file.close()
    identities_file.close()
    print("Exiting...")
