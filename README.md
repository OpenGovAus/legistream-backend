# legistream_backend

This is the Python backend for legistream.

---

Install with **pip**:

`pip install legistream-backend`

View project on PyPI: [https://pypi.org/project/legistream-backend/](https://pypi.org/project/legistream-backend/).

## Usage

This package uses different modules to get live stream data from the various Australian parliaments.

**Currently supported parliaments:**

- Australian Capital Territory
- Federal
- New South Wales
- Northern Territory
- South Australia
- Tasmania
- Victoria
- Western Australia

### Setup

Install required packages with **pip3**:

`pip3 install -r requirements.txt`

---

Install **ffmpeg**:

#### Linux

`sudo apt install ffmpeg`

#### Mac

Install with **brew**:

`brew install ffmpeg`

#### Windows

Official Windows builds of **ffmpeg** can be found [here](https://ffmpeg.org/download.html#build-windows)

### Print out stream URLs:

Every parliament module returns data the same way, Victoria is used here only for example purposes.

The `stream_urls` property can be used to return streams as a **dict**:

```python
from legistream_backend.vic import Stream

print(Stream().stream_urls)
```

Each URL can be returned individually by using the `[house]_stream_url` property (e.g `lower_stream_url`)

```python
print(Stream().lower_stream_url)
```

### Check if a parliament's house is live:

Similarly, you can check the status of a live stream with the `[house]_is_live` boolean property.

```python
if(Stream().lower_is_live):
    print('The lower house of Victoria is currently live.')
else:
    print('The lower house of Victoria is not currently live.')
```

## Notes

The South Australia stream extractor uses code adapted from the [streamlink ustreamtv implementation](https://github.com/streamlink/streamlink/blob/master/src/streamlink/plugins/ustreamtv.py).