#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_not
from hamcrest import has_item
from hamcrest import assert_that
does_not = is_not

from nti.testing.matchers import verifiably_provides

from nti.app.products.integration.interfaces import IIntegrationWorkspace

from nti.appserver.workspaces.interfaces import IUserService

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver


class TestWorkspace(ApplicationLayerTest):

    testapp = None

    @WithSharedApplicationMockDS
    def test_workspace(self):

        with mock_dataserver.mock_db_trans(self.ds):
            user = self._create_user(username=self.extra_environ_default_user)
            service = IUserService(user)

            workspaces = service.workspaces

            assert_that(workspaces,
						has_item(verifiably_provides(IIntegrationWorkspace)))

