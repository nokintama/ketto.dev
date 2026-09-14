from django.urls import path
from .views import (
    PickProblemView,
    ProblemTestsView,
    CreateMatchView,
    FinishMatchView,
    CreateSubmissionView,
    UserRatingView,
)

urlpatterns = [
    path('problems/pick/', PickProblemView.as_view(), name='internal-pick-problem'),
    path('problems/<int:problem_id>/tests/', ProblemTestsView.as_view(), name='internal-problem-tests'),
    path('matches/', CreateMatchView.as_view(), name='internal-create-match'),
    path('matches/<int:match_id>/finish/', FinishMatchView.as_view(), name='internal-finish-match'),
    path('submissions/', CreateSubmissionView.as_view(), name='internal-create-submission'),
    path('users/<int:user_id>/rating/', UserRatingView.as_view(), name='internal-user-rating'),
]