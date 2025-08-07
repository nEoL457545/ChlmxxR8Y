# 代码生成时间: 2025-08-08 00:49:42
from django import forms
def validate_email(value):
    """验证电子邮件格式是否正确"""
    if '@' not in value: return False
def validate_password(value):
    """验证密码是否符合安全要求（至少8位，包含数字和特殊字符）"""
    try:
        import re
        return re.fullmatch(r'(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z\d@$!#%*?&]{8,}', value) is not None
    except re.error: return False
def validate_phone_number(value):
    """验证电话号码是否符合标准（例如：123-456-7890）"""
    try:
        import re
        return re.fullmatch(r'\d{3}-\d{3}-\d{4}', value) is not None
    except re.error: return False
def validate_social_security_number(value):
    """验证社会安全号码是否符合标准（例如：123-45-6789）"""
    try:
        import re
        return re.fullmatch(r'\d{3}-\d{2}-\d{4}', value) is not None
    except re.error: return None
def validate_zipcode(value):
    """验证邮政编码是否符合标准（例如：12345）"""
    try:
        import re
        return re.fullmatch(r'\d{5}', value) is not None
    except re.error: return False
def validate_first_name(value):
    """验证名字是否只包含字母"""
    if value.isalpha(): return True
def validate_last_name(value):
    """验证姓氏是否只包含字母"""
    if value.isalpha(): return True
def validate_address(value):
    """验证地址是否符合标准（至少包含一个字母和一个数字）"""
    try:
        import re
        return re.fullmatch(r'^.*\d.*\w.*$', value) is not None
    except re.error: return False
def validate_date_of_birth(value):
    """验证出生日期是否符合标准（例如：YYYY-MM-DD）"""
    try:
        import datetime
        if datetime.datetime.strptime(value, '%Y-%m-%d') > datetime.datetime.now():
            return False
    except ValueError: return False