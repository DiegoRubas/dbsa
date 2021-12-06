import csv
import matplotlib.pyplot as plt
import numpy as np
import random as rnd


NO_BINS = 10
NO_JOIN_RANGES, NO_JOIN_IT = 5, 1000
NO_SEL_RANGES, NO_SEL_IT = 10, 1000


class Table:

    def __init__(self, number):
        self.lines, self.bounds = [], []
        self.minimum, self.maximum, self.interval, self.avg_bin_count = 0, 0, 0, 0
        self.occurrence = [0] * NO_BINS
        # self.weighted_occ = [0] * NO_BINS  # each contribution to a bin is 1/length of the range
        self.displayed_ranges = number
        self.create_ranges()
        self.fill_bounds()
        self.count_occurrence()
        # self.count_weighted_occ()

    def create_ranges(self):
        for i in range(100):
            self.lines.append((create_range(0, 101)))
        self.minimum = min([line[0] for line in self.lines[:self.displayed_ranges]])
        self.maximum = max([line[1] for line in self.lines[:self.displayed_ranges]])
        self.interval = self.maximum - self.minimum

    def fill_bounds(self):
        for i in range(NO_BINS):
            lower_bound = round(self.minimum + i * self.interval / NO_BINS, 1)
            upper_bound = round(self.minimum + (i + 1) * self.interval / NO_BINS, 1)
            self.bounds.append((lower_bound, upper_bound))

    def count_occurrence(self):
        for i in range(self.displayed_ranges):
            for j in range(NO_BINS):
                if overlaps(self.lines[i], self.bounds[j]):
                    self.occurrence[j] += 1
                    self.avg_bin_count += 1
        self.avg_bin_count /= self.displayed_ranges
        self.avg_bin_count = int(self.avg_bin_count + 1)

    # def count_weighted_occ(self):
    #     for i in range(NO_JOIN_RANGES):
    #         bin_count = 0
    #         for j in range(NO_BINS):
    #             if overlaps(self.lines[i], self.bounds[j]):
    #                 bin_count += 1
    #         for j in range(NO_BINS):
    #             if overlaps(self.lines[i], self.bounds[j]):
    #                 self.weighted_occ[j] += 1 / bin_count


def create_range(b1, b2):
    lower_bound, upper_bound = 0, 0
    while not (lower_bound < upper_bound):
        lower_bound, upper_bound = rnd.randrange(b1, b2), rnd.randrange(b1, b2)
    return lower_bound, upper_bound


def str_left_of(r1, r2):
    return r1[1] < r2[0]


def str_right_of(r1, r2):
    return r1[0] > r2[1]


def overlaps(r1, r2):
    if str_left_of(r1, r2):
        return False
    elif str_right_of(r1, r2):
        return False
    else:
        return True

def display_table(t1, r):

    x = np.linspace(1, 21, 200)

    plt.figure()

    for i in range(NO_SEL_RANGES):
        plt.hlines(y=11 - i, xmin=t1.lines[i][0], xmax=t1.lines[i][1], linewidth=2, color='r')
        plt.text(x=(t1.bounds[i][0] + t1.bounds[i][1]) / 2, s=t1.occurrence[i], y=11.5, color='black')
    plt.hlines(y=11.5, xmin=t1.minimum, xmax=t1.maximum, linewidth=1, color='black')
    plt.hlines(y=0.5, xmin=t1.minimum, xmax=t1.maximum, linewidth=1, color='black')
    plt.hlines(y=1, xmin=r[0], xmax=r[1], linewidth=2, color='b')

    for i in range(NO_BINS):
        plt.vlines(x=t1.bounds[i][0], ymin=0.5, ymax=11.5, linewidth=1, color='black')
    plt.vlines(x=t1.bounds[9][1], ymin=0.5, ymax=11.5, linewidth=1, color='black')

    plt.show()


