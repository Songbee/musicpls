from io import BytesIO


class SeekableBuffer:
    """
    A filelike object that wraps a stream and reads it into a buffer on demand,
    making it seekable and re-readable / re-writable.

    Implements IOInterface described at https://mutagen.readthedocs.io/en/latest/user/filelike.html.

    Example:
        >>> r = requests.get("http://speedtest.tele2.net/10GB.zip", stream=True)
        >>> sb = SeekableBuffer(r.raw)
        >>> sb.seek(1024)
        >>> sb.read(10)  # => probably garbage
        # this doesn't download the full file though
    """

    def __init__(self, stream, seek_cache=0):
        self.stream = stream
        self.buffer = BytesIO()
        self._length = 0
        self._seek_cache = seek_cache

    def _buffer(self, length=-1):
        pos = self.buffer.tell()
        if length == -1:
            v = self.buffer.getvalue()
            self.buffer = BytesIO(v + self.stream.read())
            self.buffer.seek(pos)
        elif length > self._length + self._seek_cache:
            v = self.buffer.getvalue()
            self.buffer = BytesIO(v + self.stream.read(length - pos))
            self.buffer.seek(pos)

    def tell(self):
        return self.buffer.tell()

    def read(self, size=-1):
        if size == -1:
            self._buffer()
            return self.buffer.read()

        self._buffer(self.buffer.tell() + size)
        return self.buffer.read(size)


    def seek(self, offset, whence=0):
        if whence == 0:
            self._buffer(offset)
        elif whence == 1:
            self._buffer(self.buffer.tell() + offset)
        elif whence == 2:
            self._buffer()

        return self.buffer.seek(offset, whence)

    def write(self, data):
        self._buffer()
        self.buffer.write(data)
        print("WRITE", len(data))

    def truncate(self, size=None):
        self._buffer()
        self.buffer.truncate(size)
        print("TRUNC", size)

    def flush(self):
        self._buffer()
        self.buffer.flush()
