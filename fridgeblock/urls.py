from django.conf.urls import url
from .views import (
    new_session, del_session, all_sessions, edit_categories, add_category,
    edit_category, delete_category, reorder_categories, add_item,
    edit_item, delete_item, reorder_items, session, save_magnet,
    delete_magnet,
)

urlpatterns = [
    url(r'^new_session/$', new_session, {}, 'fridge-new-session'),
    url(r'^del_session/(?P<id>\d+)/$', del_session, {}, 'fridge-del-session'),
    url(r'^all_sessions/$', all_sessions, {}, 'fridge-all-sessions'),
    url(r'^(?P<id>\d+)/edit_categories/$', edit_categories, {},
        'fridge-edit-categories'),

    url(r'^(?P<id>\d+)/edit_categories/add_category/$', add_category, {},
        'edit-fridge-add-category'),
    url(r'^(?P<id>\d+)/edit_category/$', edit_category, {},
        'edit-fridge-category'),
    url(r'^(?P<id>\d+)/delete_category/$', delete_category, {},
        'delete-fridge-category'),
    url(r'^(?P<id>\d+)/reorder_categories/$', reorder_categories, {},
        'reorder-fridge-categories'),

    url(r'^(?P<id>\d+)/edit_category/add_item/$', add_item, {},
        'edit-fridge-add-item'),
    url(r'^(?P<id>\d+)/edit_item/$', edit_item, {}, 'edit-fridge-item'),
    url(r'^(?P<id>\d+)/delete_item/$', delete_item, {}, 'delete-fridge-item'),
    url(r'^(?P<id>\d+)/reorder_items/$', reorder_items, {},
        'reorder-fridge-items'),

    url(r'^session/(?P<id>\d+)/$', session, {}, 'fridge-session'),
    url(r'^session/(?P<id>\d+)/save_magnet/$', save_magnet, {},
        'fridge-save-magnet'),
    url(r'^session/(?P<id>\d+)/delete_magnet/$', delete_magnet, {},
        'fridge-delete-magnet'),
]