def display_2_tables(t1, t2):

    x = np.linspace(1, 21, 200)

    plt.figure()

    for i in range(NO_JOIN_RANGES):
        plt.hlines(y=20 - 2*i, xmin=t1.lines[i][0], xmax=t1.lines[i][1], linewidth=2, color='r')
        plt.hlines(y=10 - 2*i, xmin=t2.lines[i][0], xmax=t2.lines[i][1], linewidth=2, color='b')

    for i in range(NO_BINS):
        plt.vlines(x=t1.bounds[i][0], ymin=10.5, ymax=20.5, linewidth=1, color='black')
        plt.text(x=(t1.bounds[i][0] + t1.bounds[i][1]) / 2, s=t1.occurrence[i], y=20.75, color='black')
        # plt.text(x=t1.bounds[i][0], s=round(t1.weighted_occ[i], 2), y=20.75, color='black')
        plt.vlines(x=t2.bounds[i][0], ymin=0.5, ymax=10.5, linewidth=1, color='black')
        plt.text(x=(t2.bounds[i][0] + t2.bounds[i][1]) / 2, s=t2.occurrence[i], y=-0.25, color='black')
        # plt.text(x=t2.bounds[i][0], s=round(t2.weighted_occ[i], 2), y=-0.25, color='black')
    plt.vlines(x=t1.bounds[9][1], ymin=10.5, ymax=20.5, linewidth=1, color='black')
    plt.vlines(x=t2.bounds[9][1], ymin=0.5, ymax=10.5, linewidth=1, color='black')
    plt.hlines(y=20.5, xmin=t1.minimum, xmax=t1.maximum, linewidth=1, color='black')
    plt.hlines(y=10.5, xmin=t1.minimum, xmax=t1.maximum, linewidth=1, color='black')
    plt.hlines(y=10.5, xmin=t2.minimum, xmax=t2.maximum, linewidth=1, color='black')
    plt.hlines(y=0.5, xmin=t2.minimum, xmax=t2.maximum, linewidth=1, color='black')

    plt.show()


def join_cardinality(t1, t2):
    count = 0
    for l1 in t1.lines[:NO_JOIN_RANGES]:
        for l2 in t2.lines[:NO_JOIN_RANGES]:
            if overlaps(l1, l2):
                count += 1
    return count


def join_estimation(t1, t2):
    """
    1st method: increments the count for each overlap between a bin from the first relation and a bin from the second
    relation
    - advantage:
        - least computing power
    - disadvantage:
        - doesn't account for multiple ranges in one bin
        - independent of ranges and only uses bin spatial disposition
    2nd method: for each bin b1 from the first relation R1 and for each bin b2 from the second relation R2, it multiplies
    the number of ranges in b1 by the number of ranges in b2 and adds that product to the total count
    - advantage:
        - accounts for multiple ranges in one bin
    - disadvantage:
        - counts one actual overlap multiple times if 2 ranges overlap over multiple bins combinations
    3rd method: same as step 2 but normalises by average bin span of the considered ranges
    - advantage:
        - accounts for overlaps of 2 long ranges
        - adjusts the count depending on the ranges' average bin span
    - disadvantage:
        - requires the most memory of all methods
    """
    count = 0
    for i in range(NO_BINS):
        for j in range(NO_BINS):
            if overlaps(t1.bounds[i], t2.bounds[j]):
                # count += 1  # adds to the count whenever bounds overlap
                count += t1.occurrence[i] * t2.occurrence[j]
    # count /= t1.avg_bin_count  # ±28%
    # count /= t2.avg_bin_count  # ±28%
    count /= t1.avg_bin_count * 0.5 + t2.avg_bin_count + 0.5  # 23%
    count = int(round(count))
    return count


def print_join_details(t1, t2):
    join_card = join_cardinality(t1, t2)
    join_est = join_estimation(t1, t2)
    print("join cardinality:", join_card)
    print("join estimation after dividing by average bin count",
          int(round(t1.avg_bin_count * 0.5 + t2.avg_bin_count * 0.5)),
          ':', join_est)
    rel_diff = abs(join_card - join_est) / join_card
    print("relative difference " + str(round(rel_diff * 100, 2)) + "%")


def join_csv():
    avg_rel_diff = 0
    with open('join_estimation.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([join_cardinality.__name__, join_estimation.__name__,
                             'absolute_difference', 'relative_difference'])
        for i in range(NO_JOIN_IT):
            t1, t2 = Table(NO_JOIN_RANGES), Table(NO_JOIN_RANGES)
            join_card = join_cardinality(t1, t2)
            join_est = join_estimation(t1, t2)
            abs_diff = abs(join_card - join_est)
            rel_diff = abs_diff / join_cardinality(t1, t2)
            csv_writer.writerow([join_card, join_est, abs_diff, rel_diff])
            avg_rel_diff += rel_diff
        avg_rel_diff /= NO_JOIN_IT
        csv_writer.writerow(["average relative difference " + str(round(avg_rel_diff * 100, 2)) + "%"])


def left_cardinality(t1, r):
    count = 0
    for l1 in t1.lines[:NO_SEL_RANGES]:
        if str_left_of(l1, r):
            count += 1
    return count


def left_estimation(t1, r):
    count, range_bin_count = 0, 0
    for i in range(NO_BINS):
        if str_left_of(t1.bounds[i], r):
            count += t1.occurrence[i]  # 180%
            range_bin_count += 1
    # print("left estimation before dividing:", count)
    # count /= round(t1.avg_bin_count * 0.5 + range_bin_count * 0.5)  # 36%
    count /= round(t1.avg_bin_count)  # 30%
    # if range_bin_count != 0:  # 50%
    #     count /= round(range_bin_count)
    count = int(round(count))
    return count


