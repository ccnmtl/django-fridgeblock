from django.db import models
from pagetree.models import PageBlock
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django import forms
from datetime import datetime
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings
from sorl.thumbnail.fields import ImageWithThumbnailsField
import os

class FridgeBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "fridgeblock/fridgeblock.html"
    js_template_file = "fridgeblock/fridgeblock_js.html"
    css_template_file = "fridgeblock/fridgeblock_css.html"

    display_name = "Fridge Block"
    
    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            alt_text = "<a href=\"" + reverse("fridge-edit-categories",args=[self.id]) + "\">categories</a><br />"
        return EditForm()
    
    def edit(self,vals,files=None):
        self.save()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            pass
        return AddForm()

    @classmethod
    def create(self,request):
        return FridgeBlock.objects.create()

    def needs_submit(self):
        return False

    def categories(self):
        return self.category_set.all()

    def add_category_form(self,request=None,files=None):
        return CategoryForm(request,files)

    @classmethod
    def get_exporter(self,export_type):
        e = Exporter()
        return (e.identifier,e.exporter)

class Exporter(object):
    block_class = FridgeBlock
    identifier = 'fridge'

    def exporter(self, block, xmlfile, zipfile):
        pass

    def importer(self, node, zipfile):
        return None


class Category(models.Model):
    fridgeblock = models.ForeignKey(FridgeBlock)
    label = models.CharField(max_length=256,default="")
    image = ImageWithThumbnailsField(upload_to="images/fridge/categories/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            })


    class Meta:
        order_with_respect_to = "fridgeblock"

    def __unicode__(self):
        return self.label

    def css(self):
        return slugify(self.label)

    def edit_form(self,request=None):
        return CategoryForm(request,instance=self)

    def edit(self,vals,files):
        self.label = vals.get('label','')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def add_item_form(self,request=None):
        return ItemForm(request)

    def save_image(self,f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg','jpeg','gif','png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/fridge/categories/%04d/%02d/%02d/" % (now.year,now.month,now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("fridgeblock",)

class Item(models.Model):
    label = models.CharField(max_length=256,default="")
    category = models.ForeignKey(Category)
    description = models.TextField(default="",blank=True)

    class Meta:
        order_with_respect_to = 'category'

    def __unicode__(self):
        return self.label

    def edit_form(self,request=None):
        return ItemForm(request,instance=self)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ("category",)

class Session(models.Model):
    fridgeblock = models.ForeignKey(FridgeBlock)
    user = models.ForeignKey(User)
    saved = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("user","saved")

    def __unicode__(self):
        return "session #%d for %s %s" % (self.number(),self.user.first_name, self.user.last_name)

    def number(self):
        r = Session.objects.filter(user=self.user,fridgeblock=self.fridgeblock,
                                   saved__lt=self.saved).count()
        return r + 1

class Magnet(models.Model):
    session = models.ForeignKey(Session)
    item = models.ForeignKey(Item)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)


