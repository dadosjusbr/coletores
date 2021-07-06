# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def is_nan(string):
    return string != string