def print_left_of_details(t1, r):
    left_card = left_cardinality(t1, r)
    left_est = left_estimation(t1, r)
    print("left of cardinality:", left_card)
    print("left of estimation after dividing by average bin count",
          int(round(t1.avg_bin_count)),
          ':', left_est)
    abs_diff = abs(left_card - left_est)
    rel_diff = 0
    if left_card == 0:
        if left_est == 0:
            rel_diff = 0
        else:
            rel_diff = 1
    else:
        rel_diff = abs_diff / left_card
    print("relative difference " + str(round(rel_diff * 100, 2)) + "%")


def left_of_csv():
    avg_rel_diff = 0
    with open('left_of_estimation.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([left_cardinality.__name__, left_estimation.__name__,
                             'absolute_difference', 'relative_difference'])
        for i in range(NO_SEL_IT):
            t1, r = Table(NO_JOIN_RANGES), create_range(0, 101)
            left_card = left_cardinality(t1, r)
            left_est = left_estimation(t1, r)
            abs_diff = abs(left_card - left_est)
            rel_diff = 0
            if left_card == 0:
                if left_est == 0:
                    rel_diff = 0
                else:
                    rel_diff = 1
            else:
                rel_diff = abs_diff / left_card
            csv_writer.writerow([left_card, left_est, abs_diff, rel_diff])
            avg_rel_diff += rel_diff
        avg_rel_diff /= NO_JOIN_IT
        csv_writer.writerow(["average relative difference " + str(round(avg_rel_diff * 100, 2)) + "%"])


def overlap_cardinality(t1, r):
    count = 0
    for l1 in t1.lines[:NO_SEL_RANGES]:
        if overlaps(l1, r):
            count += 1
    return count


def overlap_estimation(t1, r):
    count, range_bin_count = 0, 0
    for i in range(NO_BINS):
        if overlaps(t1.bounds[i], r):
            count += t1.occurrence[i]  # 73%
            range_bin_count += 1
    # count /= round(t1.avg_bin_count * 0.5 + range_bin_count * 0.5)  # 70%
    # count /= round(t1.avg_bin_count)  # 70%
    if range_bin_count != 0:  # 61%
        count /= round(range_bin_count)
    count = int(round(count))
    return count


def print_overlap_details(t1, r):
    over_card = overlap_cardinality(t1, r)
    print("overlap cardinality:", over_card)
    over_est = overlap_estimation(t1, r)
    print("overlap estimation after dividing by average bin count",
          int(round(t1.avg_bin_count)),
          ':', over_est)
    abs_diff = abs(over_card - over_est)
    rel_diff = 0
    if over_card == 0:
        if over_est == 0:
            rel_diff = 0
        else:
            rel_diff = 1
    else:
        rel_diff = abs_diff / over_card
    print("relative difference " + str(round(rel_diff * 100, 2)) + "%")


def overlap_csv():
    avg_rel_diff = 0
    with open('overlap_estimation.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([overlap_cardinality.__name__, overlap_estimation.__name__,
                             'absolute_difference', 'relative_difference'])
        for i in range(NO_SEL_IT):
            t1, r = Table(NO_JOIN_RANGES), create_range(0, 101)
            over_card = overlap_cardinality(t1, r)
            over_est = overlap_estimation(t1, r)
            abs_diff = abs(over_card - over_est)
            rel_diff = 0
            if over_card == 0:
                if over_est == 0:
                    rel_diff = 0
                else:
                    rel_diff = 1
            else:
                rel_diff = abs_diff / over_card
            csv_writer.writerow([over_card, over_est, abs_diff, rel_diff])
            avg_rel_diff += rel_diff
        avg_rel_diff /= NO_JOIN_IT
        csv_writer.writerow(["average relative difference " + str(round(avg_rel_diff * 100, 2)) + "%"])


# table_1, table_2 = Table(NO_JOIN_RANGES), Table(NO_JOIN_RANGES)
# display_2_tables(table_1, table_2)
# print_join_details(table_1, table_2)
# join_csv()
# print()


# table_3, random_range = Table(NO_SEL_RANGES), create_range(0, 101)
# display_table(table_3, random_range)
# print_left_of_details(table_3, random_range)
# left_of_csv()
# print()


# table_4, random_range_2 = Table(NO_SEL_RANGES), create_range(0, 101)
# display_table(table_4, random_range_2)
# print_overlap_details(table_4, random_range_2)
# overlap_csv()
