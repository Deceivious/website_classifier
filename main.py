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
     if not(status_code.startswith("2") or status_code.startswith("3")):
        return score
    try:
        robots_result = check_robots(url)
    except Exception as err:
        robots_result = str(err)
    score["robot_classification"] = robots_result
    selenium_score = SeleniumScore(url).start()
    score = {**score, **selenium_score}
    return score


def start():
    output_path = r"D:\a.tsv"
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
    else:
        df = pd.DataFrame(columns=["URL"])
    score = []
    url_list = ["http://www.iluminacionhernandezhermanos.com", "http://www.almex.com",
                "http://www.lydiasalon.com", "http://www.onlineshopmactorled.com", "http://www.angelsalon.mx",
                "http://www.colorizimohairsalón.com", "http://www.abraelec.com", "http://www.guss-roch.com.mx",
                "http://www.luckytattoos.com.mx", "http://www.kitdomiciliariotca.blogsport.mx",
                "http://www.seguridadindustrialpeso.com", "http://www.extineza.com.mx",
                "http://www.materialesdelsurete.com", "http://www.amano.com.mx", "http://www.laseratto.com.mx",
                "http://www.xavierandvicents.com.mx", "http://www.kopay.com.mx", "http://www.isainstrument.com",
                "http://www.beluxiluminacion.com", "http://www.pisaflex.com.mx", "http://www.moorsphanails.com",
                "http://www.sincroniamexico.com", "http://www.factumsecurity.com.mx", "http://www.lightmex.com.mx",
                "http://www.wix/uliseskooll/rico.com", "http://cursos-micropigmentacion.com.mx",
                "http://www.ralux.com.mx", "http://www.hubbell.com.mx", "http://www.bombassuarez.com.mx",
                "http://www.mostbeautiful.com.mx", "http://imbimora.wix.com/aura_beautyspa",
                "http://www.bomberfire.com", "http://www.bronceadoexpress.com", "http://www.corpslam.com",
                "http://www.cncser.com.mx", "http://www.tarengo.com", "http://www.esteticasaloncarmela.com"]
    try:
        ll = len(url_list)
        for idx, i in enumerate(url_list):
            print(idx / ll * 100, i)
            if i in df["URL"]:
                continue
            score.append(get_score(i))
    except:
        raise
    finally:
        pd.concat([df, pd.DataFrame(score)]).to_csv(output_path, index=False)


start()
