TITLE = 'Orvis Videos'
PREFIX = '/video/orvisvideos'

ICON = 'icon-default.png'
ART = 'thetug.jpg'
URL_PATTERN = 'http://www.orvis.com/flyfishingvideos/%s/feed'

BASE_URL = 'http://www.orvis.com'
API_URL = BASE_URL + '/flyfishingvideos/'

CATEGORY_LIST = [
    {'title': 'Freshwater', 'key': 'freshwater'},
    {'title': 'Saltwater', 'key': 'saltwater'},
    {'title': 'Warmwater', 'key': 'warmwater'},
    {'title': 'Fly-Tying', 'key': 'fly-tying'},
    {'title': 'How to', 'key': 'how-to'},
    {'title': 'Gear', 'key': 'gear'},
    {'title': 'Editors Choice', 'key': 'editors-choice'}
]


####################################################################################################
def Start():
    ObjectContainer.title1 = TITLE


####################################################################################################
@handler('/video/orvisvideos', 'Orvis Videos')
def MainMenu():
    oc = ObjectContainer()
    for category in CATEGORY_LIST:
        oc.add(DirectoryObject(
            key=Callback(VideoList, title=category['title'], category=category['key']),
            title=category['title']
        ))
    return oc


####################################################################################################
def VideoList(title, category, page=1):
    oc = ObjectContainer(title2="%s: %s" % (title, str(page)))
    videos = XML.ElementFromURL(URL_PATTERN % (category))

    for video in videos.xpath('//item'):
        try:
            title = video.xpath('./title/text()')[0]
            cdata = video.xpath('./description/text()')[0]
            datael = HTML.ElementFromString(cdata)
            thumb = datael.xpath('./p[1]/img/@src')[0]
            videoinfo = datael.xpath('./p[2]/text()')[0]
            vinfo = videoinfo[1:-1]
            parts = vinfo.split()
            if "vimeo" in parts[0]:
                url = "https://vimeo.com/" + parts[1]
            else:
                url = "https://www.youtube.com/watch?v=" + parts[1]
            oc.add(VideoClipObject(
                url=url,
                title=title,
                thumb=Resource.ContentsOfURLWithFallback(url=thumb)
            ))
        except Exception:
            Log("An error occurred")
            continue
    return oc
