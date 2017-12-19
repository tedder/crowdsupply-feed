#!/usr/bin/env python3

# MIT license, see /LICENSE

import boto3
import json
import requests
import lxml
import lxml.html

# using the JSON feed spec: https://jsonfeed.org/version/1

SITE_URL = 'https://www.crowdsupply.com'
BROWSE_URL = SITE_URL + '/browse'
S3_KEY = 'rss/crowdsupply-browse.json'
FEED_URL = 'https://dyn.tedder.me/' + S3_KEY


def get_only_one(item):
  if len(item) != 1:
    raise Exception("we wanted one item but instead got {} of them.".format(len(item)))
  return item[0]


def parse_tile(tile):
  ret = {}
  ret['url'] = SITE_URL + tile.get('href')
  ret['id'] = tile.get('href')
  ret['image'] = SITE_URL + tile.xpath('img')[0].get('src')
  overview = get_only_one(tile.xpath("div[contains(@class, 'project-tile-overview')]"))
  ret['title'] = get_only_one(overview.xpath("h3")).text

  overview_text = []
  for opara in overview.xpath("p"):
    overview_text.append(opara.text)
  overview_text.append('<img src="{}" border=0>'.format(ret['image']))
  ret['content_html'] = "<br>\n".join(overview_text)

  return ret


r = requests.get(BROWSE_URL)
browse_text = r.text
if len(browse_text) < 10000: # currently around 41k bytes
  raise Exception("page was much smaller than expected, got {} bytes. url: {}".format(len(browse_text), BROWSE_URL))
tree = lxml.html.fromstring(browse_text)

browse_container = tree.xpath("//section[contains(@class, 'section-browse')]//a[contains(@class, 'project-tile')]")

jfeed = {
  'version': 'https://jsonfeed.org/version/1',
  'title': 'Crowd Supply projects',
  'home_page_url': BROWSE_URL,
  'description': 'Projects scraped from the crowdsupply browse page',
  'user_comment': 'If dates/creator/funding level is needed, I can scrape the child pages too. Probably worth caching if so.',
  'author': {'name': 'tedder', 'url': 'https://tedder.me/' },
  'feed_url': FEED_URL,
  'items': [],
}
for tile in browse_container:
  tileinfo = parse_tile(tile)
  jfeed['items'].append(tileinfo)

feedj = json.dumps(jfeed)

s3 = boto3.client('s3')
s3.put_object(
  ACL='public-read',
  Body=feedj,
  Bucket='dyn.tedder.me',
  Key=S3_KEY,
  ContentType='application/json',
  CacheControl='public, max-age=300' # todo: 3600
)



