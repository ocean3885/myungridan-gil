from django import template

register = template.Library()

@register.filter
def truncate_char(value, max_length):
    """
    Truncate the string if it is longer than max_length.
    Append '...' to the end if the string is truncated.
    """
    if len(value) > max_length:
        return value[:max_length] 
    return value

@register.filter
def truncate_chars(value, max_length):
    """
    Truncate the string if it is longer than max_length.
    Append '...' to the end if the string is truncated.
    """
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value


@register.simple_tag
def combine_strings(name, title, created_at, comment_count):
    combined = f"{name} {title} [{comment_count}] {created_at.strftime('%m.%d')}"
    return combined

@register.filter
def mask_name(name):
    if not name:
        return ''
    return name[0] + 'ㅇ' * (len(name) - 1)