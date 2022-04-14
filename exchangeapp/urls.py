from django.urls import path, include
from . import views
urlpatterns = [
    path('detail/<str:stock_name>', views.detail_page, name='detail_page'),
    path('detail/<int:stock_id>/response', views.detail, name='detail'),
    path('', views.main_page, name='main_page'),
    path('main_course', views.main, name='main'),
    path('buy/<int:stock_id>/<int:user_id>', views.buy, name='buy'),
    path('sell/<int:stock_id>/<int:user_id>', views.sell, name='sell'),
    path('portfolio/', views.portfolio_page, name='portfolio'),
]
