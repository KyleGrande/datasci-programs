"""
    Name: Kyle Grande
    Email: kyle.grande72@myhunter.cuny.edu
    Resources:
            re docs: https://docs.python.org/3/library/re.html
"""
import re


def rm_tags(data):
    '''
    rm_tags(data): This function takes one input:
    data: a multiline string.
    Returns a string with all HTML formatting removed.
    If the string was plain text, the contents are returned
    unaltered as a string.

    '''
    re_data = re.sub('<[^>]+>', '', data)
    return re_data


def test_rm_tags(rm_tags_fnc):
    '''
    test_rm_tags(rm_tags_fnc): This function takes one input:
    rm_tags_fnc: a function that takes a string and returns a string.
    Returns True if the inputted function correctly strips out the text
    from a HTML file and False otherwise.

    '''
    test_data = """
    <html>
        <head>
            <title>test title</title>
        </head>
        <body>
            <p>test text</p>
        </body>
    </html>
    """
    expected_output = "\n\n\ntest title\n\n\ntest text\n\n\n"
    return rm_tags_fnc(test_data) == expected_output


def make_dict(data):
    '''
    make_dict(data): This function takes one input:
    data: a string
    Uses regular expressions (see Chapter 12.4 for using
    the re package in Python) to find all external links in
    data and store the link text as the key and URL value
    in a dictionary. Title and URL in the CSV file specified by the user.
    For the URL, keep the leading https:// or http://.
    Returns the resulting dictionary.
    '''
    links_dict = {}
    links_pattern = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>')
    links = links_pattern.findall(data)

    for url, text in links:
        links_dict[text] = url

    return links_dict


def test_make_dict(make_dict_fnc):
    '''
    test_make_dict(make_dict_fnc): This function takes one input:
    make_dict_fnc: a function that takes a string and returns a dictionary.
    Returns True if the inputted function correctly returns a dictionary of
    links and False otherwise.
    '''

    test_string = '<a href="http://www.test.com">Test</a> <a href="https://www.test2.org">Test2</a>'
    expected_output = {'Test': 'http://www.test.com', 'Test2': 'https://www.test2.org'}
    actual_output = make_dict_fnc(test_string)
    return actual_output == expected_output


# if __name__ == "__main__":
#     print("Testing rm_tags:", test_rm_tags(rm_tags))
#     print("Testing make_dict:", test_make_dict(make_dict))
