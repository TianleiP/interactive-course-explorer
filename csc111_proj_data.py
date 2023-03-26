"""
scrap the course data from uoft website
"""
from typing import Any

import bs4
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import xlwt

find_name = re.compile(r'<h3 class="js-views-accordion-group-header"> (.*?)</h3>')
find_detail = re.compile(r'<div class="views-field views-field-body">(.*?)'
                         r'<span class="views-field views-field-field-method-of-delivery">')
find_prerequisite = re.compile(r'Prerequisite(.*?)</span>')
find_exclusion = re.compile(r'Exclusion(.*?)</span>')
find_core = re.compile(r'Corequisite(.*?)</span>')


def main():
    """main """
    baseurl = "https://artsci.calendar.utoronto.ca/section/Statistical-Sciences"

    datalist = get_data(baseurl)
    savepath = "sta_course.xls"
    save_data(datalist, savepath)

    # ask_url(baseurl)


def ask_url(url: str) -> str:
    """ask usrl"""
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv: 100.0) Gecko / 20100101 Firefox / 100.0"
    }

    request = urllib.request.Request(url, headers=head)

    html = " "
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def get_data(baseurl: str) -> Any:
    """scrap data"""

    datalist = []

    html = ask_url(baseurl)

    soup = BeautifulSoup(html, "html.parser")

    content = soup.find_all('div', class_="view-content")[-1]

    names = re.findall(find_name, str(content))

    details = re.findall(find_detail, str(content))

    for i in range(len(details)):
        data = [names[i]]
        item = str(details[i])

        prerequisite = re.findall(find_prerequisite, item)
        if len(prerequisite) == 1:
            data.append(delete_string(prerequisite)[0])
        else:
            data.append(" ")

        exclusion = re.findall(find_exclusion, item)
        if len(exclusion) == 1:
            data.append(delete_string(exclusion)[0])
        else:
            data.append(" ")

        core = re.findall(find_core, item)
        if len(core) == 1:
            data.append(delete_string(core)[0])
        else:
            data.append(" ")

        datalist.append(data)

    return datalist


def delete_string(lst: list) -> list:
    """delete string"""

    lst[0] = re.sub(': </strong><span class="field-content">', "", lst[0])
    lst[0] = re.sub(' <a href="/course/(.*?)">', "", lst[0])
    lst[0] = re.sub('<a href="/course/(.*?)">', "", lst[0])
    lst[0] = re.sub('<span><span>', "", lst[0])
    lst[0] = re.sub('<a href="https:(.*?)</a>', "", lst[0])
    lst[0] = re.sub(',  ', "", lst[0])
    lst[0] = re.sub('/  ', "", lst[0])
    lst[0] = re.sub('</a>', "", lst[0])
    lst[0] = re.sub(';', ",", lst[0])
    lst[0] = re.sub('  ', " ", lst[0])
    return lst


def save_data(datalist: list, savepath: str) -> None:
    """save data"""
    print("save....")
    book = xlwt.Workbook(encoding="uft-8", style_compression=0)
    sheet = book.add_sheet('statistics', cell_overwrite_ok=True)
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(len(data)):
            sheet.write(i, j, data[j])

    book.save(savepath)


if __name__ == "__main__":
    main()
