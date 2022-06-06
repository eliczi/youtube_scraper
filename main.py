from scraper import YouTubeScraper

def main(line=None, sort_by=None):
    yt = YouTubeScraper('https://www.youtube.com/watch?v=QuTW_jbiYhM&t=325s')
    yt.scrape()


if __name__ == '__main__':
    main()
