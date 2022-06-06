from scraper import YouTubeScraper
import pandas as pd

ys = YouTubeScraper('https://www.youtube.com/watch?v=zxaXgNJG3xk')
ys.scrape()
data = ys.comments
replies = ys.comments['replies']  # list of dictionaries, 10th comment replies is 10th list element as a dict
data.pop('replies', None)
df = pd.DataFrame(data)
