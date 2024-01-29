"""
Student: MSc Banking and Finances
Name: Laurence Rosenthal Winckler
From: Zürich, Swizerland
Linkedin: https://www.linkedin.com/in/laurence-rosenthal-winckler/
Github: https://github.com/laurence-rw
EdX: https://profile.edx.org/u/laurencew35
"""

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

def read_csv(csv_file):
    """
    Read data from the CSV file.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        list of dict: List of dictionaries containing data from the CSV file.
    """
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def convert_to_datetime(data):
    """
    Convert string datetime to datetime objects.

    Args:
        data (list of dict): Data containing string datetime values.

    Returns:
        list of dict: Data with datetime values converted to datetime objects.
    """
    for entry in data:
        entry["snapped_at"] = datetime.datetime.strptime(entry["snapped_at"], "%Y-%m-%d %H:%M:%S %Z")
    return data

def calculate_percentage_changes(data):
    """
    Calculate percentage change for each consecutive pair of entries.

    Args:
        data (list of dict): Data containing price information.

    Returns:
        list of float: List of percentage changes.
    """
    percentage_changes = []
    for i in range(1, len(data)):
        previous_price = float(data[i - 1]["price"])
        current_price = float(data[i]["price"])
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        percentage_changes.append(percentage_change)
    return percentage_changes

def count_jumps_within_ranges(percentage_changes, ranges):
    """
    Count occurrences of jumps within specified percentage ranges.

    Args:
        percentage_changes (list of float): List of percentage changes.
        ranges (list of tuple): List of percentage ranges.

    Returns:
        dict: Dictionary containing counts for each percentage range.
    """
    jump_counts = {range_: 0 for range_ in ranges}
    for change in percentage_changes:
        for range_ in ranges:
            if range_[0] <= abs(change) < range_[1]:
                jump_counts[range_] += 1
                break  # Exit the inner loop once a range is found
    return jump_counts

def display_results(jump_counts):
    """
    Display results.

    Args:
        jump_counts (dict): Dictionary containing counts for each percentage range.
    """
    for range_, count in jump_counts.items():
        print(f"Bitcoin had a jump between {range_[0]}% and {range_[1]}% in a single day {count} times.")

def plot_graph(jump_counts, output_file=None):
    """
    Plot graph.

    Args:
        jump_counts (dict): Dictionary containing counts for each percentage range.
        output_file (str, optional): File name to save the graph image. Defaults to None.
    """
    ranges = [f"{range_[0]}-{range_[1]}" for range_ in jump_counts.keys()]
    counts = list(jump_counts.values())

    x = np.arange(len(ranges))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, counts, width, label='Jump Frequency')

    ax.set_xlabel('Percentage Range')
    ax.set_ylabel('Frequency')
    ax.set_title('Bitcoin Jumps Frequency')
    ax.set_xticks(x)
    ax.set_xticklabels(ranges)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    fig.tight_layout()

    if output_file:
        plt.savefig(output_file)  # Save the graph to a file
        plt.close()
        print(f"Graph saved as '{output_file}'.")
    else:
        plt.show()

def main():
    # Path to the CSV file
    csv_file = "btc-usd-max.csv"
    # Read data from the CSV file
    data = read_csv(csv_file)
    # Convert string datetime to datetime objects
    data = convert_to_datetime(data)
    # Calculate percentage change for each consecutive pair of entries
    percentage_changes = calculate_percentage_changes(data)
    # Define percentage ranges
    ranges = [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 25), (25, 50)]
    # Count occurrences of jumps within specified percentage ranges
    jump_counts = count_jumps_within_ranges(percentage_changes, ranges)
    # Display results
    display_results(jump_counts)
    # Plot graph
    output_file = "bitcoin_jumps_frequency.png"
    plot_graph(jump_counts, output_file)

if __name__ == "__main__":
    main()
