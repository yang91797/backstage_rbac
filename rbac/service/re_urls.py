from django.urls import reverse
from django.http import QueryDict


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL(替代了模板中的URL)
    :param request:
    :param name:
    :param args: 接收url中的参数 例如： re_path(r'^menu/edit/(\d+)/*$', menu.menu_edit, name='menu_edit'),
    :param kwargs: 接收url中有名分组参数 例如：re_path(r'^menu/edit/(?P<pk>\d+)/*$', menu.menu_edit, name='menu_edit'),
    :return:
    """
    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 当前URL中无参数,则直接返回原url
    if not request.GET:
        return basic_url

    # 参数处理
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    old_params = query_dict.urlencode()

    return "%s?%s" % (basic_url, old_params)


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成url,并解析出原url参数
    http://127.0.0.1:8000/rbac/menu/add/?_filter=mid%3D2
    1. 在url中解析出原来的搜索条件，_filter后的值
    2. reverse反向生成原来的URL, 如：/menu/list/
    3. 生成原来的url  /menu/list?mid%3D2
    :param request:
    :param name:
    :param args:接收url中的参数 例如： re_path(r'^menu/edit/(\d+)/*$', menu.menu_edit, name='menu_edit'),
    :param kwargs:接收url中有名分组参数 例如：re_path(r'^menu/edit/(?P<pk>\d+)/*$', menu.menu_edit, name='menu_edit'),
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get("_filter")
    if origin_params:
        url = "%s?%s" % (url, origin_params,)

    return url

