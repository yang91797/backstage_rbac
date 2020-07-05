from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息的校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候触发执行
        :param request:
        :return:
        """

        # 1、获取当前用户请求的URL
        # 2、获取当前用户在session中保存的权限列表
        # 3、权限信息匹配

        valid_url_list = settings.VALID_URL_LIST    # 白名单

        current_url = request.path_info     # 获取当前用户请求的URL

        for valid_url in valid_url_list:
            if re.match(valid_url, current_url):
                # 白名单中的URL无序权限验证即可访问
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)        # 获取当前用户在session中保存的权限列表

        if not permission_dict:
            return HttpResponse("未获取到用户权限信息，请登录")

        url_record = [          # 动态菜单路径导航
            {'title': '首页', 'url': '#'}
        ]

        # 需要登录，但无需权限校验
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None

        flag = False
        for item in permission_dict.values():             # 权限信息匹配
            reg = "^%s$" % item['url']          # 起始和终止符
            if re.match(reg, current_url):   # 正则匹配

                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.url_record = url_record
                break
        if not flag:
            return HttpResponse("无权访问")



