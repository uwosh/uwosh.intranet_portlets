from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.app.portlets.portlets.rss import IRSSPortlet, Assignment as RSSAssignment, \
    RSSFeed, Renderer as RSSRenderer, AddForm as RSSAddForm, EditForm as RSSEditForm

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
#from uwosh.intranet_portlets.intranet_portlets import NewsfeedPortletMessageFactory as _

from plone.app.portlets import PloneMessageFactory as _
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName


class IPinsPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet.'),
        required=True,
        default=u'My Pins')

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=10)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IPinsPortlet)

    portlet_title = u''
    count = 0

    @property
    def title(self):
        """return the title"""
        return self.portlet_title

    def __init__(self, portlet_title=u'My Pins', count=10):
        self.portlet_title = portlet_title
        self.count = count



class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('pinsportlet.pt')

    def title(self):
        """return title of feed for portlet"""
        return getattr(self.data, 'portlet_title', '') 

    def links_folder_url(self):
        """return URL of links folder"""
        links_folder = self.links_folder()
        if not links_folder:
            return ''
        else:
            return links_folder.absolute_url()+'/folder_contents'

    def enabled(self):
        """Return if view should display at all."""
        pm = getToolByName(self, 'portal_membership', None)
        if not pm:
            return
        return not pm.isAnonymousUser()

    def links_folder(self):
        """return user's links folder"""
        pm = getToolByName(self, 'portal_membership', None)
        if not pm:
            return
        member = pm.getAuthenticatedMember()
        if not member:
            return
        home_folder = pm.getHomeFolder(member.id)
        if not home_folder:
            return
        links_folder = getattr(home_folder, 'my-pins', None)
        return links_folder

    def items(self):
        """Return all the user's pins."""
        links_folder = self.links_folder()
        if not links_folder:
            return 
        object_count = links_folder.objectCount()
        items = links_folder.contentItems()
        visible_items = items[:self.data.count] 
        return visible_items


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IPinsPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPinsPortlet)
