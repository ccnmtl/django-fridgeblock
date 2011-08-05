# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from django.core.urlresolvers import reverse
from pagetree.helpers import get_hierarchy

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@login_required
def index(request):
    user = request.user
    # let's just send them to the most recent session
    newest = Session.objects.filter(user=user).order_by("-id")
    if newest.count() == 0:
        # create one
        return HttpResponseRedirect(reverse('fridge-new-session'))
    else:
        return HttpResponseRedirect(reverse('fridge-session',args=[newest[0].id]))


@login_required
@rendered_with('healthhabitplan/session.html')
def session(request,id):
    s = get_object_or_404(Session,id=id)
    h = get_hierarchy()
    return dict(session=s,
                sessions=Session.objects.filter(user=request.user),
                categories=Category.objects.all(),
                root = h.get_root()
                )

@login_required
@rendered_with('healthhabitplan/all_sessions.html')
def all_sessions(request):
    user = request.user
    h = get_hierarchy()
    sessions = Session.objects.filter(user=request.user)
    return dict(sessions=sessions, categories=Category.objects.all(), root = h.get_root())

@login_required
def new_session(request):
    user = request.user
    s = Session.objects.create(user=user)
    return HttpResponseRedirect(reverse('fridge-session',args=[s.id]))

@login_required
def del_session(request, id=id):
    user = request.user
    s = Session.objects.get(id=id)
    s.delete()
    return HttpResponseRedirect(reverse('fridge-index'))


@login_required
def save_magnet(request,id):
    s = get_object_or_404(Session,id=id)
    if request.method == "POST":
        item_id = request.GET['item_id']
        item = get_object_or_404(Item,id=item_id)
        x = request.GET['x']
        y = request.GET['y']
        r = Magnet.objects.filter(session=s,item=item)
        if r.count() > 0:
            m = r[0]
            m.x = x
            m.y = y
            m.save()
        else:
            m = Magnet.objects.create(session=s,item=item,x=x,y=y)
    return HttpResponse("ok");

@login_required
def delete_magnet(request,id):
    s = get_object_or_404(Session,id=id)
    if request.method == "POST":
        item_id = request.GET['item_id']
        item = get_object_or_404(Item,id=item_id)
        r = Magnet.objects.filter(session=s,item=item)
        if r.count() > 0:
            m = r[0]
            m.delete()
    return HttpResponse("ok");

@login_required
@rendered_with("fridgeblock/edit_categories.html")
def edit_categories(request,id):
    block = get_object_or_404(FridgeBlock,id=id)
    return dict(fridge=block)

def reorder_categories(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    fridge = get_object_or_404(FridgeBlock,id=id)
    keys = request.GET.keys()
    category_keys = [int(k[len('category_'):]) for k in keys if k.startswith('category_')]
    category_keys.sort()
    categories = [int(request.GET['category_' + str(k)]) for k in category_keys]
    fridge.set_category_order(categories)
    return HttpResponse("ok")

def delete_category(request,id):
    c = get_object_or_404(Category,id=id)
    fridge = c.fridgeblock
    c.delete()
    return HttpResponseRedirect(reverse("fridge-edit-categories",args=[fridge.id]))

@rendered_with('fridgeblock/edit_category.html')
def edit_category(request,id):
    category = get_object_or_404(Category,id=id)
    if request.method == "POST":
        form = category.edit_form(request.POST)
        category = form.save(commit=False)
        category.save()
        return HttpResponseRedirect(reverse("edit-fridge-category",args=[category.id]))
    return dict(category=category)


def add_category(request,id):
    fridge = get_object_or_404(FridgeBlock,id=id)
    form = fridge.add_category_form(request.POST,request.FILES)
    if form.is_valid():
        layer = form.save(commit=False)
        layer.fridgeblock = fridge
        layer.save()
    else:
        print "form was not valid"
        print form.errors
    return HttpResponseRedirect(reverse("fridge-edit-categories",args=[fridge.id]))



def reorder_items(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    category = get_object_or_404(Category,id=id)
    keys = request.GET.keys()
    item_keys = [int(k[len('item_'):]) for k in keys if k.startswith('item_')]
    item_keys.sort()
    items = [int(request.GET['item_' + str(k)]) for k in item_keys]
    category.set_item_order(items)
    return HttpResponse("ok")

def delete_item(request,id):
    c = get_object_or_404(Item,id=id)
    category = c.category
    c.delete()
    return HttpResponseRedirect(reverse("edit-fridge-category",args=[category.id]))

@rendered_with('fridgeblock/edit_item.html')
def edit_item(request,id):
    item = get_object_or_404(Item,id=id)
    if request.method == "POST":
        form = item.edit_form(request.POST)
        item = form.save(commit=False)
        item.save()
        return HttpResponseRedirect(reverse("fridge-edit-item",args=[item.id]))
    return dict(item=item)


def add_item(request,id):
    category = get_object_or_404(Category,id=id)
    form = category.add_item_form(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.category = category
        item.save()
    else:
        print "form was not valid"
        print form.errors
    return HttpResponseRedirect(reverse("edit-fridge-category",args=[category.id]))

