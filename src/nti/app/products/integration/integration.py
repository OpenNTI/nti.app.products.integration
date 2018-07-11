#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: model.py 123306 2017-10-19 03:47:14Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.cachedescriptors.property import Lazy

from nti.app.products.integration.interfaces import IIntegration
from nti.app.products.integration.interfaces import IAuthorizedIntegration
from nti.app.products.integration.interfaces import IOAuthAuthorizedIntegration

from nti.externalization.representation import WithRepr

from nti.ntiids.oids import to_external_ntiid_oid

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

logger = __import__('logging').getLogger(__name__)


@WithRepr
@interface.implementer(IIntegration)
class AbstractIntegration(SchemaConfigured):
    createDirectFieldProperties(IIntegration)

    __external_can_create__ = True

    creator = None
    NTIID = alias('ntiid')

    @Lazy
    def ntiid(self):
        return to_external_ntiid_oid(self)


@WithRepr
@interface.implementer(IAuthorizedIntegration)
class AbstractAuthorizedIntegration(AbstractIntegration):

    createDirectFieldProperties(IAuthorizedIntegration)


@WithRepr
@interface.implementer(IOAuthAuthorizedIntegration)
class AbstractOAuthAuthorizedIntegration(AbstractAuthorizedIntegration):

    createDirectFieldProperties(IOAuthAuthorizedIntegration)
