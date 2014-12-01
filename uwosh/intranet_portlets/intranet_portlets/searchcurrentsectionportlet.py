from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.search import ISearchPortlet, Assignment as BaseAssignment, Renderer as BaseRenderer, AddForm as BaseAddForm, EditForm as BaseEditForm
from plone.app.portlets.portlets import base
from zope import schema
from zope.interface import implements
from zope.formlib import form
from plone.app.portlets import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter


class ISearchCurrentSectionPortlet(ISearchPortlet):
    """ A portlet displaying a (live) search box for searching the current section
    """
    pass


class Assignment(BaseAssignment):
    implements(ISearchCurrentSectionPortlet)

    @property
    def title(self):
        return _(u"Search Current Section")


class Renderer(base.Renderer, BaseRenderer):

    render = ViewPageTemplateFile('searchcurrentsectionportlet.pt')

    def __init__(self, context, request, view, manager, data):
        BaseRenderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    def folder_path(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        folder = context_state.folder()
        return '/'.join(folder.getPhysicalPath())
     

class AddForm(base.AddForm):
    form_fields = form.Fields(ISearchCurrentSectionPortlet)
    label = _(u"Add Search Current Section Portlet")
    description = _(u"This portlet shows a search box for searching the current section.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(ISearchCurrentSectionPortlet)
    label = _(u"Edit Search Current Section Portlet")
    description = _(u"This portlet shows a search box for searching the current section.")

