from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        批量修改样式
        :param args:
        :param kwargs:
        """
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
