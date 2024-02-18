import sys
sys.path.append("dynamic_fingerprint_generator")
from lib.object_hasher import ObjectHasher
class TestFingerPrinter:
    example_headers_set = {
        "Host": "github.githubassets.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "*/*",
        "Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://github.com",
        "Connection": "keep-alive",
        "Referer": "https://github.com/",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "DNT": "1",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
    }

    example_remote_ip = "192.168.1.1"


    def test_fingerprint(self):
        object_hasher = ObjectHasher()
        result = object_hasher.hash_objects(headers=self.example_headers_set, remote_ip=self.example_remote_ip)
        assert result
        assert isinstance(result, int)
        assert result > 0
        result2 = object_hasher.hash_objects(headers=self.example_headers_set, remote_ip=self.example_remote_ip)
        assert result == result2
