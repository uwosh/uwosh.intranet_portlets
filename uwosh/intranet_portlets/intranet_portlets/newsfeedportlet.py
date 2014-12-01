from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.app.portlets.portlets.rss import IRSSPortlet, Assignment as RSSAssignment, \
    RSSFeed, Renderer as RSSRenderer, AddForm as RSSAddForm, EditForm as RSSEditForm

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
#from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
#from uwosh.intranet_portlets.intranet_portlets import NewsfeedPortletMessageFactory as _

from zope import schema
from plone.app.portlets import PloneMessageFactory as _
from zope.schema.vocabulary import SimpleVocabulary


NEWSFEED_VOCAB = [('', ''),
                  ('UW Oshkosh Plone activities', 'http://www.uwosh.edu/ploneprojects/plone-activities-blog/plone-activities-blog/RSS'),
                  ('Slashdot', 'http://rss.slashdot.org/Slashdot/slashdot'),
                  ('UW Oshkosh Plone Projects recent changes', 'http://www.uwosh.edu/ploneprojects/recent-changes/RSS'),
                  ('Plone News', 'http://plone.org/news/newslisting/RSS'),
                  ('Plone Events', 'http://plone.org/events/community/upcoming-events/RSS'),
                  ('Planet Plone', 'http://feeds.plone.org/ploneblogs'),
                  ('Twitter #plone', 'http://search.twitter.com/search.atom?q=%23plone'),
                  ('Twitter #ploneedu', 'http://search.twitter.com/search.atom?q=%23ploneedu'),
                  ('Twitter #plonesymp', 'http://search.twitter.com/search.atom?q=%23plonesymp'),
                  ('Twitter @uwoshkosh', 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=uwoshkosh'),
                  ('Twitter @plonesymp', 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=plonesymp'),
                  ('Twitter @plonesymposium', 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=plonesymposium'),
                  ('Twitter @ploneedu', 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=ploneedu'),
                  ('UW Oshkosh Today', 'http://www.uwosh.edu/today/feed/'),
                  ]


class INewsfeedPortlet(IRSSPortlet):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet.  If omitted, the title of the feed will be used.'),
        required=False,
        default=u'')

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)
    url = schema.Choice(title=_(u'Name of RSS feed'),
                        description=_(u'Name of the RSS feed to display.'),
                        required=True,
                        default=u'',
                        vocabulary=SimpleVocabulary.fromItems(NEWSFEED_VOCAB),)

    timeout = schema.Int(title=_(u'Feed reload timeout'),
                        description=_(u'Time in minutes after which the feed should be reloaded.'),
                        required=True,
                        default=100)


class Assignment(RSSAssignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(INewsfeedPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field



class Renderer(RSSRenderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """


class AddForm(RSSAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(INewsfeedPortlet)

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


class EditForm(RSSEditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(INewsfeedPortlet)
