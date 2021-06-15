from django import template

register = template.Library()

@register.simple_tag
def comment_restrictable(current_user):
    return current_user.is_admin