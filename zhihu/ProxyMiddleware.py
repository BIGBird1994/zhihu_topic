from .fetch_proxy import FetchProxy
import logging


class ProxyMiddleware(object):
    f = FetchProxy()
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        proxy = self.f.fetch_proxy()
        if proxy is not None:
            request.meta["proxy"] = "%s" % proxy
        else:
            proxy = self.f.fetch_proxy()
            request.meta["proxy"] = "%s" % proxy
