# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, SoupStrainer
import webbrowser
from wox import Wox,WoxAPI
import urllib.parse

### Icon Source ###
### Icon made by Freepik from www.flaticon.com ###


class ReleaseDate(Wox):

    def request(self,url):
        # Proxy setup for Wox
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
          proxies = {
            "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
            "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
          return requests.get(url,proxies = proxies)
        else:
          return requests.get(url)

    def query(self,keyword):

        # search keyword at release-date.info
        r = self.request('http://release-date.info/?s=' + urllib.parse.quote(keyword))

        # title and url are inside an h2 tag
        bs = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer("h2"))

        i = 0
        results = []
        for result in bs.find_all('h2'):
            # result only valid with 'a' tag
            if result.a:
                title = result.text
                url = result.a.get('href')
                subtitle = self.getSubtitle(url)

                results.append({
                    "Title": title,
                    "SubTitle": subtitle,
                    "IcoPath":"Images\\calendar.png",
                    "JsonRPCAction":{
                      "method": "openUrl",
                      "parameters":[url],
                      "dontHideAfterAction":False
                    }
                })

                # limit results to 4
                i+=1
                if i >= 4:
                    break

        if len(results) == 0:
            results.append({
                "Title": "No Results found",
                "SubTitle": "",
                "IcoPath":"Images\\calendar.png"
            })

        return results

    # request site where we can find specific release infos inside an h5 tag
    def getSubtitle(self, url):
        info_request = self.request(url)
        info = BeautifulSoup(info_request.text, "html.parser", parse_only=SoupStrainer("h5")).find('h5')

        return info.text if info else "No release information found"

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    ReleaseDate()
