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

const loadJson = (url, done) => {
  $.ajax({
    url: url,
    dataType: 'json',
    success: function(data) {
      // Code to handle the loaded JSON data goes here
      done(data)
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log('Error loading JSON file:', textStatus, errorThrown);
    }
  });
}
  
var url1 = '/api/schema'
var url2 = '/api/project/ros2-foxy-moveit'

loadJson(url1, (schema) => {
  loadJson(url2, (data) => {
    console.log(schema, data)
  })
})