import asyncio
import aiohttp

URLS=[
    "https://example.com/",
    "https://www.python.org/",
    "https://httpbin.org/delay/1"
]

async def fetch(session,url,sem,retries=2):
    async with sem:
        for attempt in range(retries+1):
            try:
                async with session.get(url,timeout=aiohttp.ClientTimeout(total=10)) as r:
                    text=await r.text()
                    return {"url":url,"status":r.status,"bytes":len(text.encode())}
            except (aiohttp.ClientError,asyncio.TimeoutError) as exc:
                if attempt==retries:return {"url":url,"error":str(exc)}
                await asyncio.sleep(2**attempt)

async def main():
    sem=asyncio.Semaphore(3)
    async with aiohttp.ClientSession(headers={"User-Agent":"portfolio-learning-scraper/1.0"}) as session:
        results=await asyncio.gather(*(fetch(session,u,sem) for u in URLS))
    for result in results: print(result)

if __name__=="__main__": asyncio.run(main())
