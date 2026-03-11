# Reddit Trend Scraper

Scrapes trending posts from any subreddit and exports to a clean CSV file. No API key or Reddit account required.

## Features

- Fetches posts by `hot`, `top`, `new`, or `rising`
- Exports rank, title, score, upvote ratio, comment count, awards, author, timestamps, and URLs
- Console summary preview (top 10 posts)
- Auto-generates output filename if not specified
- Polite rate limiting built in

## Requirements

Python 3.9+ — no external libraries needed (uses only the standard library).

## Usage

```bash
# Basic — scrapes top 25 hot posts from r/python
python scraper.py

# Custom subreddit and sort
python scraper.py --subreddit technology --sort top --limit 50

# Custom output file
python scraper.py --subreddit investing --limit 100 --output investing_trends.csv
```

## Output

CSV with columns: `rank`, `title`, `author`, `score`, `upvote_ratio`, `comments`, `awards`, `flair`, `is_nsfw`, `url`, `external_url`, `created_utc`, `scraped_at`

## Example

```
$ python scraper.py --subreddit MachineLearning --sort hot --limit 10

[*] Scraping r/MachineLearning (hot, 10 posts)...

============================================================
  r/MachineLearning — Top 10 posts
============================================================
     4821 pts | New benchmark shows GPT-5 matching human exp...
     2103 pts | We open-sourced our entire training pipeline...
  ...
============================================================

[OK] Exported 10 posts → r_MachineLearning_hot_20260311_041500.csv
```
