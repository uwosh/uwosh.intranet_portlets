from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import addStatusMessage


class PinThis(BrowserView):
    """Add a pin for the current object
    """

    def __call__(self):
        REQUEST = self.request
        context = self.context
        out = ''

        pm = getToolByName(context, 'portal_membership', None)
        if pm is None:
          out += "Unable to locate portal_membership."
          context.plone_utils.addPortalMessage(out, 'error')

        member = pm.getAuthenticatedMember()
        if not member:
          out += "Unable to look up your account."
          context.plone_utils.addPortalMessage(out, 'error')

        home_folder = pm.getHomeFolder(member.id)
        if not home_folder:
          out += "You have no home folder."
          context.plone_utils.addPortalMessage(out, 'error')

        pins_folder = getattr(home_folder, 'my-pins', None)
        if not pins_folder:
          out += "Attempting to create your missing 'My Pins' folder."
          pins_id_actual = home_folder.invokeFactory('Folder', 'my-pins')
          pins_folder = getattr(home_folder, 'my-pins', None)
          if not pins_folder:
            out += "Your 'My Pins' folder could not be found and could not be created."
            context.plone_utils.addPortalMessage(out, 'error')
          else:
            pins_folder.setTitle('My Pins')
            pins_folder.reindexObject()
            out += "Created your 'My Pins' folder ok."

        link_id_desired = pins_folder.generateUniqueId('Link')
        link_id_actual = pins_folder.invokeFactory('Link', link_id_desired)

        link_obj = getattr(pins_folder, link_id_actual, None)

        if not link_obj:
          out += "Unable to create new pin."
          context.plone_utils.addPortalMessage(out, 'error')

        link_obj.setTitle(context.Title())
        link_obj.setRemoteUrl(context.absolute_url())
        link_obj.reindexObject()
        out += "Added pin for '" + link_obj.Title() + "', " + link_obj.getRemoteUrl()
        context.plone_utils.addPortalMessage(out, 'info')

        return REQUEST.RESPONSE.redirect(context.absolute_url())
