from rbac import models
from django import forms
from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    """
    用户验证
    """
    confirm_password = forms.CharField(label="确认密码")

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        """
        批量修改样式
        :param args:
        :param kwargs:
        """
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise ValidationError("输入密码不一致")
        return confirm_password


class UpdateUserModelForm(forms.ModelForm):
    """
    用户验证
    """

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        """
        批量修改样式
        :param args:
        :param kwargs:
        """
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"


class ResetPasswordUserModelForm(forms.ModelForm):
    """
    用户验证
    """
    confirm_password = forms.CharField(label="确认密码")

    class Meta:
        model = models.UserInfo
        fields = ['password']

    def __init__(self, *args, **kwargs):
        """
        批量修改样式
        :param args:
        :param kwargs:
        """
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise ValidationError("输入密码不一致")
        return confirm_password

