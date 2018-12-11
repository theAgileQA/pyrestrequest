""" Metrics methods that perform calculations based on the request provided."""
import requests


class Metrics(requests.Response):
    """ Class containing all calculation methods. """

    @staticmethod
    def namelookup_time():
        """ Timing info, precisely in order from start to finish
        The time it took from the start until the name resolving was completed.
        """
        pass

    @staticmethod
    def connect_time():
        """ The time it took from the start until the connect
         to the remote host (or proxy) was completed.
        """
        pass

    @staticmethod
    def appconnect_time():
        """ The time it took from the start until the SSL
        connect/handshake with the remote host was completed.
        """
        pass

    @staticmethod
    def pretransfer_time():
        """ The time it took from the start until the file transfer is just about to begin.
        This includes all pre-transfer commands and negotiations that are
        specific to the particular protocol(s) involved.
        """
        pass

    @staticmethod
    def starttransfer_time():
        """ The time it took from the start until the first
        byte is received by request.
        """
        pass

    @staticmethod
    def redirect_time():
        """ The time it took for all redirection steps include
         name lookup, connect, pre-transfer and transfer
         before final transaction was started.
         So, this is zero if no redirection took place.
        """
        pass

    @staticmethod
    def total_time(response):
        """ Total time of the previous request. """
        total = response.elapsed.total_seconds()
        return total

    @staticmethod
    def size_download():
        """ Transfer sizes and speeds. """
        pass

    @staticmethod
    def size_upload(response):
        """ Total size of attachments uploaded. """
        size = response.headers['content-length']
        return size

    @staticmethod
    def request_size(response):
        """ Total size of request. """
        size = len(response.content)
        return size

    @staticmethod
    def speed_download():
        """ Total time of speed to download content. """
        pass

    @staticmethod
    def speed_upload():
        """ Total time of speed of uploading content. """
        pass

    @staticmethod
    def redirect_count(response):
        """ Connection count total made by request. """
        count = len(response.history)
        return count

    @staticmethod
    def num_connects():
        """ Total number of connections made by request. """
        pass
