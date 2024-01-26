#!/usr/bin/env python
"""Simple script to download and format the data from
   https://store.steampowered.com/hwsurvey/videocard/
"""

from json import dump as jdump
from requests import get as rget

from bs4 import BeautifulSoup
from bs4 import element

PAGE_URL = "https://store.steampowered.com/hwsurvey/videocard/"


def get_list_of_tables_from_soup(soupdata):
    """Get a list of tables from the BeautifulSoup data"""
    listolists = []
    index = 0

    for current_element in soupdata.find("div", id="sub_stats"):
        if len(listolists) <= index:
            listolists.append([])
        if isinstance(current_element, element.Tag):
            if current_element.name == 'br' \
               and 'clear' in current_element.attrs \
               and current_element.attrs['clear'] == 'all':
                index += 1
            else:
                listolists[index].append(current_element)

    return list(filter(None, listolists))


def get_table_headers(table):
    """Get the table headers from a table"""
    width = 0
    headers = []

    for row in table:
        if 'class' not in row.attrs:
            break
        if 'substats_row' in row.attrs['class']:
            break
        if row.text.strip() == '':
            try:
                headers.append(row.attrs['class'][0])
            except (KeyError, IndexError):
                headers.append(f"HEADER_{width}")
        else:
            headers.append(row.text)
        width += 1

    return headers


def get_float_from_table_cell_percentage(celldata):
    """Get JSON-serializable data from VALVe's table cell percentage format"""
    try:
        return float(celldata.strip('%'))
    except ValueError:
        return None


def main():
    """Main function"""
    soup = BeautifulSoup(rget(PAGE_URL, timeout=120).content, "html.parser")

    finaljson = {}

    for table in get_list_of_tables_from_soup(soup):

        tableheaders = get_table_headers(table)
        table = table[len(tableheaders):]  # truncate headers

        data = {}
        for row in table:
            cell_index = 0
            json_data = {}
            json_key = None
            for cell in row:
                if isinstance(cell, element.Tag) and cell.name != 'br':
                    if cell_index == 0:
                        json_key = cell.text
                    else:
                        json_data[tableheaders[cell_index]] = \
                            get_float_from_table_cell_percentage(cell.text)
                    cell_index += 1
            data[json_key] = json_data
        finaljson[tableheaders[0]] = data

    with open("steam_hw_survey_videocards.json", 'w', encoding="utf8") as _fp:
        jdump(finaljson, _fp)


if __name__ == "__main__":
    main()
