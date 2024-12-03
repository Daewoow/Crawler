from Crawlers_engine.robot_parser import RobotParser


def test_robot_parser():
    needed = {"User-agent": {"*"},
              "Disallow": {"/goto_issue/", "/soft/punto/win/uninstall/*", "/edu/test", "/advanced_engl.html",
                           "/yandsearch", "/collections/iznanka/", "/adfox/", "/video/v$", "/games/*?*pageId*",
                           "/promo/launcher/feedback", "/weather/*"},
              "Allow": {"/video/dizi-izle/?", "/gorsel/touch/?*", "/blogs/pad$", "/gorsel/smart/$", "/maps/*?lang=uz$"},
              "Crawl-delay": set(), "Request-rate": set(), "Visit-time": set()}

    parser = RobotParser("https://yandex.ru/")
    parser.parse()
    if all(needed[field] in parser.key_words[field] for field in needed.keys()):
        assert False
    assert True
