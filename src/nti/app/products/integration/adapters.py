#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.appserver.workspaces.interfaces import IUserService

from nti.app.products.integration.interfaces import IIntegrationWorkspace
from nti.app.products.integration.interfaces import IIntegrationCollection

from nti.app.products.integration.workspaces import IntegrationCollection

from nti.dataserver.interfaces import IUser

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IIntegrationCollection)
@component.adapter(IUser)
def user_integration_collection(user):
    service = IUserService(user)
    workspace = IIntegrationWorkspace(service, None)
    if workspace is not None:
        return IntegrationCollection(workspace)
