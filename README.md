# WBM Flat Bot

Python bot that automates flat search and application for flats by WBM Wohnungsbaugesellschaft Berlin-Mitte. 

## Features 

- Search flats by zip code, flat size, minimum room number, maximum rent (more to come)
- Filter flats by net household income and net base rent ratio. WBM only considers applicants with net household income between 15% and 30% of the net base rent: https://www.antidiskriminierungsstelle.de/SharedDocs/praxisbeispiele/DE/wohnungsmarkt/praxisbeispiel-wbm.html
- Apply automatically via application form and log applications

It is not yet possible to search for WBS flats, but this feature will be implemented soon.

This bot tries to scrape flats responsibly by offering more filter options than preexisting wbm flat bots, without sacrificing too much speed, since speed is crucial for being considered in the WBM application process. 

## Usage

1. Fork this repo 
2. In your forked repository, go to *Settings* -> *Secrets and variables* -> *Actions* -> *Secrets* and set up a new *Repository secret* called `USER_CONFIG`. Paste the content of the sample config.yaml file in the window and adapt to your needs (replace email, name, search criteria). 
3. Go to repository *Actions* tab and verify that everything is running correctly. It may take a few minutes until the scheduled run is triggered, but you can also trigger the run manually if you don't want to wait. Once the first run is complete, click on the run, scroll down to *Artifacts* and download logs (the artifact is called `scraper-logs`). `flats.log` contains flats that have been applied to. This is empty if no flats were found. `app.log` logs scraping process and flats that did not match criteria. 

Although the workflow is scheduled to run every 5 minutes, GitHub Actions may experience server-side delays, so the actual interval is closer to 15 minutes.

