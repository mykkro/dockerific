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

const renderAction = (targetDiv, actions, act) => {
  // find action type
  var act_type = null;
  for(var type in actions) {
    if(type in act) {
      act_type = type
      break
    }
  }
  const actionSchema = actions[act_type]
  const actionTitle = actionSchema.title
  const actionProps = actionSchema.props || []
  console.log('Action type:', actionTitle)
  actionProps.forEach((p) => {
    const propKey = p.key
    const propDefault = p.default
    const propValue = act[p.key] || propDefault
    console.log("Prop:", propKey, propValue, p.type, p.is_list || false, p.required)
  })
}

const renderDockerific = (targetDiv, schema, data) => {
  const schemaFields = schema.build_actions
  console.log("Rendering Dockerific!")
  console.log("Schema fields:", schemaFields)
  console.log("Data:", data)
  const base_image = data.base
  const actions = data.build
  console.log("Base image:", base_image)
  actions.forEach((a) => {
    renderAction(targetDiv, schemaFields, a)
  })
}

loadJson(url1, (schema) => {
  loadJson(url2, (data) => {
    renderDockerific("#dockerific", schema, data)
  })
})