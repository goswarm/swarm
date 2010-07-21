/* THIS FUNCTION WILL TRIM WHITESPACE FROM BEFORE/AFTER A STRING */
String.prototype.trim = function() {
	return this.replace(/^\s+/, '').replace(/\s+$/, '');
};

/* THIS FUNCTION WILL ESCAPE ANY HTML ENTITIES SO "Quoted Values" work */
String.prototype.escape_html = function() {
	return this.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
};
/* This removes HTML */
String.prototype.remove_html = function() {
	return this.replace(/</g, " ").replace(/>/g, " ");
};
/* This replaces breaks with newlines */
String.prototype.br2newline = function() {
	return this.replace(/<br\s*\/>/g, "\n").replace(/<br\s*>/g, "\n");
};
/* This replaces newlines with breaks */
String.prototype.newline2br = function() {
	return this.replace(/\n/g, "<br />");
};

(function($){
	a.getListings = function(resource_id) {
		/* This is an outdated piece of code.
			*/
		var fetch = true;
		var listings_options = {
			type: "POST",
			data: { 
				"resource_id": resource_id
			},
			dataType: "html",
			beforeSend: function(XMLHttpRequest) {
				$("#"+resource_id).addClass("am_ajax_loading");
			},
			success: function(data,textStatus,XMLHttpRequest) {
				$("#"+resource_id).html(data);
				$("#"+resource_id).removeClass("am_ajax_loading");
				$('input.am_linkselect').click(function(event){ $(this).select(); });
			}
		};
		switch (resource_id) {
			case 'am_persons_listings':
				listings_options['url'] = '/xhr/people/'+a.profile.id+'/listings/';
				break;
			case 'am_brandables_listings':
				listings_options['url'] = '/xhr/brandables/'+a.brandable.id+'/listings/';
				break;
			case 'am_everyones_listings':
				listings_options['url'] = '/xhr/listings/';
				break;
			default:
				fetch = false;
			    break;
		}
		if (fetch == true) {
			$.ajax(listings_options);
		}
	};
	a.getMoreListings = function(resource_id,starting_listing_id) {
		/* This fetches more listings for any profile displayed.
			*/
		if (typeof(starting_listing_id) == 'undefined') { starting_listing_id = -1; }
		var more_listings_options = {
			type: "POST",
			data: { 
				"resource_id": resource_id,
				"starting_listing_id": starting_listing_id
			},
			dataType: "html",
			beforeSend: function(XMLHttpRequest) {
				$("#"+resource_id+" div.am_more_listings").addClass("am_ajax_loading_fb");
				$("#"+resource_id+" div.am_more_listings a").hide();
			},
			success: function(data,textStatus,XMLHttpRequest) {
				$("#"+resource_id+" div.am_more_listings").remove();
				$("#"+resource_id).append(data);
				$("#"+resource_id+" div.am_more_listings").removeClass("am_ajax_loading_fb");
				$('input.am_linkselect').click(function(event){ $(this).select(); });
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				$("#"+resource_id+" div.am_more_listings a").show();
				$("#"+resource_id+" div.am_more_listings").removeClass("am_ajax_loading_fb");
			}
		};
		switch (resource_id) {
			case 'am_persons_listings':
				more_listings_options['url'] = '/xhr/people/'+a.profile.id+'/listings/';
				break;
			case 'am_brandables_listings':
				more_listings_options['url'] = '/xhr/brandables/'+a.brandable.id+'/listings/';
				break;
			case 'am_everyone_listings':
			default:
				more_listings_options['url'] = '/xhr/listings/';
		}
		$.ajax(more_listings_options);
	};
	
	$.blockUI.defaults.css.width = '500px';
	
	
	/* Edit In Place ****************/
	$.fn.editMe = function(options) {
		/* This creates a field that is editable in place.  When the blur occurs, the value
		   is transfered to the value placeholder, and the parent form submits.
		   TODO: Restrict submission to only occur when the value of the form field is 
		   changed...
		   **/
		var parent_field = 'undefined';
		
		var sendForm = function(form) {
			form.submit();
		};
		
		var blurField = function(event) {
			var $this = $(this);
			$('#'+parent_field.attr('target')+'_cloak').addClass('am_hidden_input');
			$this.removeClass('am_editable_input');
			if (this.tagName == 'INPUT' && this.value != '') {
				var text = this.value.trim().escape_html();
			} else if (this.tagName == 'TEXTAREA' && this.value != '') {
				var text = this.value.trim().escape_html().newline2br();
			} else if (this.tagName == 'SELECT' && this.value != '' && !/---/.test(this.value)) {
				var text = this.value.trim().escape_html();
			}
			parent_field.html(text);
			parent_field.removeClass('am_hidden_field');
			parent_form = $this.parents('form');
			sendForm(parent_form);
		};
		
		var eL = function(event){
			var $this = $(this);
			$this.addClass('am_hidden_field');
			parent_field = $this;
			$('#'+$this.attr('target')+'_cloak').removeClass('am_hidden_input');
			$('#'+$this.attr('target'))
				.addClass('am_editable_input')
				.focus()
				.blur(blurField);
			event.preventDefault();
		};
		
		var settings = {
		
		};
		$.extend(settings,options||{});
		this.each(function(){
			$this = $(this); // the jquery object of each element
			$this.mouseover(function(){$(this).css("background", '#ffc');})
				 .mouseout(function(){$(this).css("background", 'none');})
				 .click(eL);
		});
	};
	$('.am_editme').editMe();
	/* End Edit In Place ************/
	
	
	a.showMessage = function(msg) {
		/* This displays system level messages at the top of the page.
			*/
		var am_messages = $(document.createElement('div'));
		am_messages.attr('id','am_messages');
		am_messages.attr('class','clearfix');
		am_messages.attr('style','display:none;');
		
		var highlight = $(document.createElement('div'));
		highlight.attr('class','ui-state-highlight ui-corner-all');
		highlight.attr('style','padding: 0px 0.7em;');
		
		var message = $(document.createElement('p'));
		message.attr('class','clearfix');
		
		var icon = $(document.createElement('span'));
		icon.attr('class','ui-icon ui-icon-info');
		icon.attr('style','float: left; margin: 0.2em;');
		
		message.html(msg);
		message.prepend(icon);
		highlight.html(message);
		am_messages.html(highlight);
		
		am_messages.prependTo('#am_content').slideDown("slow");
		
		setTimeout(function(){ am_messages.slideUp("slow",function(){ am_messages.remove(); }); }, 5000);
	};
	
	/** Search ******************/
	$('#am_search').inputLabel();
	/** END Search **************/


	/** ** ** ** File Inputs ** ** ** **/
	$('input[type=file]').each(function(){
		/* This makes your upload file buttons look sexy
			*/
		var uploadbuttonlabeltext = $(this).attr('title'); //get title attribut for languagesettings
		if(uploadbuttonlabeltext == ''){
			var uploadbuttonlabeltext = 'Browse';
		} 
		var uploadbutton = '<button type="button" class="am_file_button">'+uploadbuttonlabeltext+'</button>';
		$(this).wrap('<div class="am_fileinputs"></div>');
		$(this).addClass('am_file').css('opacity', 0); //set to invisible
		$(this).parent().append($('<div class="am_fakefile" />').append($('<input type="text" />').attr('id',$(this).attr('id')+'__fake')).append(uploadbutton));
		
		$(this).bind('change', function() {
			$('#'+$(this).attr('id')+'__fake').val($(this).val());;
		});
		$(this).bind('mouseout', function() {
			$('#'+$(this).attr('id')+'__fake').val($(this).val());;
		});
	});
	/** ** ** ** END File Inputs ** ** ** **/

	
	/** ** ** ** Newsletter Form ** ** ** ** **/
	var newsletter_form_options = {
		/* This allows for a simple newsletter signup to exist as a web service.
			*/
		'url': '/xhr/newsletter/',
		'dataType': 'json',
		'resetForm': true,
		'success': function(data, textStatus, XMLHttpRequest) {
			if (data.success == 1) {
				a.showMessage(data.message);
				$('#am_newsletter').inputLabel(data.message,{ color:"green" });
			} else {
				$('#am_newsletter').inputLabel(data.message,{ color:"#F00" });
			}
		}
	};
	$('#am_newsletter_form').ajaxForm(newsletter_form_options);	
	/** ** ** ** End Newsletter Form ** ** ** ** **/
	
	$('input.am_linkselect').click(function(event){ $(this).select(); });

	/** LOGIN FORM *******/
	var login_ajax_options = {
		/* 	This allows for a simple webservice oriented login form to exist so
			the site demonstrates it's dependency on ajax, webservices, 
			and submits authentication as a webservice without full page reloads.
			The action is specified in the form.
			*/
		dataType:"json",
		type:"post",
		beforeSend: function(XMLHttpRequest) {
			// Hide the fields, display a facebook style loader
			$('#am_auth_form').hide('fast');
			$('#am_authenticating').show('fast');
			$('#am_auth_form_error').hide('fast');
		},
		success: function(data, textStatus, XMLHttpRequest) {
			if (data.result.success == 1) {
				window.location.replace("/");
			} else {
				$('#am_auth_form').show('fast');
				$('#am_auth_form_error p').text(data.result.message);
				$('#am_auth_form_error').show('fast');
			}
		},
		complete: function(XMLHttpRequest, textStatus) {
			$('#am_authenticating').hide('fast');
			$("button.am_auth").attr('disabled','');
		},
		error: function() {
			$('#am_auth_form').show('fast');
			$('#am_auth_form_error').show('fast');
		}
	};
	$("#am_auth_form").ajaxForm(login_ajax_options).submit(function(event) { $("button.am_auth").attr('disabled','disabled'); });
	$('#am_password').inputLabel();
	$('#am_email').inputLabel();
	/** END LOGIN ***************/
	
	/** Registration Form *******/
	var registration_ajax_options = {
		/*	This allows for a simple webservice oriented registration for to exist so
			the site demonstrates webservice and ajax necessity and does account 
			creation without full pag reloads. The action is specified in the form.
			*/
		dataType:"json",
		type:"post",
		beforeSend: function(XMLHttpRequest) {
			// Hide the fields, display a facebook style loader
			$('#am_reg_form').hide('fast');
			$('#am_registering').show('fast');
			$('#am_reg_form_error').hide('fast');
			$('.am_error').remove();
		},
		success: function(data, textStatus, XMLHttpRequest) {
			if (data.result.success == 1) {
				window.location.replace(data.result.redirect);
			} else {
				$('#am_reg_form').show('fast');
				$('#am_reg_form_error p').text(data.result.message);
				if (typeof(data.result.errors) != "undefined") {
				    var er = data.result.errors;
					for (var key in er) {
						if (er.hasOwnProperty(key)) {
							s = $(document.createElement("div")).addClass("am_error").text(er[key][0]);
							$("#am_"+key).after(s);
						}
					}
				}
				$('#am_reg_form_error').show('fast');
			}
		},
		complete: function(XMLHttpRequest, textStatus) {
			$('#am_registering').hide('fast');
			$("button.am_reg").attr('disabled','');
		},
		error: function() {
			$('#am_reg_form').show('fast');
			$("button.am_reg").attr('disabled','');
		}
	};
	$('#am_reg_form').ajaxForm(registration_ajax_options).submit(function(event) { $("button.am_reg").attr('disabled','disabled'); });
	/** END Registration ********/

	/** New Profile Form *******/
	var new_profile_ajax_options = {
		/* 	This allows for asynchronous profile creation through a webservice.
			The action is specified in the form.  The site must require JavaScript.
			*/
		dataType:"json",
		type:"post",
		beforeSend: function(XMLHttpRequest) {
			// Hide the fields, display a facebook style loader
			$('#am_new_profile').hide('fast');
			$('#am_new_profiling').show('fast');
			$('#am_new_pro_form_error').hide('fast');
			$('.am_error').remove();
		},
		success: function(data, textStatus, XMLHttpRequest) {
			if (data.result.success == 1) {
				window.location.replace(data.result.redirect);
			} else {
				$('#am_new_profile').show('fast');
				$('#am_new_pro_form_error p').text(data.result.message);
				if (typeof(data.result.errors) != "undefined") {
				    var er = data.result.errors;
					for (var key in er) {
						if (er.hasOwnProperty(key)) {
							s = $(document.createElement("div")).addClass("am_error").text(er[key][0]);
							$("#am_"+key).after(s);
						}
					}
				}
				$('#am_new_pro_form_error').show('fast');
			}
		},
		complete: function(XMLHttpRequest, textStatus) {
			$('#am_new_profiling').hide('fast');
			$("button.am_new_pro").attr('disabled','');
		},
		error: function() {
			$('#am_new_profile').show('fast');
			$("button.am_new_pro").attr('disabled','');
		}
	};
	$('#am_new_profile').ajaxForm(new_profile_ajax_options).submit(function(event) { $("button.am_new_pro").attr('disabled','disabled'); });
	/** END Registration ********/

	/** Update Profile Form *******/
	var profile_update_ajax_options = {
		/* 	This allows for the updating of a profile from an inline editable form or
			asynchronous update request to webservices.The action is specified in the form.
			*/
		dataType:"json",
		type:"post",
		beforeSend: function(XMLHttpRequest) {
			// Hide the fields, display a facebook style loader
			$('.am_error').remove();
		},
		success: function(data, textStatus, XMLHttpRequest) {
			if (data.result.success == 1) {
			} else {
				$('#am_new_pro_form_error p').text(data.result.message);
				if (typeof(data.result.errors) != "undefined") {
				    var er = data.result.errors;
					for (var key in er) {
						if (er.hasOwnProperty(key)) {
							s = $(document.createElement("div")).addClass("am_error").text(er[key][0]);
							$("#am_"+key).after(s);
						}
					}
				}
				$('#am_new_pro_form_error').show('fast');
			}
		},
		complete: function(XMLHttpRequest, textStatus) {
			$('#am_loading').hide('fast');
		},
		error: function() {
		}
	};
	$('#am_update_profile').ajaxForm(profile_update_ajax_options);
	/** END Registration ********/
	
})(jQuery);