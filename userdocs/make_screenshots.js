/*
invoke using 

  phantomjs make_screenshots.js
  
*/

//~ Load library functions
//~ phantom.libraryPath = '../../lino/media/phantomjs'
phantom.injectJs('/home/luc/hgwork/lino/lino/media/phantomjs/screenshooter.js');

//~ Configuration options
SERVER_ROOT = 'http://127.0.0.1:8000';

var system = require('system');
//~ var LANGUAGE = system.env.OVERRIDE_USER_LANGUAGE;
var LANGUAGE = system.args[1];

OUTPUT_ROOT = '.build/' + LANGUAGE + '/gen/screenshots';

var fs = require('fs');

if (!fs.exists(OUTPUT_ROOT)) { console.error('OUTPUT_ROOT does not exist:' + OUTPUT_ROOT); phantom.exit()}


//~ Declare screenshots to take

add_screenshot('?ul='+LANGUAGE,'index.png');

add_screenshot('/api/cal/CalendarPanel?ul='+LANGUAGE,'cal.CalendarPanel.png');
add_screenshot('/api/cal/CalendarPanel?su=8&ul='+LANGUAGE,'cal.CalendarPanel-su.png');
//~ add_screenshot('/api/cal/PanelEvents/266?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');
add_screenshot('/api/cal/PanelEvents/105?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');

add_screenshot('/api/pcsw/Clients?ul='+LANGUAGE,'pcsw.Clients.grid.png');
add_screenshot('/api/pcsw/Clients/122?ul='+LANGUAGE,'pcsw.Client.detail.png');
add_screenshot('/api/pcsw/Clients/122?tab=1&ul='+LANGUAGE,'pcsw.Client.detail.1.png');
add_screenshot('/api/pcsw/Clients/122?tab=2&ul='+LANGUAGE,'pcsw.Client.detail.2.png');

add_screenshot('/api/debts/Budgets/2?ul='+LANGUAGE,'debts.Budget.detail.png');
add_screenshot('/api/debts/Budgets/2?tab=1&ul='+LANGUAGE,'debts.Budget.detail.1.png');
add_screenshot('/api/debts/Budgets/2?tab=2&ul='+LANGUAGE,'debts.Budget.detail.2.png');
add_screenshot('/api/debts/Budgets/2?tab=3&ul='+LANGUAGE,'debts.Budget.detail.3.png');
add_screenshot('/api/debts/Budgets/2?tab=4&ul='+LANGUAGE,'debts.Budget.detail.4.png');
add_screenshot('/api/jobs/JobsOverview?ul='+LANGUAGE,'jobs.JobsOverview.png');
    
  
//~ Start working
next_task();
