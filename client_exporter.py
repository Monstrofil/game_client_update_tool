#!/usr/bin/python
# coding=utf-8
import argparse
import os
import subprocess
import tempfile

import requests

from lxml import etree
from subprocess import Popen

__author__ = "Aleksandr Shyshatsky"


class UpdatesHelper(object):

    def __init__(self):
        pass

    def retrive(self):
        self.__retrive()

    def __retrive(self):
        links = self.__obtain_links_wgpkg()
        files = []
        for link in links:
            files.append(self.__retrive_file(link))
        print(files)
        try:
            for file in files:
                if file.endswith('001'):
                    Popen(
                        ['7z', 'x', file, '-oGAME']).communicate()
                    break
            else:
                raise Exception
        except:
            raise
        finally:
            for file in files:
                os.unlink(file)

    def __obtain_links_wgpkg(self):
        """
        I really don't know what is the difference between these links, so I just download one ;)
        <http name="Cedexis">
            http://dl-wows-cdx.wargaming.net/ru/patches/wows_0.6.7.0.261848_ru/wows.ru_0.6.7.0.261848_locale_be.wgpkg
        </http>
        <http name="G-Core">
            http://dl-wows-gc.wargaming.net/ru/patches/wows_0.6.7.0.261848_ru/wows.ru_0.6.7.0.261848_locale_be.wgpkg
        </http>
        <web_seeds>
            <url threads="10">
                http://dl-wows-gc.wargaming.net/ru/patches/wows_0.6.7.0.261848_ru/wows.ru_0.6.7.0.261848_locale_be.wgpkg
            </url>
        </web_seeds>
        :rtype: str
        """
        url = "http://update.worldofwarships.ru"
        data = dict(
            target='client',
            client_ver='unknown'
        )
        xml = requests.get(url, data).content
        links = etree.fromstring(xml).xpath('content/file/web_seeds/url/text()')

        return links

    def __retrive_file(self, link):
        """
        Retrives wgpkg file, exports .mo;
        Returns link to exported .mo file;
        :type link: str 
        :rtype: str 
        """

        Popen(
            ['bash', '-c', 'wget %s' % link]).communicate()
        filename = os.path.basename(link)
        return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    namespace = parser.parse_args()
    locale_helper = UpdatesHelper()
    locale_helper.retrive()
