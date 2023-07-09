from django.urls import path

from goals.views.boards import BoardCreateView, BoardListView, BoardDetailView
from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryDetailView
from goals.views.goals import GoalCreateView, GoalListView, GoalDetailView
from goals.views.goal_comment import GoalCommentListView, GoalCommentDetailView, GoalCommentCreateView

urlpatterns = [
    path("goal_category/create", GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='list_category'),
    path("goal_category/<int:pk>", GoalCategoryDetailView.as_view(), name='detail_category'),

    path("goal/create", GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", GoalListView.as_view(), name='list_goal'),
    path("goal/<int:pk>", GoalDetailView.as_view(), name='detail_goal'),

    path("goal_comment/create", GoalCommentCreateView.as_view(), name='create_goal_comment'),
    path("goal_comment/list", GoalCommentListView.as_view(), name='list_goal_comment'),
    path("goal_comment/<int:pk>", GoalCommentDetailView.as_view(), name='detail_goal_comment'),

    path("board/create", BoardCreateView.as_view(), name='create_board'),
    path("board/list", BoardListView.as_view(), name='list_board'),
    path("board/<int:pk>", BoardDetailView.as_view(), name='detail_board'),
]
