from django.contrib import admin

from .models import PaperCategory, Paper, PaperAuthor, PaperVersion, PaperVersionReviewer, Review, JohaEventSchedule

@admin.register(JohaEventSchedule)
class JohaEventScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'receipt_start_at',
        'receipt_end_at',
    ]

@admin.register(PaperCategory)
class PaperCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content',
        'created_at',
        'updated_at',
    ]

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'subtitle',
        'summary',
    ]

@admin.register(PaperAuthor)
class PaperAuthorAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'author'
    ]

    list_display = [
        'id',
        'author',
        'paper',
    ]

@admin.register(PaperVersion)
class PaperVersionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'paper',
        'chief',
        'version_number',
    ]

@admin.register(PaperVersionReviewer)
class PaperVersionReviewerAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'reviewer'
    ]
    list_display = [
        'id',
        'reviewer',
        'paper_version',
        'status'
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'reviewer'
    ]
    list_display = [
        'id',
        'before_version',
        'current_version',
        'reviewer',
        'comment'
    ]