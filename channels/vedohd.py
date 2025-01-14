# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canale per vedohd
# ------------------------------------------------------------

from core import scrapertoolsV2, httptools, support
from core.item import Item
from platformcode import logger, config
from specials import autoplay

__channel__ = "vedohd"
host = config.get_channel_url(__channel__)
headers = ""

IDIOMAS = {'Italiano': 'IT'}
list_language = IDIOMAS.values()
list_servers = ['verystream', 'openload', 'streamango', 'wstream']
list_quality = ['HD', 'SD']

#esclusione degli articoli 'di servizio'
blacklist = ['CB01.UNO &#x25b6; TROVA L&#8217;INDIRIZZO UFFICIALE ', 'AVVISO IMPORTANTE – CB01.UNO', 'GUIDA VEDOHD']

@support.menu
def mainlist(item):

    film = [
        ('I più votati', ["ratings/?get=movies", 'peliculas']),
        ('I più popolari', ["trending/?get=movies", 'peliculas']),
        ('Generi', ['ratings/?get=movies', 'menu', 'genres']),
        ('Anno', ["", 'menu', 'releases']),
    ]
    return locals()


def search(item, text):
    logger.info("[vedohd.py] " + item.url + " search " + text)
    item.url = item.url + "/?s=" + text

    return support.dooplay_search(item, blacklist)


def peliculas(item):
    return support.dooplay_films(item, blacklist)


def findvideos(item):
    itemlist = []
    for link in support.dooplay_get_links(item, host):
        if link['title'] != 'Trailer':
            logger.info(link['title'])
            server, quality = scrapertoolsV2.find_single_match(link['title'], '([^ ]+) ?(HD|3D)?')
            if quality:
                title = server + " [COLOR blue][" + quality + "][/COLOR]"
            else:
                title = server
            itemlist.append(
                Item(channel=item.channel,
                     action="play",
                     title=title,
                     url=link['url'],
                     server=server,
                     fulltitle=item.fulltitle,
                     thumbnail=item.thumbnail,
                     show=item.show,
                     quality=quality,
                     contentType=item.contentType,
                     folder=False))

    autoplay.start(itemlist, item)

    return itemlist


@support.scrape
def menu(item):
    patron = '<a href="(?P<url>[^"#]+)"(?: title="[^"]+")?>(?P<title>[a-zA-Z0-9]+)'
    patronBlock = '<nav class="' + item.args + '">(?P<block>.*?)</nav>'
    action = 'peliculas'

    return locals()


def play(item):
    logger.info("[vedohd.py] play")

    data = support.swzz_get_url(item)

    return support.server(item, data, headers=headers)
