from django import template
from fridgeblock.models import Magnet,Session

register = template.Library()

class MagnetExistsForSessionNode(template.Node):
    def __init__(self, session, item, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.session = session
        self.item = item

    def render(self, context):
        if self.session not in context:
            return self.nodelist_false.render(context)
        s = context[self.session]
        i = context[self.item]
        if Magnet.objects.filter(session=s,item=i).count():
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.tag('if_magnet_for_item_exists')
def accessible(parser, token):
    session = token.split_contents()[1:][0]
    item    = token.split_contents()[1:][1]
    nodelist_true = parser.parse(('else','endif_magnet_for_item_exists'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_magnet_for_item_exists',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return MagnetExistsForSessionNode(session, item, nodelist_true, nodelist_false)


class GetSessionNode(template.Node):
    def __init__(self,fridge,var_name):
        self.fridge = fridge
        self.var_name = var_name

    def render(self, context):
        f = context[self.fridge]
        u = context['request'].user
        if u.is_anonymous():
            return ''
        r = Session.objects.filter(fridgeblock=f,user=u).order_by("-saved")
        if r.count() == 0:
            context[self.var_name] = Session.objects.create(fridgeblock=f,user=u)
        else:
            context[self.var_name] = r[0]
        return ''

@register.tag('getsession')
def getquestionresponse(parser, token):
    fridge = token.split_contents()[1:][0]
    var_name = token.split_contents()[1:][2]
    return GetSessionNode(fridge,var_name)
