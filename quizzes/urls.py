from django.urls import path, include # new added
from rest_framework.routers import DefaultRouter # new added
from .views import (
    ModuleQuestionsView, 
    StartAttemptView, 
    SubmitAttemptView,
    QuestionViewSet, # new added
    ChoiceViewSet # new added
)

router = DefaultRouter() # new added
router.register('questions', QuestionViewSet) # new added
router.register('choices', ChoiceViewSet) # new added

urlpatterns = [
    path('modules/<int:pk>/questions/', ModuleQuestionsView.as_view(), name='module-questions'),
    path('modules/<int:pk>/attempts/', StartAttemptView.as_view(), name='start-attempt'),
    path('attempts/<int:pk>/submit/', SubmitAttemptView.as_view(), name='submit-attempt'),
    
    path('', include(router.urls)), # new added
]