$(document).ready(function() {
	function addButton(text, attr, func) {
		var btn = document.createElement('button')
		$(btn).attr('class', 'btn')
			  .attr('onclick', func)
			  .html(text)
			  .appendTo($(attr))
	}
	function dnsField(k, v, field, master) {
		var attr = document.createElement('td')
		/*if (field == 'name') {
			$(attr).html('<div id="'+v['id']+'" contenteditable>' + v[field] + '</div>')
			return true
		}*/
		if(field == 'commit') {
			//var params = "/all[0]['value']/all[1]['value']/all[2]['value']/all[3]['value']/all[4]['value']/all[5]['value']"
			///var commit_function = "$.get('/dns/update/domain/"+params+"', function(res, stat) { window.location.reload() })"
//			var commit_function = "var all = $('td."+v['id']+"').each(function() { return $(this).val() }); $.get('/dns/update/domain"+params+"', function(res,stat) { window.location.reload() })"
			var commit_function = "var all = new Array(); $('td."+v['id']+"').each(function() { all.push($(this).val()) }); all = all.join('/'); $.get('/dns/update/domain/'+all, function(res,stat) { window.location.reload() });"
			addButton('commit', master, commit_function)
			return true
		}
		else if(field == 'id') {
			$(attr).hide()
		}
		else if(field == 'delete') {
			var kill_function = "$.get('/dns/delete/domain/"+v['id']+"', function(res, stat) { window.location.reload() })"
			addButton('delete', master, kill_function)
			return true
		}
		$(attr).attr('id', v['id'])
			   .attr('value', v[field])
			   .attr('class', v['id'])
			   .appendTo($(master))
		$(attr).html('<div id="'+v['id']+'" contenteditable>' + v[field] + '</div>')
		return true
	}
	$('#createdomain').click(function() {
		$.get('/dns/create/domain/'+$('#newdomain').val(), function(res, stat) {
			window.location.reload()
		})
	})
	$.get('/dns/report/domain', function(res, stat) {
        $.each(res, function(k, v) {
			var sudo = document.createElement('tr')
			var master = v.name + '.sudo'
			$(sudo).attr('id', master)
			dnsField(k, v, 'id', sudo)
			dnsField(k, v, 'name', sudo)
			dnsField(k, v, 'master', sudo)
			dnsField(k, v, 'last_check', sudo)
			dnsField(k, v, 'type', sudo)
			dnsField(k, v, 'notified_serial', sudo)
			dnsField(k, v, 'account', sudo)
			dnsField(k, v, 'commit', sudo)
			dnsField(k, v, 'delete', sudo)
			$('#report_body').append(sudo)
        })
    })
	addButton('commit all', "#domain_list", "alert('test')")
})
