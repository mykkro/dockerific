// https://codepen.io/DobsonDev/pen/ByaNZd

// disable animations
jQuery.fx.off = true;

// Show the first tab and hide the rest
$('#tabs-nav li:first-child').addClass('active');
$('.tab-content').hide();
$('.tab-content:first').show();

// Click function
$('#tabs-nav li').click(function(){
  $('#tabs-nav li').removeClass('active');
  $(this).addClass('active');
  $('.tab-content').hide();
  
  var activeTab = $(this).find('a').attr('href');
  $(activeTab).fadeIn();
  return false;
});

// load calendar data and create calendar
// TODO later serve it directly from app.py
var url = '/calendar/main'
$.ajax({
  url: url,
  dataType: 'json',
  success: function(data) {
    // Code to handle the loaded JSON data goes here
    console.log("Data loaded:", data)
    renderCalendar("#calendar-main", data)
  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log('Error loading JSON file:', textStatus, errorThrown);
  }
});

const renderCalendar = (divName, data) => {
  const events = data.events
  events.forEach((e) => {
    console.log("Event:", e)
  })
}