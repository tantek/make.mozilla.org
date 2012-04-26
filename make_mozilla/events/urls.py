from django.conf.urls.defaults import patterns, url
from make_mozilla.events.views import events

urlpatterns = patterns('',
    url(r'^$',                  events.index,             name = 'events'),
    url(r'^feed.rss$',          events.IndexGeoRSSFeed(), name = 'events-feed'),
    url(r'^new/$',              events.new,               name = 'event.new'),
    url(r'^create/$',           events.create,            name = 'event.create'),
    url(r'^(?P<event_id>\d+)/$', events.details,           name = 'event'),
    url(r'^bsd/page/event/create/$',    events.bsd_create,  name='bsd_event_create'),
    url(r'^bsd/ctl/Constituent/Login/$',    events.bsd_create_user, name='bsd_create_user'),
    url(r'^bsd/page/event/create_details/$',    events.bsd_create_details, name='bsd_create_details'),
    url(r'^bsd/page/event/share/$', events.bsd_share, name='bsd_share'),
    url(r'^bsd/page/event/manage/$', events.bsd_manage, name='bsd_manage'),
    url(r'^bsd/page/event/invite/$', events.bsd_invite, name='bsd_invite'),
    url(r'^bsd/page/event/myevents/$', events.bsd_my, name='bsd_myevents'),
    url(r'^bsd/page/event/detail/$', events.bsd_detail, name='bsd_detail'),
    url(r'^bsd/page/event/rsvp_save/$', events.bsd_rsvp_save, name='bsd_rsvp_save'),
)

