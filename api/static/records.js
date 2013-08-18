$(document).ready(function() {
	function dnsField(k, v, field, master) {
		var attr = document.createElement('td')
		$(attr).attr('id', v['id'])
			   .attr('value', v[field])
			   .appendTo($(master))
		if(field == 'kill') {
			var kill_function = "$.get('/dns/delete/record/"+v['id']+"', function(res, stat) { window.location.reload() })"
			$(attr).html('<img src="/static/Delete.png" width="28" height="28" id="kill" onClick="'+kill_function+'"></img>')
			return true
		}
		else if(field == 'type') {
			var dropdown = document.createElement('select')
			var types = new Object()
			types.MX = document.createElement('option')
			types.CNAME = document.createElement('option')
			types.SOA = document.createElement('option')
			for(var type in types) {
				$(types[type]).appendTo($(dropdown))
					   .attr('value', type)
					   .html(type)
				if(type == v['type']) {
					$(types[type]).attr('selected', 'selected')
				}
			}
			$(dropdown).attr('id', v['id'])
					   .attr('class', v['id'])
					   .css('height', '19')
					   .appendTo($(attr))
			return true
		}
		$(attr).html('<div id="'+v['id']+'" contenteditable><span>' + v[field] + '</span></div>')
		return true
	}
	$.get('/dns/report/record', function(res, stat) {
        $.each(res, function(k, v) {
			var sudo = document.createElement('tr')
			var master = v.name + '.sudo'
			$(sudo).attr('id', master)
			dnsField(k, v, 'domain_id', sudo)
			dnsField(k, v, 'name', sudo)
			dnsField(k, v, 'type', sudo)
			dnsField(k, v, 'content', sudo)
			//dnsField(k, v, 'prio', sudo)
			dnsField(k, v, 'ttl', sudo)
			dnsField(k, v, 'kill', sudo)
			//dnsField(k, v, 'change_date', sudo)
			//dnsField(k, v, 'ordername', sudo)
			//dnsField(k, v, 'auth', sudo)
			$('#report_body').append(sudo)
        })
    })
})
