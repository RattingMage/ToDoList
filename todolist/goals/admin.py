from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class CommentInLine(admin.StackedInline):
    model = GoalComment
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('created', 'updated')
    list_filter = ['due_date']
    search_fields = ['title', 'description']
    inlines = [CommentInLine]


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('created', 'updated')
    list_filter = ['is_deleted']
    search_fields = ['title']
