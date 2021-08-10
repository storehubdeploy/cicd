#!/usr/bin/env python3
# coding:utf-8
import os
import sys
import configparser
from optparse import OptionParser
import requests, json
sys.path.append("/data/ops/ci/libs")
from common import print_color

def generate_png(app,env,branch,revision):
    import time
    import git
    from PIL import Image, ImageDraw, ImageFont
    # General Params
    lib_path="/data/ops/ci/for_monitor/libs"
    png_path="/data/share/workplacechat"
    img = '{}/template.png'.format(lib_path)
    font_title = '{}/title.ttf'.format(lib_path)
    font_content = '{}/content.ttf'.format(lib_path)
    title_font = ImageFont.truetype(font_title, 40)
    content_font = ImageFont.truetype(font_content, 20)
    content_font_small = ImageFont.truetype(font_content, 14)
    new_img_name = "{}_{}.png".format(time.time(),app)
    new_img_path = '{}/{}'.format(png_path,new_img_name)
    title = "Notice Board"
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # open
    image = Image.open(img)
    w, h  = image.size
    draw = ImageDraw.Draw(image)
    width, height = image.size
    # Draw
    ## title
    title_x = 8
    title_y = 5
    draw.text((title_x, title_y), u'%s' % title, "#F5F5F5", title_font)
    ## content
    content_x = 8
    content_y = 50
    draw.text((content_x, content_y), u'%-8s %s' % ("Date",current_time), "#696969", content_font)
    content_y = 75
    draw.text((content_x, content_y), u'%-8s %s' % ("App",app), "#696969", content_font)
    content_y = 100
    draw.text((content_x, content_y), u'%-8s %s' % ("Env",env), "#696969", content_font)
    if branch:
        content_y = 125
        draw.text((content_x, content_y), u'%-8s %s' % ("Branch",branch), "#696969", content_font)
    if revision:
        content_y = 150
        draw.text((content_x, content_y), u'%-8s %s' % ("Revision",revision[0:15]), "#696969", content_font)
        repo = git.Repo(os.getenv("WORKSPACE"))
        content_y = 175
        draw.text((content_x, content_y), u'%s' % repo.git.log('-1','--pretty=format:%s')[0:50], "#696969", content_font_small)
            
    # generate
    width = int(w / 1.4)
    height = int(h / 1.4)
    compress = image.resize((width, height), Image.ANTIALIAS)
    compress.save(new_img_path, 'png')
    #image.save(new_img_path, 'png')
    return new_img_name

def send_to_group():
    # Send message
    parser = OptionParser()
    parser.add_option("--app"   , dest="app"   , default=None)
    parser.add_option("--env"   , dest="env"   , default=None)
    parser.add_option("-t"      , dest="addr"  , default=None)

    (options, args) = parser.parse_args()

    # config
    app   = options.app
    env   = options.env
    addr  = options.addr

    if 't_' in addr:
        thread_type="thread_key"
    else:
        thread_type="id"
    #generate_png
    new_img_name = generate_png(app,env,branch=os.getenv("GIT_BRANCH"),revision=os.getenv("GIT_COMMIT"))
    image_url = "https://share.shub.us/workplacechat/{}".format(new_img_name)

    # init
    PAGE_ACCESS_TOKEN='DQVJ1RFhaWUxaNlRyZAHQ0bVZAKYzlPMUxZAY1ZAHNzROamxzN2FnYW9EMk9OWkFYYnZAtdlRzazZARbndqMzZAYWjljTGQxWHp6WHU0OEVfckV1RkdBcEdieFNILVhlbDJYZAUtqQWY2UTBCaGxGc182YS1saWdvTVoyd3h6SmFla0xCYU5yV3ZA6VTdPVkQ4a2RmNGxkWjFtUTN4Si1tRnBZANzF2N05mdXRLN2I3Mk1XOGVGb3N5cUdYaDFtSjVGdjRFV20wVWhSTzJB'
    data={
            "recipient":{thread_type:addr},
            "message":{
                "attachment":{
                    "type":"image",
                    "payload":{
                        "url":image_url,
                        "is_reusable":"false"
                    }
                }
            }
        }
    post_data = json.dumps(data)
    url = "https://graph.facebook.com/me/messages"
    headers = {'Content-Type': 'application/json'}
    payload = {'access_token':PAGE_ACCESS_TOKEN}
    try:
        r = requests.post(url, headers=headers, params=payload, data=post_data)
        r.raise_for_status()
    except requests.RequestException as e:
        print_color(31,e)
    else:
        print_color(32,r.json())

if __name__ == "__main__":
    send_to_group()
