"""Download example images.

Uses this project: https://github.com/yavuzceliker/sample-images
"""
import asyncio
import os
import aiohttp


async def main():
    """Download images."""
    await download_images("sample-images", 300, parallel=8)


async def fetch_image(session, url, dest, sem):
    """Download image."""
    async with sem:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(dest, "wb") as f:
                    f.write(await resp.read())
                print(f"Downloaded {url} -> {dest}")
            else:
                raise ValueError(f"Failed {url} (status {resp.status})")


async def download_images(outdir, n: int, parallel: int = 8):
    """Download images."""
    os.makedirs(outdir, exist_ok=True)
    sem = asyncio.Semaphore(parallel)
    base_url = "https://yavuzceliker.github.io/sample-images/image-{}.jpg"

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_image(session, base_url.format(i), os.path.join(outdir, f"image-{i}.jpg"), sem)
            for i in range(1, n + 1)
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
