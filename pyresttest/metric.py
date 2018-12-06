import requests


class Metrics(requests.Response):
    # Timing info, precisely in order from start to finish
    # The time it took from the start until the name resolving was completed.
    @staticmethod
    def namelookup_time():
        pass

    # The time it took from the start until the connect to the remote host (or
    # proxy) was completed.
    @staticmethod
    def connect_time():
        pass

    # The time it took from the start until the SSL connect/handshake with the
    # remote host was completed.
    @staticmethod
    def appconnect_time():
        pass

    # The time it took from the start until the file transfer is just about to begin.
    # This includes all pre-transfer commands and negotiations that are
    # specific to the particular protocol(s) involved.
    @staticmethod
    def pretransfer_time():
        pass

    # The time it took from the start until the first byte is received by
    # libcurl.
    @staticmethod
    def starttransfer_time():
        pass

    # The time it took for all redirection steps include name lookup, connect, pretransfer and transfer
    # before final transaction was started. So, this is zero if no redirection
    # took place.
    @staticmethod
    def redirect_time():
        pass

    # Total time of the previous request.
    @staticmethod
    def total_time(response):
        total = response.elapsed.total_seconds()
        return total

    # Transfer sizes and speeds
    @staticmethod
    def size_download():
        pass

    @staticmethod
    def size_upload(response):
        size = response.headers['content-length']
        return size

    @staticmethod
    def request_size(response):
        size = len(response.content)
        return size

    @staticmethod
    def speed_download():
        pass

    @staticmethod
    def speed_upload():
        pass

    @staticmethod
    # Connection counts
    def redirect_count(response):
        count = len(response.history)
        return count

    @staticmethod
    def num_connects():
        pass
