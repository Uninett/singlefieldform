from django.urls import path, include

from . import views

multifield = [
    path('new/', views.CreateBookView.as_view(), name='book-new'),
    path('<int:pk>/delete/', views.DeleteBookView.as_view(), name='book-delete'),
    path('<int:pk>/update/', views.UpdateBookView.as_view(), name='book-edit'),
    path('', views.ListBookView.as_view(), name='book-list'),
]

singlefield = [
    path('new/', views.SinglefieldCreateBookView.as_view(), name='book-new2'),
    path('<int:pk>/delete/', views.SinglefieldDeleteBookView.as_view(), name='book-delete2'),
    path('<int:pk>/<str:fieldname>/', views.SinglefieldGetBookFieldView.as_view(), name='book-edit-field'),
    path('<int:pk>/<str:fieldname>/update/', views.SinglefieldUpdateBookView.as_view(), name='book-edit2'),
    path('', views.SinglefieldListBookView.as_view(), name='book-list2'),
]

singlefield_html = [
    path('new/', views.HTMxSinglefieldCreateBookView.as_view(), name='book-new3'),
    path('<int:pk>/delete/', views.HTMxSinglefieldDeleteBookView.as_view(), name='book-delete3'),
    path('<int:pk>/<str:fieldname>/', views.HTMxSinglefieldGetBookFieldView.as_view(), name='book-edit-field3'),
    path('<int:pk>/<str:fieldname>/update/', views.HTMxSinglefieldUpdateBookView.as_view(), name='book-edit3'),
    path('', views.HTMxSinglefieldListBookView.as_view(), name='book-list3'),
]

urlpatterns = [
    path("multifield/", include(multifield)),
    path("singlefield/", include(singlefield)),
    path("singlefield-htmx/", include(singlefield_html)),
]
