# legistream_backend

This is the Python backend for Legistream.

---

Install with `pip3`:

`pip3 install legistream-backend`

View project on PyPI: [https://pypi.org/project/legistream-backend/](https://pypi.org/project/legistream-backend/).

## Info

This package uses different modules to get live stream data from the various Australian parliaments.

**Currently supported parliaments:**

- Australian Capital Territory
- Federal
- New South Wales
- Northern Territory
- Queensland

### Setup

1. Install `poetry`:

    ```sh
    pip3 install poetry
    ```

2. Install/update dependencies with `poetry`:

    ```sh
    poetry update
    ```

3. Install **ffmpeg**:

    #### Linux

    `sudo apt install ffmpeg`

    #### Mac

    Install with **brew**:

    `brew install ffmpeg`

    #### Windows

    Official Windows builds of **ffmpeg** can be found [here](https://ffmpeg.org/download.html#build-windows)

### Usage

#### Interpreting the streams

Every parliament module returns data as a list of `StreamModel` objects. Each `StreamModel` has these 3 properties:

- Stream URL: `string`
- Stream title: `string`
- Stream status (is this stream live?): `bool`

### Loop through streams

**Note**: The ACT is used here just as an example, this works for all the parliament modules.

```py
from legistream_backend.site.act import ACTStreamExtractor

for stream in ACTStreamExtractor().streams:
    print(stream.url,
          stream.title,
          stream.is_live
    )
```

### Notes

1. Run all scripts using `poetry`:

    ```sh
    poetry run python3 <file>.py
    ```

1. The South Australia stream extractor uses code adapted from the [streamlink ustreamtv implementation](https://github.com/streamlink/streamlink/blob/master/src/streamlink/plugins/ustreamtv.py).
