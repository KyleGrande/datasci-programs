"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:  w3schools for a refresher on items() method
    as well as to see if sum would work as expected for compute_ridership
"""

def make_dictionary(data, kind = "min"):
    """
    Creating a dictionary with a key of the remote unit ID + turnstile unit number.
    Depending on kind, the resulting dictionary will store the minimum entry
    number seen (as an integer), the maximum entry number seen (as an integer),
    or the station name (as a string).
    Returns the resulting dictionary.

    Keyword arguments:
    kind -- kind of dictionary to be created:  min, max, station
    """

    new_dict = {}
    for aline in data:
        info = aline.split(",")
        key = info[1] + "," + info[2]
        if kind == "min":
            num = int(info[9])
            if key not in new_dict or num < new_dict[key]:
                new_dict[key] = num
        elif kind == "max":
            num = int(info[9])
            if key not in new_dict or num > new_dict[key]:
                new_dict[key] = num
        elif kind == "station":
            station = info[3]
            new_dict[key] = station
    return new_dict

def get_turnstiles(station_dict, stations = None):
    """
    If stations is None, returns the names of all the turnstiles stored as keys
    in the inputted dictionary.
    If non-null, returns the keys which have value from station in the inputed dictionary.
    Returns a list.

    Keyword arguments:
    stations -- None or list of station names.
    station -- dict value station
    turnstile -- key value turnstile
    """

    lst = []
    for turnstile, station in station_dict.items():
        if stations is None or station in stations:
            lst.append(turnstile)
    return lst

def compute_ridership(min_dict,max_dict,turnstiles = None):
    """
    Takes as input two dictionaries and a list, possibly empty, of turnstiles.
    If no value is passed for turnstile, the default value of None is used
    (that is, the total ridership for every station in the dictionaries).
    Returns the ridership (the difference between the minimum and maximum values)
    across all turnstiles specified.

    Keyword arguments:
    turnstiles -- None or list of turnstile names
    keys -- either all keys or turnstiles given
    """
    total = 0
    if turnstiles is not None:
        keys = turnstiles
    else:
        keys = max_dict.keys()
    total = sum([max_dict[key] - min_dict[key] for key in keys])
    return total
