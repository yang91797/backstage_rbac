from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLPattern, URLResolver   # 路由分发：URLResolver。非路由分发：URLPattern
import re


def check_url_exclude(url):
    """
    排除特定的URL
    :param url:
    :return:
    """
    exclude_url = settings.AUTO_DISCOVER_EXCLUDE
    for regex in exclude_url:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取URL
    :param pre_namespace:  namespace前缀，以后用于拼接name
    :param pre_url: url前缀，用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):     # 非路由分发，将路由添加到字典中
            if not item.name:
                continue
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + str(item.pattern)
            url = url.replace('^', '').replace('$', '')
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        elif isinstance(item, URLResolver):    # 路由分发，继续递归
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None

            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL，前提是必须要name别名
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)   #

    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)     # 递归获取所有路由
    return url_ordered_dict
