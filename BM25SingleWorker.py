from typing import List, Dict, Tuple

import math
import pandas as pd

import spacy
nlp = spacy.load("en_core_web_sm")

from pydantic import BaseModel, Field
from collections import Counter
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup

#this is the function that will