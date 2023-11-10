import requests
import pandas as pd
import urllib.request
import re
import zipfile
import re
import numpy as np
import itertools

def new_concat(df, new_column, *args):
    df[new_column] = ''
    for col in args:
        df[new_column] += df[col]
    return df