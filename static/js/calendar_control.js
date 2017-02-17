TD_TAG = 'TD';
CURRENT_DEBUG_LVL = 2; // 0 = allways, 1  = usual debug, 2 = deep debug
CALENDAR_DAY_CLASS = 'calendar_day'

STATUS_OCCUPIED = 1;
STATUS_FREE = 2;

window.uncommitted_schedule_recordes = {}
window.schedule_recordes = {}
var ScheduleRecord = function (date, status){
	this.date = date;
	this.status = status;
}


function debug(msg, level){
	// set defualt debug level
	level = typeof level!== 'undefined' ? level : 0;
	
	if (CURRENT_DEBUG_LVL >= level){
		console.log(msg);
	}
};



/*function get_schedule_recordes(){
	debug("get_schedule_recordes",1)
	window.scheduler_records = {}
}
function send_schedule records(){
	debug("get_schedule_recordes",1);
}*/
function get_date_from_id(id){
	return id.split( "_")[2];
}

function get_schedule_recordes_from_server(){
	$.post( "/get_schedule_records")
		  .done(function(response) {
			window.schedule_recordes = JSON.parse(response);
			update_schedule();
			debug( "get_schedule_recordes_from_server: success" ,2);
		  })
		  .fail(function() {
			debug( "get_schedule_recordes_from_server: error" , 2);
		  })
		  .always(function() {
			$("#loading_img").css('visibility', 'hidden');
		});
}

function update_schedule(){
	$.each(window.schedule_recordes, function(key, val){
			day_id = window.calendar_id + "_" + key
			
			// Remove any marked classes
			$("#"+day_id).removeClass('free_day');
			$("#"+day_id).removeClass('occupied');
			
			// Add marked classes
			switch(val){
				case STATUS_OCCUPIED:
					$("#"+day_id).addClass('occupied');
					break;
				case STATUS_FREE:
					$("#"+day_id).addClass('free_day');
					break;
			}
		});
}

function commit_uncommitted_schedule_recordes(){
	debug("commit_uncommitted_schedule_recordes function", 1)
	window.temp_schedule_recordes_list = []
	$.each(window.uncommitted_schedule_recordes, function(date,val) {
		window.temp_schedule_recordes_list.push(val)
	});	
	window.uncommitted_schedule_recordes = {}
	if (window.temp_schedule_recordes_list.length > 0){
		$.post( "/commit_schedule_records_changes", JSON.stringify(window.temp_schedule_recordes_list))
		  .done(function() {
		  
			$.each(window.temp_schedule_recordes_list, function(key, val){
				window.schedule_recordes[val.date] = val.status
				});
			debug( "commit_uncommitted_schedule_recordes: success" ,2);
		  })
		  .fail(function() {
			$.each(window.temp_schedule_recordes_list, function(key, val){
				window.uncommitted_schedule_recordes[val.date] = val
				});
			debug( "commit_uncommitted_schedule_recordes: error" , 2);
		  })
		  .always(function() {
			$("#loading_img").css('visibility', 'hidden');
		});
		debug( "commit_uncommitted_schedule_recordes: Request sent." ,2);
		$("#loading_img").css('visibility', 'visible');
	}
	
}

function set_events(){
	
	$('.' + CALENDAR_DAY_CLASS).unbind('click').click(function(event){
		debug("Day clicked",2)
		window.e = event;
		target = event.target;
		if(target.classList[0] != CALENDAR_DAY_CLASS){
			if (target.parentElement.classList[0] != CALENDAR_DAY_CLASS) {
				debug('Error: I didn\'t find any ' + CALENDAR_DAY_CLASS + ' class. Current tag: '+ target.tagName,0);
				return
			}
			else {
				target = event.target.parentElement;
			}
		}
		debug("Day target selected:",2);
		debug(target,2);
		
		if($(target).hasClass('selected') != true){
			debug("Day doesn't have 'selected' class.",2)
			$(target).addClass('selected')
		}
		else{
			debug("Day does have 'selected' class.",2)
			$(target).removeClass('selected')
		}
	});
	
	$('#mark_as_free').unbind('click').click(function(event){ 

		$.each($('.calendar_day.selected'), function(i,day) {
			debug("free: " + day.id,2);
			
			// Add the current day to window.uncommitted_schedule_recordes  as free day
			date = get_date_from_id(day.id);
			window.uncommitted_schedule_recordes[date] = new window.ScheduleRecord(date,STATUS_FREE)
			
			// Handle classes style
			$(day).addClass('free_day');
			$(day).removeClass('occupied');
			$(day).removeClass('selected');
			});
		commit_uncommitted_schedule_recordes();
		});

	$('#mark_as_occupied').unbind('click').click(function(event){ 

		$.each($('.calendar_day.selected'), function(i,day) {
			debug("occupied: " + day.id,2);
			
			// Add the current day to window.uncommitted_schedule_recordes  as occupied day
			date = get_date_from_id(day.id);
			window.uncommitted_schedule_recordes[date] = new window.ScheduleRecord(date,STATUS_OCCUPIED)

			// Handle classes style
			$(day).addClass('occupied');
			$(day).removeClass('free_day');
			$(day).removeClass('selected');
			});
		commit_uncommitted_schedule_recordes();

		});
	$('#clear_selected_days').click(function(event){ 
		debug("clear_selected_days clicked",1)
		$.each($('.calendar_day.selected'), function(i,day) {
			$(day).removeClass('selected');
			});
		});	
}

/*
TO DO:
	- save marked (blue) days when switching months
*/