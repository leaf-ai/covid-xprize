import os
from pprint import pprint
import pandas as pd
from pandas.io.parsers import read_csv
import csv

ROOT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              os.pardir)
DATA_FILE_PATH = os.path.join(ROOT_DIRECTORY, "data", "files")


def get_orig_oxford_df():
    DATA_URL = os.path.join(DATA_FILE_PATH, "OxCGRT_latest.csv")
    oxford_df = pd.read_csv(DATA_URL,
                            parse_dates=['Date'],
                            encoding="ISO-8859-1",
                            dtype={"RegionName": str,
                                    "RegionCode": str},
                            error_bad_lines=False)

    oxford_df["RegionName"] = oxford_df["RegionName"].fillna("")
    return oxford_df


def get_aug_oxford_df():
    DATA_URL = os.path.join(DATA_FILE_PATH, "OxCGRT_latest_aug.csv")
    oxford_df = pd.read_csv(DATA_URL,
                            parse_dates=['Date'],
                            encoding="ISO-8859-1",
                            dtype={"RegionName": str,
                                    "RegionCode": str},
                            error_bad_lines=False)

    oxford_df["RegionName"] = oxford_df["RegionName"].fillna("")
    return oxford_df

def get_pop_df():
    DATA_URL = os.path.join(DATA_FILE_PATH, "pop.csv")
    pop_df = pd.read_csv(DATA_URL)
    return pop_df


def filter_df_regions(oxford_df):

    ## code for filtering out rows that dont belong to set of countries and region we care

    countries = list(oxford_df.CountryName.unique())
    regions = list(oxford_df.RegionName.unique())
    oxford_df = oxford_df[(oxford_df.CountryName.isin(countries)) &
                          (oxford_df.RegionName.isin(regions))]

    return oxford_df


def get_valid_areas():

    DATA_URL = os.path.join(DATA_FILE_PATH, "countries_regions.csv")

    code_dict = {}

    with open(DATA_URL) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row["CountryCode"]:
                code_dict[row["CountryCode"]] = (row['CountryName'],"")
            if row["RegionCode"]:
                code_dict[row["RegionCode"]] = (row['CountryName'], row['RegionName'])

    return code_dict

VALID_AREAS = get_valid_areas()

VALID_COUNTRIES = {k:v[0] for k,v in VALID_AREAS.items() if "_" not in k}
VALID_REGIONS =  {k:v for k,v in VALID_AREAS.items() if "_" in k}
COUNTRY_CODES = set(VALID_COUNTRIES.keys())
REGION_CODES = set(VALID_REGIONS.keys())

INV_VALID_COUNTRIES = {v: k for k, v in VALID_AREAS.items() if "_" not in k}
INV_VALID_REGIONS = {v: k for k, v in VALID_AREAS.items() if "_" in k}
REG_C_MAP = {**INV_VALID_COUNTRIES, **INV_VALID_REGIONS}


with open(os.path.join(DATA_FILE_PATH, "country_codes.txt"), 'wt') as out:
    pprint(VALID_COUNTRIES, out)

with open(os.path.join(DATA_FILE_PATH, "region_codes.txt"), 'wt') as out:
    pprint(VALID_REGIONS, out)

#pprint(INV_VALID_COUNTRIES)
#pprint(INV_VALID_REGIONS)
#pprint(REG_C_MAP)

def pop_areaname(country_name, region_name):
    code  = REG_C_MAP(country_name, region_name)

    df = get_pop_df()
    print(df[df["Code"]==code].values.tolist()[0][2:5])
    return df[df["Code"]==code].values.tolist()[0][2:5]