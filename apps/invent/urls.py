from django.urls import path
from . import views


app_name = "invent"
urlpatterns = [
    path('setup/itemgroup/', views.ItemGroupListView.as_view(), name="itemgroup"),
    path('setup/itemgroup/create/', views.ItemGroupCreateView.as_view(), name="itemgroup-create"),
    path('setup/itemgroupjson/', views.ItemGroup_Json.as_view(), name="itemgroup-json"),
    path('setup/itemgroup/<int:pk>/update/', views.ItemGroupUpdateView.as_view(), name="itemgroup-update"),
    path('setup/itemgroup/<int:pk>/delete/', views.ItemGroupDeleteView.as_view(), name="itemgroup-delete"),
    path('setup/itemconfig/', views.ItemConfigListView.as_view(), name="itemconfig"),
    path('setup/itemconfig/create/', views.ItemConfigCreateView.as_view(), name="itemconfig-create"),
    path('setup/itemconfigjson/', views.ItemConfig_Json.as_view(), name="itemconfig-json"),
    path('setup/itemconfig/<int:pk>/update/', views.ItemConfigUpdateView.as_view(), name="itemconfig-update"),
    path('setup/itemconfig/<int:pk>/delete/', views.ItemConfigDeleteView.as_view(), name="itemconfig-delete"),
    path('setup/itemcolor/', views.ItemColorListView.as_view(), name="itemcolor"),
    path('setup/itemcolor/create/', views.ItemColorCreateView.as_view(), name="itemcolor-create"),
    path('setup/itemcolorjson/', views.ItemColor_Json.as_view(), name="itemcolor-json"),
    path('setup/itemcolor/<int:pk>/update/', views.ItemColorUpdateView.as_view(), name="itemcolor-update"),
    path('setup/itemcolor/<int:pk>/delete/', views.ItemColorDeleteView.as_view(), name="itemcolor-delete"),
     path('setup/itemsize/', views.ItemSizeListView.as_view(), name="itemsize"),
    path('setup/itemsize/create/', views.ItemSizeCreateView.as_view(), name="itemsize-create"),
    path('setup/itemsizejson/', views.ItemSize_Json.as_view(), name="itemsize-json"),
    path('setup/itemsize/<int:pk>/update/', views.ItemSizeUpdateView.as_view(), name="itemsize-update"),
    path('setup/itemsize/<int:pk>/delete/', views.ItemSizeDeleteView.as_view(), name="itemsize-delete"),
]