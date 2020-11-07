from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError
import re


def get_status_code(url):
    if url.count("\.") == 1:
        url = "www." + url
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.get(url, headers={"User-Agent": "XY"})
    except Exception as err:
        return Exception(f"Exception:{str(err)}")
    res_code = str(response.status_code)
    return res_code


def check_robots(url):
    parsed_uri = urlparse(url)
    host_url = f'{parsed_uri.scheme}://{parsed_uri.netloc}'
    sitemap_flag = False
    for sitemap_ending in ["/sitemap.xml", "/sitemap", "/sitemap_index.xml"]:
        sitemap = host_url + sitemap_ending
        try:
            response = requests.get(sitemap, headers={"user-agent": "XY"})
        except ConnectionError:
            return "Request Error."
        except Exception as err:
            print(type(err))
            raise
        if response.status_code == 200:
            if "<html" not in str(response.content):
                sitemap_flag = True
                break
    if sitemap_flag:
        res = str(response.content)
        if "loc" in res:
            res = res.replace("\n", "").replace("\r", "")
            res = re.findall(r'<loc(.*?)</loc>', res)
            res = [i.split(">")[1] for i in res]

            if not len(res):
                raise Exception("Malformed sitemap.")

            inner_sitemaps = [i for i in res if i.endswith(".xml")]
            if len(inner_sitemaps):
                return "Multiple Inner sitemaps in sitmeap."
            else:
                return "Multiple Pages in sitemap."
        else:
            raise Exception("No loc in sitemap.")

    else:
        robots = host_url + "/'robots.txt"
        response = requests.get(robots, headers={"user-agent": "XY"})
        if response.status_code == 404:
            raise Exception("No robots.")
        else:
            if "sitemap" in str(response.content):
                raise Exception("Sitemap found in robots.")
            else:
                raise Exception("Robot found but no sitemap.")
