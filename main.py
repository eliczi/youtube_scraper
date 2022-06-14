from scraper import YouTubeScraper
from analysis import TextAnalysis


def main():
    yt = YouTubeScraper('https://www.youtube.com/watch?v=WTs3CKAIkVs')
    yt.scrape()
    ta = TextAnalysis('df.csv')
    ta.analyse()


if __name__ == '__main__':
    main()
