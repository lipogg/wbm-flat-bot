# WBM Flat Bot

Python bot that automates flat search and application for flats by WBM Wohnungsbaugesellschaft Berlin-Mitte. 

## Features 

- Search flats by zip code, flat size, minimum room number, maximum rent (more to come)
- Filter flats by net household income and net base rent ratio. WBM only considers applicants with net household income between 15% and 30% of the net base rent: https://www.antidiskriminierungsstelle.de/SharedDocs/praxisbeispiele/DE/wohnungsmarkt/praxisbeispiel-wbm.html
- Apply automatically via application form and log applications

This bot tries to scrape flats responsibly by offering more filter options than preexisting wbm flat bots, without sacrificing too much speed, since speed is crucial for being considered in the WBM application process. 