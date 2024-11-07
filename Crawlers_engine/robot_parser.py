import re
import requests


class RobotParser:
    def __init__(self, url=None):
        self.url = re.match(r'http(s)*://(\w|\d|\.)*/', url)
        self.robots_txt_path = ''.join([self.url.group(0), 'robots.txt']) if self.url else ''
        self.key_words = {
            "User-agent": set(),
            "Disallow": set(),
            "Allow": set(),
            "Crawl-delay": set(),
            "Request-rate": set(),
            "Visit-time": set()
        }

    def parse(self):
        if not self.robots_txt_path:
            return

        text = str(requests.get(self.robots_txt_path).text).split('\n')
        for i in range(len(text)):
            if not text[i].startswith('User-agent'):
                continue
            else:
                agent = text[i].split(': ')[1].split(' ')[0]
                if agent != '*':
                    continue
                self.key_words['User-agent'].add(agent)
                for j in range(i + 1, len(text)):
                    line = text[j]
                    if line.startswith('User-agent'):
                        break
                    if line.startswith('Allow'):
                        self.key_words["Allow"].add(line.split(': ')[1].split(' ')[0])
                    elif line.startswith('Disallow'):
                        self.key_words["Disallow"].add(line.split(': ')[1].split(' ')[0])
                    elif line.startswith('Crawl-delay'):
                        self.key_words["Crawl-delay"].add(line.split(': ')[1].split(' ')[0])
                    elif line.startswith('Request-rate'):
                        self.key_words["Request-rate"].add(line.split(': ')[1].split(' ')[0])
                    elif line.startswith('Visit-time'):
                        self.key_words["Visit-time"].add(line.split(': ')[1].split(' ')[0])
