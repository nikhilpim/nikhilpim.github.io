#!python3

import json
import inspect

head_html = """
    <head>
        <title>Nikhil Pimpalkhare</title>
        <meta charset="UTF-8">
        <meta name="description" content="Nikhil Pimpalkhare's academic website.">
        <meta name="author" content="Nikhil Pimpalkhare">
        <link href="https://fonts.googleapis.com/css?family=Muli" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="main.css">
        <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16x16.png">
    </head>
"""

# Define functions for pieces
def build_news(news, count):
    print("Adding news:")
    news_list = ""

    for n in news[:count]:
        print(n["date"])
        item = '<div class="news-item">'
        item += '<div class="news-date">' + n["date"] + '</div>'
        item += '<div class="news-text">' + n["text"] + '</div>'
        item += '</div>\n            '
        news_list += item

    if (count != len(news)):
        item = '<br>'
        item += '<div class="news-item">'
        item += '<div class="news-date">' + " " + '</div>'
        item += '<div class="news-text">' + "<a href=\"./news.html\">See news from " + news[-1]["date"] + " to " + news[0]["date"] + '</a></div>'
        item += '</div>\n            '
        news_list += item

    news_html = """
    <div class="section">
        <h1>News</h1>
        <div class="hbar"> </div>
        <div id="news">
            %s
        </div>
    </div>
    """ % (news_list)
    return news_html

def build_pubs(pubs, kind):
    print("\nAdding full publications:")
    pubs_list = ""

    for p in pubs:
        if kind in p["tags"]:
            print(p["title"])
            item = '<div class="paper">'
            item += '<div class="conference">' + p["conference"] + '</div>'
            item += '<div class="citation">'
            item += '<a href=\"' + p["link"] + '\">' + p["title"] + '</a> ' if p["link"] else p["title"] + " "
            item += '<br>' + p["authors"]
            item += '<br><small>(' if p["code"] or p["slides"] else ""
            item += '<a href ="' + p["code"] + '">Supplemental Material</a>' if p["code"] else ""
            item += ', <a href="' + p["slides"] + '">Presentation</a>' if p["slides"] else ""
            item += ')</small>' if p["code"] or p["slides"] else ""
            item += '</div>'
            item += '</div>\n            '
            pubs_list += item

    title = "Conference Papers" if kind == "full" else "Workshop & Short Papers"

    pubs_html = """
    <div class="section">
        <h1>%s</h1>
        <div class="hbar"> </div>
        <div id="%spublications">
            %s
        </div>
    </div>
    """ % (title, kind, pubs_list)
    return pubs_html

def build_profile(profile):
    profile = profile[0]
    profile_html = """
    <div class="profile">
        <div class="profile-left">
            <abbr title=\"Me!\">
            <img class="headshot" src="%s" alt="Missing Image"/>
            </abbr>
            %s
            <p>Here is my
                <a href="%s">CV</a> and
                <a href="%s">Google Scholar</a>.
            You can reach me at %s.
            </p>
        </div>
    </div>
    """ % (profile["headshot"], profile["blurb"], profile["cv"], profile["scholar"], profile["email"])
    return profile_html

def add_links(html, links):
    links = links[0]
    print("\nAdding links:")
    for name in links.keys():
        if name in html:
            print(name)
            html = html.replace(name, "<a href=\"%s\">%s</a>" % (links[name], name))
    return html

def build_index(profile_json, news_json, pubs_json, links):
    body_html = """
    <body>
        <div class="hbar"></div>
        %s
        </br>
        %s
        %s
        %s

        <p align=right style=\"font-size:14px\"> Site template courtesy of Federico Mora </p>
    </body>
    """ % (build_profile(profile_json), build_news(news_json, 5), build_pubs(pubs_json, "full"), build_pubs(pubs_json, "short"))

    index_html = """
    <!DOCTYPE html>
    <html lang="en">
    %s
    %s
    </html>
    """ % (head_html, body_html)

    return inspect.cleandoc(add_links(index_html, links))

def build_news_site(news_json, links):
    body_html = """
    <body>
        %s
    </body>
    """ % (build_news(news_json, len(news_json)))

    news_html = """
    <!DOCTYPE html>
    <html lang="en">
    %s
    %s
    </html>
    """ % (head_html, body_html)

    return inspect.cleandoc(add_links(news_html, links))

### Load json files
with open('includes/auto_links.json') as f:
    auto_links_json = json.load(f)

with open('includes/profile.json') as f:
    profile_json = json.load(f)

with open('includes/news.json') as f:
    news_json = json.load(f)

with open('includes/pubs.json') as f:
    pubs_json = json.load(f)

# Write to files
with open('index.html', 'w') as index:
    index.write(build_index(profile_json, news_json, pubs_json, auto_links_json))

with open('news.html', 'w') as index:
    index.write(build_news_site(news_json, auto_links_json))
