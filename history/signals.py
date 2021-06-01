"""histroy signal module"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
import logging

from history.models import LikeActivity, ViewHistory


@receiver(pre_save, sender=LikeActivity)
def update_like_counter_cache(sender, **kwargs):
    """article.like_count를 갱신합니다."""
    instance = kwargs['instance']

    content_type = instance.content_type
    content_id = instance.content_id
    category = instance.category

    prev_instance = LikeActivity.objects.filter(pk=instance.id).first()
    prev_category = prev_instance.category if prev_instance else 'None'

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


@receiver(pre_save, sender=LikeActivity)
def update_dislike_counter_cache(sender, **kwargs):
    """article.dislike_count를 갱신합니다."""

    instance = kwargs['instance']

    content_type = instance.content_type
    content_id = instance.content_id
    category = instance.category

    prev_instance = LikeActivity.objects.filter(pk=instance.id).first()
    prev_category = prev_instance.category if prev_instance else 'None'

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


@receiver(pre_save, sender=ViewHistory)
def update_viewed_counter_cache(sender, **kwargs):
    """viewed_count를 갱신합니다."""
    instance = kwargs['instance']

    viewed_type = instance.viewed_type
    viewed_id = instance.viewed_id
    viewed_object = viewed_type.get_object_for_this_type(pk=viewed_id)
    
    next_viewed_count = instance.viewed_count
    prev_instance = ViewHistory.objects.filter(pk=instance.id).first()

    logger = logging.getLogger(__name__)
    if prev_instance:
        prev_viewed_count = prev_instance.viewed_count
        viewed_object.viewed_count += next_viewed_count - prev_viewed_count
        logger.info("{} {}".format("ppp", next_viewed_count - prev_viewed_count))
    else:
        viewed_object.viewed_count += next_viewed_count
        logger.info("{} {}".format("ppp", next_viewed_count))
    
    viewed_object.save()
