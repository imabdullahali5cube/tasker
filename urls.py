from django.urls import path
from developers.views import developersApiView,developersDetailsApiView,ProjectApiView,ManagerCreateView,BankCreateView,ProjectUpdateView

urlpatterns = [
    path("developers/",developersApiView.as_view(),name='get-all'),
    path('developers/create/', developersApiView.as_view(),name='devloper-create-list'),
    path('developers/<int:pk>/',developersDetailsApiView.as_view(),name='developer-id'),
    path('project/create/',ProjectApiView.as_view(),name='project-create-list'),
    path("projects/",ProjectApiView.as_view(),name='get-all-projects'),

    path("project/manager/",ManagerCreateView.as_view(),name='manager'),
    path("project/bank/",BankCreateView.as_view(),name='bank'),

    path("project/update/<int:pk>/",ProjectUpdateView.as_view(),name='update'),

    # path('developers/<int:pk>/update/', developersDetailsApiView.as_view(), name='developer-update'),
    # path('developers/<int:pk>/', developersDetailsApiView.as_view(),name='developer-by-id'),

]   