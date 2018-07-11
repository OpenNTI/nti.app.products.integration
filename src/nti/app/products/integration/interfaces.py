#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class,expression-not-assigned

from zope import interface

from zope.location.interfaces import IContained

from nti.appserver.workspaces.interfaces import IWorkspace
from nti.appserver.workspaces.interfaces import IContainerCollection

from nti.coremetadata.interfaces import IShouldHaveTraversablePath

from nti.schema.field import ValidDatetime
from nti.schema.field import DecodingValidTextLine as ValidTextLine


class IIntegration(IContained):
    """
    Contains integration information with third-party systems.
    """

    title = ValidTextLine(title=u"Integration title",
                          min_length=2,
                          required=True)

    description = ValidTextLine(title=u"Integration description", required=False)


class IAuthorizedIntegration(IIntegration, IShouldHaveTraversablePath):
    """
    An :class:`IIntegration` object that has been authorized.
    """

    authorization_date = ValidDatetime(title=u"Integration auth date",
                                       required=True)


class IOAuthAuthorizedIntegration(IAuthorizedIntegration):
    """
    An :class:`IIntegration` object that has been oath authorized.
    """

    refresh_token = ValidTextLine(title=u'The refresh token',
                                  required=True)

    refresh_token.setTaggedValue('_ext_excluded_out', True)


class IIntegrationWorkspace(IWorkspace):
    """
    A workspace to hold integration information.
    """


class IIntegrationCollection(IContainerCollection):
    """
    Contains a collection of :class:`IIntegration` objects.
    """


class IIntegrationCollectionProvider(interface.Interface):
    """
    Provides :class:`IIntegration` objects to our integration collection.
    """

    def get_collection_iter():
        """
        Returns an iterable over this collection provider, optionally
        filtering on the given string.
        """
