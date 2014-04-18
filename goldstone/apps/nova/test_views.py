# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright 2014 Solinea, Inc.
#


from django.test import SimpleTestCase
from django.utils.unittest.case import skip
from .views import *
from datetime import datetime
import pytz


logger = logging.getLogger(__name__)


class NovaDiscoverViewTest(SimpleTestCase):
    # view requires a start_ts, end_ts, and interval string
    valid_start = str(calendar.timegm(
        datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc).utctimetuple()))
    valid_end = str(calendar.timegm(
        datetime.now(tz=pytz.utc).utctimetuple()))
    valid_interval = '3600s'
    invalid_start = '999999999999'
    invalid_end = '999999999999'
    invalid_interval = 'abc'

    def _test_bad_request(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def _test_good_request(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nova_discover.html')

    def test_good_request(self):
        url = '/nova/discover?start=' + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval
        self._test_good_request(url)

    def test_no_start(self):
        url = "/nova/discover?end=" + self.valid_end + \
            "&interval=" + self.valid_interval
        self._test_good_request(url)

    def test_no_end(self):
        url = "/nova/discover?start=" + self.valid_start + \
            "&interval=" + self.valid_interval
        self._test_good_request(url)

    def test_no_interval(self):
        url = "/nova/discover?start=" + self.valid_start + \
            "&end=" + self.valid_end
        self._test_good_request(url)

    def test_invalid_start(self):
        url = "/nova/discover?start=" + self.invalid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval
        self._test_bad_request(url)

    def test_invalid_finish(self):
        url = "/nova/discover?start=" + self.valid_start + \
            "&end=" + self.invalid_end + \
            "&interval=" + self.valid_interval
        self._test_bad_request(url)

    def test_invalid_interval(self):
        url = "/nova/discover?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.invalid_interval
        self._test_bad_request(url)


class NovaSpawnsViewTest(SimpleTestCase):
    # view requires a start_ts, end_ts, and interval string
    valid_start = str(calendar.timegm(
        datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc).utctimetuple()))
    valid_end = str(calendar.timegm(
        datetime.now(tz=pytz.utc).utctimetuple()))
    valid_interval = '3600s'
    invalid_start = '999999999999'
    invalid_end = '999999999999'
    invalid_interval = 'abc'

    def test_with_explicit_render(self):
        url = '/nova/hypervisor/spawns?start=' + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spawns.html')

    def test_with_implicit_render(self):
        url = '/nova/hypervisor/spawns?start=' + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spawns.html')

    def _test_no_render_success(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def _test_no_render_bad_request(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_no_render(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_start(self):
        url = "/nova/hypervisor/spawns?end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_end(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_interval(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&render=false"
        self._test_no_render_success(url)

    def test_invalid_start(self):
        url = "/nova/hypervisor/spawns?start=" + self.invalid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_finish(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&end=" + self.invalid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_interval(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.invalid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_render(self):
        url = "/nova/hypervisor/spawns?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=xyz"
        self._test_no_render_bad_request(url)


class NovaApiPerfViewTest(SimpleTestCase):
    # view requires a start_ts, end_ts, and interval string
    valid_start = str(calendar.timegm(
        datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc).utctimetuple()))
    valid_end = str(calendar.timegm(
        datetime.now(tz=pytz.utc).utctimetuple()))
    valid_interval = '3600s'
    invalid_start = '999999999999'
    invalid_end = '999999999999'
    invalid_interval = 'abc'

    def test_with_explicit_render(self):
        url = '/nova/api_perf?start=' + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nova_api_perf.html')

    def test_with_implicit_render(self):
        url = '/nova/api_perf?start=' + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nova_api_perf.html')

    def _test_no_render_success(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def _test_no_render_bad_request(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_no_render(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_start(self):
        url = "/nova/api_perf?end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_end(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_success(url)

    def test_no_interval(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&render=false"
        self._test_no_render_success(url)

    def test_invalid_start(self):
        url = "/nova/api_perf?start=" + self.invalid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_finish(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&end=" + self.invalid_end + \
            "&interval=" + self.valid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_interval(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.invalid_interval + \
            "&render=false"
        self._test_no_render_bad_request(url)

    def test_invalid_render(self):
        url = "/nova/api_perf?start=" + self.valid_start + \
            "&end=" + self.valid_end + \
            "&interval=" + self.valid_interval + \
            "&render=xyz"
        self._test_no_render_bad_request(url)


class LatestStatsViewTest(SimpleTestCase):

    def test_no_render(self):
        uri = '/nova/hypervisor/latest-stats?render=false'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)
        logger.debug("[test_no_render] response = %s",
                     response.content)
        self.assertNotEqual(json.loads(response.content), [])

    def test_with_render(self):
        uri = '/nova/hypervisor/latest-stats?render=true'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)
        logger.debug("[test_with_render] response = %s",
                     response.content)

    def test_default_render(self):
        uri = '/nova/hypervisor/latest-stats'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)
        logger.debug("[test_default_render] response = %s",
                     response.content)


class ResourceViewTest(SimpleTestCase):
    # view requires a start_ts, end_ts, and interval string
    valid_start = str(calendar.timegm(
        datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc).utctimetuple()))
    valid_end = str(calendar.timegm(
        datetime.now(tz=pytz.utc).utctimetuple()))
    valid_interval = '3600s'
    invalid_start = '999999999999'
    invalid_end = '999999999999'
    invalid_interval = 'abc'

    @skip('TODO')
    def test_get_cpu(self):
        end = datetime.now(tz=pytz.utc)
        start = datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc)
        end_ts = calendar.timegm(end.utctimetuple())
        start_ts = calendar.timegm(start.utctimetuple())

        uri = '/intelligence/compute/cpu_stats?start_time=' + \
              str(start_ts) + "&end_time=" + str(end_ts) + "&interval=3600s"

        response = self.client.get(uri)
        logger.debug("[test_get_cpu_stats_view] uri = %s", uri)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json.loads(response.content), [])
        logger.debug("[test_get_cpu_stats_view] response = %s",
                     json.loads(response.content))

    @skip('TODO')
    def test_get_mem(self):
        end = datetime.now(tz=pytz.utc)
        start = datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc)
        end_ts = calendar.timegm(end.utctimetuple())
        start_ts = calendar.timegm(start.utctimetuple())

        uri = '/intelligence/compute/mem_stats?start_time=' + \
              str(start_ts) + "&end_time=" + str(end_ts) + "&interval=3600s"

        response = self.client.get(uri)
        logger.debug("[test_get_mem_stats_view] uri = %s", uri)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json.loads(response.content), [])
        logger.debug("[test_get_mem_stats_view] response = %s",
                     json.loads(response.content))

    @skip('TODO')
    def test_get_disk(self):
        end = datetime.now(tz=pytz.utc)
        start = datetime(2014, 3, 12, 0, 0, 0, tzinfo=pytz.utc)
        end_ts = calendar.timegm(end.utctimetuple())
        start_ts = calendar.timegm(start.utctimetuple())

        uri = '/intelligence/compute/phys_disk_stats?start_time=' + \
              str(start_ts) + "&end_time=" + str(end_ts) + "&interval=3600s"

        response = self.client.get(uri)
        logger.debug("[test_get_phys_disk_stats_view] uri = %s", uri)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json.loads(response.content), [])
        logger.debug("[test_get_phys_disk_stats_view] response = %s",
                     json.loads(response.content))