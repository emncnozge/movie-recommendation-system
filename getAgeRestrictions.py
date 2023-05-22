import asyncio
import aiohttp
from lxml import html
import json


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def process_movie(session, semaphore, movie):
    async with semaphore:
        url = 'https://www.imdb.com/title/' + movie["imdb_id"]
        response_text = await fetch(session, url)
        tree = html.fromstring(response_text)

        xpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a'
        selected_element = tree.xpath(xpath)

        if selected_element:
            adult = selected_element[0].text
            movie["adult"] = adult
        else:
            print(movie["imdb_id"], "XPath değeri bulunamadı.")


async def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    with open("movie_info.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    semaphore = asyncio.Semaphore(10)  # En fazla 20 talep yapılacak

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for movie in movies:
            tasks.append(process_movie(session, semaphore, movie))

        await asyncio.gather(*tasks)

    with open("movie_info.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4, sort_keys=False)

asyncio.run(main())
