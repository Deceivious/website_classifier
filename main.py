import os

import pandas as pd
from selenium_quantifier import SeleniumScore

from request_quantifier import check_robots, get_status_code


def fix_url(url):
    if url.count(".") == 1:
        url = "www." + url
    if not url.startswith("http"):
        url = "http://" + url
    return url


def get_score(url):
    original_url = url
    url = fix_url(url)
    status_code = str(get_status_code(url))
    score = {"URL": original_url, "status_code": str(status_code)}
    if not (status_code.startswith("2") or status_code.startswith("3")):
        return score

    try:
        robots_result = check_robots(url)
    except Exception as err:
        robots_result = str(err)
    score["robot_classification"] = robots_result
    selenium_score = SeleniumScore(url).start()
    score = {**score, **selenium_score}
    return score


def start(input_path, url_header, offset=0):
    if input_path.endswith("tsv"):
        url_list = pd.read_csv(input_path, sep="\t")[url_header]
    if input_path.endswith("tsv"):
        url_list = pd.read_csv(input_path)[url_header]
    if input_path.endswith("xlsx"):
        url_list = pd.read_excel(input_path)[url_header]
    url_list = list(url_list)
    output_path = r"D:\a.tsv"
    if os.path.exists(output_path):
        df = pd.read_csv(output_path, sep="\t")
    else:
        df = pd.DataFrame(columns=["URL"])
    score = []

    ll = len(url_list)
    success_count = 0
    for idx, i in enumerate(url_list):
        if idx < offset:
            continue
        if i in df["URL"].values:
            print(idx, idx / ll * 100, i, "completed")
            continue
        else:
            print(idx, idx / ll * 100, i)
        try:
            score.append(get_score(i))
        except:
            continue
        else:
            success_count += 1
            if success_count == 10:
                success_count = 0
                df = pd.concat([df, pd.DataFrame(score)])
                df = df.drop_duplicates(["URL"])
                df.to_csv(output_path, index=False, sep="\t")
                score = []
    pd.concat([df, pd.DataFrame(score)]).to_csv(output_path, index=False, sep="\t")


if __name__ == "__main__":
    start(r"D:\2019-Cleaned_Database.xlsx", "domain_name", 10_000)
