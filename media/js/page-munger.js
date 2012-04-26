var webmaker = window.webmaker || {};

webmaker.munge = function() {
	var pages, init;
	pages = [
		{
			frag : 'rsvp_save'
		},
		{
			frag : 'create_details',
			onload : function() {
				var msg = $('td.required').html();
				$('<p>' + msg + '</p>').insertAfter($('h2.header'));
			}
		},
		{
			frag : 'create',
			onload : function() {
				var types = $('table.typedesc').remove(),
					move_to = $('#event_zip_row'),
					target = $('<td colspan="2"></td>').appendTo($('<tr></tr>')).insertAfter(move_to);
				target.append(types);
			}
		},
		{
			frag : 'manage',
		},
		{
			frag : 'share',
			onload : function() {
				$('#eventdetail').find('input[type="submit"]').attr({
					'value': 'RSVP'
				});
			}
		},
		{
			frag : 'detail',
			onload : function() {
				var event_details = $('div.detailtable_container').remove(),
					target = $('div.description');
				event_details.insertBefore(target);
				var google_a = $('div.maplinks').find('a:first-child')[0],
					google_url = $(google_a).attr('href').split('?q=')[1],
					static_url = 'http://maps.google.com/maps/api/staticmap?center=' + google_url + '&zoom=15&size=250x250&markers=color:blue%7C26455+' + google_url + '&sensor=false',
					img = $('<img />').attr({
						src: static_url,
						alt: ''
					}).addClass('venue_map');
				img.appendTo(event_details);
				var extra_target = $('#extra'),
					to_move = [$('#rsvp_container').remove(), $('#otherrsvps_container').remove()];
				jQuery.each(to_move, function(index, value) {
					value.appendTo(extra_target);
				});
				$('input[type="submit"]').attr({
					'value': 'RSVP'
				});
			}
		}
	];
	init = function() {
		var URL = window.location.href;
		jQuery.each(pages, function(index, value) {
			var frag = value.frag,
				func = value.onload || false;
			if (URL.indexOf(frag) != -1) {
				$('html').addClass(frag);
				$('td.button').removeClass('button');
				if (func) {
					func();
				}
				return false;
			}
		});
	};
	return {
		'init': init
	};
}();

jQuery(function() {
	webmaker.munge.init();
});