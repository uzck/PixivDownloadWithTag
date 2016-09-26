# PixivDownloadWithTag
A tool use to download images on Pixiv by tags. Use the API provied by ``PixivPy`` [upbit/pixivpy](https://github.com/upbit/pixivpy)  
So please use ``pip install PixivPy`` to download the support.  
You can change the target_score to filter images. And now I hide the pic with tag ``R-18``. If you want to download R-18 pic, just remove``and (not(u'R-18' in illust.tags))``
