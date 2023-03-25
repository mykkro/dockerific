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
  const div = $("<li>").addClass("dockerific-action").appendTo(targetDiv)
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
  div.append($("<h2>").text(actionTitle))
  const propsDiv = $("<ul>").addClass("dockerify-props").appendTo(div)
  actionProps.forEach((p) => {
    const propDiv = $("<li>").addClass("dockerify-prop").appendTo(propsDiv)
    const propKey = p.key
    const propDefault = p.default
    const propIsList = p.list || false
    const propTypeStr = p.type + (!propIsList) ? "" : " list"
    propDiv.append($("<h3>").text(propKey))
    propDiv.append($("<div>").addClass("dockerify-prop-type").text(propTypeStr))
    if(propIsList) {
      const propListValue = act[p.key] || propDefault
      propListValue.forEach((it) => {
        propDiv.append($("<div>").addClass("dockerify-prop-list-value").text(it))
      })
    } 
    else {
      const propValue = act[p.key] || propDefault
      propsDiv.append($("<div>").addClass("dockerify-prop-value").text(propValue))
      }
  })
  return div
}

const renderDockerific = (targetDiv, schema, data) => {
  const schemaFields = schema.build_actions
  console.log("Rendering Dockerific!")
  console.log("Schema fields:", schemaFields)
  console.log("Data:", data)
  const base_image = data.base
  const actions = data.build
  console.log("Base image:", base_image)
  const outerdiv = $("<ul>").addClass("dockerific-actions").appendTo(targetDiv)
  actions.forEach((a) => {
    renderAction(outerdiv, schemaFields, a)
  })
}

loadJson(url1, (schema) => {
  loadJson(url2, (data) => {
    renderDockerific("#dockerific", schema, data)
  })
})