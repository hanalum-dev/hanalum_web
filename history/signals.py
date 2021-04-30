from django.db.models.signals import pre_save
from django.dispatch import receiver
from history.models import LikeActivity

from django.contrib.contenttypes.models import ContentType
from articles.models import Article

@receiver( pre_save, sender = LikeActivity )
def update_like_counter_cache( sender, **kwargs ):

    instance = kwargs[ 'instance' ]

    content_type = instance.content_type
    content_id = instance.content_id
    category = instance.category

    prev_instance = LikeActivity.objects.get(pk=instance.id)
    prev_category = prev_instance.category


    if category != 'like' and prev_category != 'like':
        return

    if category == 'like' and prev_category != 'like':
        try:
            liked_object = content_type.get_object_for_this_type(pk=content_id)
            liked_object.like_count += 1
            liked_object.save()
        except:
            return
    elif category != 'like' and prev_category == 'like':
        try:
            liked_object = content_type.get_object_for_this_type(pk=content_id)
            liked_object.like_count -= 1
            liked_object.save()
        except:
            return


@receiver( pre_save, sender = LikeActivity )
def update_dislike_counter_cache( sender, **kwargs ):

    instance = kwargs[ 'instance' ]

    content_type = instance.content_type
    content_id = instance.content_id
    category = instance.category

    prev_instance = LikeActivity.objects.get(pk=instance.id)
    prev_category = prev_instance.category


    if category != 'dislike' and prev_category != 'dislike':
        return

    if category == 'dislike' and prev_category != 'dislike':
        try:
            disliked_object = content_type.get_object_for_this_type(pk=content_id)
            disliked_object.dislike_count += 1
            disliked_object.save()
        except:
            return
    elif category != 'dislike' and prev_category == 'dislike':
        try:
            disliked_object = content_type.get_object_for_this_type(pk=content_id)
            disliked_object.dislike_count -= 1
            disliked_object.save()
        except:
            return
