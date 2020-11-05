from selenium.webdriver import Chrome
from env import tracker_links
from time import sleep
from urllib.parse import urlparse
from env import chrome_path


class SeleniumScore:
    def __init__(self, url):

        self.driver = Chrome(chrome_path)
        self.url = url
        self.driver.get(url)

        loading_elements_count = self.check_loading()
        javascript_load_state = self.check_javascript_loaded()

        self.source = self.self.driver.page_source

    def check_loading(self):
        class_items = self.driver.find_elements_by_xpath("//*[@class]")
        class_items = [i for i in class_items if "loading" in i.get_attribute("class")]
        id_items = self.driver.find_elements_by_xpath("//*[@id]")
        id_items = [i for i in id_items if "loading" in i.get_attribute("id")]
        return len(class_items) + len(id_items)

    def check_javascript_loaded(self):
        return self.driver.execute_script("return document.readyState")

    def check_for_trackers(self):
        has_tracker = False
        for i in tracker_links:
            if i in self.source:
                has_tracker = True
                break
        return has_tracker

    def check_for_font(self):
        source = self.driver.page_source
        if "@font-face" in source:
            return True
        fonts = self.driver.find_elements_by_xpath(
            "//link[(contains(@href,'font')) and (@rel='stylesheet') and (@type='text/css')]")
        if len(fonts):
            return True
        return False

    def check_autoscroll(self):
        current_height = self.driver.execute_script("return document.scrollHeight;")
        self.driver.execute_script(f'self.driver.execute_script("window.scrollTo(0, {current_height});")')
        sleep(3)
        new_height = self.driver.execute_script("return document.scrollHeight;")
        if current_height != new_height:
            return True
        return False

    def check_third_party_js(self):
        if "bootstrap" in self.source.lower():
            return True
        if "jquery" in self.source.lower():
            return True
        return False

    def check_third_party_platform(self):
        word_list = ["wordpress", "wp-content", "shopify"]
        for i in word_list:
            if i in self.source.lower():
                return True
        return False

    def has_js_script_count(self):
        source = self.driver.find_elements_by_xpath(".//source")
        source = sum([1 for i in source if i.text])
        return bool(source)

    def is_responsive(self):
        if len(self.driver.find_elements_by_xpath(".//meta[@name='viewport']")):
            return True
        if "@media" in self.source:
            return True
        link_refs = self.driver.find_elements_by_xpath(".//link[@href]")
        link_refs = [i for i in link_refs if "responsive" in i.get_attribute("href").lower()]
        if len(link_refs):
            return True
        return False

    def has_good_title(self):
        titles = self.driver.find_elements_by_xpath(".//title")
        if len(titles) != 1:
            return False
        titles = titles[0]
        if len(titles) < 6 or len(titles) > 18:
            return False
        return True

    def get_element_count(self, element_type):
        return len(self.driver.find_elements_by_xpath(f".//{element_type}"))

    def check_images(self):
        images = self.driver.find_elements_by_xpath(".//img")
        logos = [i for i in images
                 if ("logo" in i.get_attribute("src").lower()
                     or "logo" in i.get_attribute("class").lower()
                     or "logo" in i.get_attribute("id").lower()
                     )]
        thumbnails = [i for i in images
                      if ("thumb" in i.get_attribute("src").lower()
                          or "thumb" in i.get_attribute("class").lower()
                          or "thumb" in i.get_attribute("id").lower()
                          )]
        return len(images), len(logos), len(thumbnails)

    def check_links(self):
        links = self.driver.find_elements_by_xpath(".//a")
        links = [i.get_attribute("href") for i in links]
        internal_links = [i for i in links if
                          (
                                  (i.startswith("/"))
                                  or (urlparse(self.url).netloc.lower()) in i.lower()
                          )
                          ]
        return len(links), len(internal_links), len(links) - len(internal_links)

    def has_theme_installed(self):
        links = self.driver.find_elements_by_xpath("//link")
        links = [i for i in links if "theme" in i.get_attribute("@href").lower()]
        return bool(len(links))

    def start(self):

        tracker_exists = self.check_for_trackers()
        font_included = self.check_for_font()
        auto_scroll = self.check_autoscroll()
        third_party_js = self.check_third_party_js()
        third_party_platform = self.check_third_party_platform()
        has_javascript_code = self.has_js_script_count()
        is_responsive_flag = self.is_responsive()
        has_good_title = self.has_good_title()
        tag_count = self.get_element_count("*")
        h1_count = self.get_element_count("h1")
        h2_count = self.get_element_count("h2")
        h3_count = self.get_element_count("h3")
        h4_count = self.get_element_count("h4")
        h5_count = self.get_element_count("h5")
        h6_count = self.get_element_count("h6")
        h7_count = self.get_element_count("h7")
        header_count = self.get_element_count("header")
        footer_count = self.get_element_count("footer")
        iframe_count = self.get_element_count("iframe")
        table_count = self.get_element_count("table")
        form_count = self.get_element_count("form")

        image_count, logo_count, thumbnail_count = self.check_images()

        link_count, internal_link_count, external_link_count = check_links()

        has_themes = self.has_theme_installed()
