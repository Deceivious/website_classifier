from selenium_quantifier import SeleniumScore
from request_quantifier import check_robots, get_status_code


def fix_url(url):
    if url.count(".") == 1:
        url = "www." + url
    if not url.startswith("http"):
        url = "http://" + url
    return url


def get_score(url):
    url = fix_url(url)
    status_code_score, status_code = get_status_code(url)
    if status_code is None:
        return 0
    robots_result = check_robots(url)
    return robots_result
    SeleniumScore(url)


for i in """abf.bigya
00wwwspotfy.com
abogadosinnovacionjuridica.com
adesiscontrol.com
alambradoselreal.com
alaskaviajes.com
alexromeroblog.com
alfredomayacatering.com
alsegrupo.com
antsanch.com
appsatelite.com
aramreposteria.com
archsensus.com
autodineroprestamossobreauto.com
autopartesdesantiago.com
bacanavillasmazamitla.com
bankiia-acceso-clientes.com
baum-mkt.com
benchmarkingsalon.com
cancunpropertyinvestment.com
caninemirroring.com
capacitacion-educa.com
catepra.com
cdfgty.club
cherryideas.com
chuntachis.com
cibelisa.com""".split("\n"):
    try:
        print(i, get_score(i))
    except Exception as err:
        print(i, str(err))
    print("=======================================")
