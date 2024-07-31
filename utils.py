import aiohttp


async def get_video_url(api_url, headers, querystring):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers, params=querystring) as response:
            if response.status == 200:
                data = await response.json()
                if data['success']:
                    if 'links' in data:
                        if isinstance(data['links'], list):
                            video_url = next((link['link'] for link in data['links'] if link['quality']
                                             == 'video_hd_original' or link['quality'] == 'video_hd_original_0'), None)
                            if not video_url:
                                video_url = next(
                                    (link['link'] for link in data['links'] if 'video' in link['quality'].lower()), None)
                        elif isinstance(data['links'], dict):
                            video_url = next((link for quality, link in data['links'].items(
                            ) if 'video' in quality.lower()), None)
                        return video_url
    return None


async def download_video(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
    return None
