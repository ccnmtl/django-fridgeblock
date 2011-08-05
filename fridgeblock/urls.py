from django.conf.urls.defaults import patterns


urlpatterns = patterns('fridgeblock.views',
                       (r'^new_session/$','new_session',{},'fridge-new-session'),
                       (r'^del_session/(?P<id>\d+)/$','del_session',{},'fridge-del-session'),
                       (r'^all_sessions/$','all_sessions',{},'fridge-all-sessions'),
                       (r'^(?P<id>\d+)/edit_categories/$','edit_categories',{},'fridge-edit-categories'),

                       (r'^(?P<id>\d+)/edit_categories/add_category/$','add_category',{},'edit-fridge-add-category'),
                       (r'^(?P<id>\d+)/edit_category/$','edit_category',{},'edit-fridge-category'),
                       (r'^(?P<id>\d+)/delete_category/$','delete_category',{},'delete-fridge-category'),
                       (r'^(?P<id>\d+)/reorder_categories/$','reorder_categories',{},'reorder-fridge-categories'),

                       (r'^(?P<id>\d+)/edit_category/add_item/$','add_item',{},'edit-fridge-add-item'),
                       (r'^(?P<id>\d+)/edit_item/$','edit_item',{},'edit-fridge-item'),
                       (r'^(?P<id>\d+)/delete_item/$','delete_item',{},'delete-fridge-item'),
                       (r'^(?P<id>\d+)/reorder_items/$','reorder_items',{},'reorder-fridge-items'),


                       (r'^session/(?P<id>\d+)/$','session',{},'fridge-session'),
                       (r'^session/(?P<id>\d+)/save_magnet/$','save_magnet',{},'fridge-save-magnet'),
                       (r'^session/(?P<id>\d+)/delete_magnet/$','delete_magnet',{},'fridge-delete-magnet'),
)
