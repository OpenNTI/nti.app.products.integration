#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.interfaces import IRequest

from zope import component
from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.container.contained import Contained

from zope.location.interfaces import IContained

from zope.traversing.interfaces import IPathAdapter

from nti.appserver.workspaces.interfaces import IUserService

from nti.app.products.integration import INTEGRATION_WORKSPACE

from nti.app.products.integration.interfaces import IIntegrationWorkspace
from nti.app.products.integration.interfaces import IAuthorizedIntegration
from nti.app.products.integration.interfaces import IIntegrationCollection
from nti.app.products.integration.interfaces import IIntegrationCollectionProvider

from nti.dataserver.authorization import is_admin_or_content_admin_or_site_admin

from nti.dataserver.interfaces import IUser

from nti.datastructures.datastructures import LastModifiedCopyingUserList

from nti.property.property import alias

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IIntegrationCollection)
class _IntegrationCollection(Contained):
    """
    Returns all the :class:`IIntegration` objects.
    """

    __name__ = u'Integrations'

    name = alias('__name__')

    def __init__(self, parent):
        self.__parent__ = parent

    @Lazy
    def accepts(self):
        return ()

    @Lazy
    def integrations(self):
        """
        Fetch all registered IIntegration objects; if they are adaptable to
        IAuthorizedIntegration, we include that instead.
        """
        result = []
        for integration_provider in component.getAllUtilitiesRegisteredFor(IIntegrationCollectionProvider):
            integration_iter = integration_provider.get_collection_iter()
            result.extend(integration_iter)
        return result

    def __len__(self):
        return len(self.container)

    @Lazy
    def container(self):
        container = LastModifiedCopyingUserList()
        container.extend(self.integrations)
        container.__name__ = self.__name__
        container.__parent__ = self.__parent__
        container.lastModified = 0
        return container

    @property
    def links(self):
        return ()


@interface.implementer(IIntegrationWorkspace, IContained)
class _IntegrationWorkspace(object):

    __parent__ = None
    __name__ = INTEGRATION_WORKSPACE

    name = alias('__name__')

    def __init__(self, user_service):
        self.context = user_service
        self.user = user_service.user

    @Lazy
    def collections(self):
        """
        The returned collections are sorted by name.
        """
        return (_IntegrationCollection(self),)

    @property
    def links(self):
        return ()

    def __getitem__(self, key):
        """
        Make us traversable to collections.
        """
        for i in self.collections:
            if i.__name__ == key:
                return i
        raise KeyError(key)

    def __len__(self):
        return len(self.collections)

    def predicate(self):
        return is_admin_or_content_admin_or_site_admin(self.user)


@interface.implementer(IIntegrationWorkspace)
@component.adapter(IUserService)
def IntegrationWorkspace(user_service):
    workspace = _IntegrationWorkspace(user_service)
    if workspace.predicate():
        workspace.__parent__ = workspace.user
        return workspace


@interface.implementer(IPathAdapter)
@component.adapter(IUser, IRequest)
def IntegrationPathAdapter(context, unused_request):
    service = IUserService(context)
    workspace = IIntegrationWorkspace(service)
    return workspace
