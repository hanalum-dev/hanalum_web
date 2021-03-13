from django import template

register = template.Library()

@register.simple_tag
def editable(comment, current_user):
    return comment.editable(current_user)

@register.simple_tag
def destroyable(comment, current_user):
    return comment.destroyable(current_user)