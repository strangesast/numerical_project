var canvas_properties = document.getElementById("canvas-properties");
var target_properties = document.getElementById("target-properties");
var background_properties = document.getElementById("background-properties");
var init_properties = document.getElementById('init-properties');
var fire_button = document.getElementById('fire');
var fire_lots_button = document.getElementById('fire-lots');
var initialize_button = document.getElementById('initialize');
var canvas_element = document.getElementById('canvas');
var pressure_function_input_element = background_properties.querySelector('[name=pressure_shape]');
var hill_function_input_element = background_properties.querySelector('[name=hill_shape]');
var canvas_width = canvas_properties.querySelector('[name=width]').value;
var canvas_height = canvas_properties.querySelector('[name=height]').value;
var wind_velocity_function_element = background_properties.querySelector('[name=wind_velocity_profile]');
var plot_angles_button = document.getElementById('plot_angles');
var angles_canvas = document.getElementById('range_canvas');

var hill_function = null;
var airdensity_function = null;
var windvelocity_function = null;
var initial_position = null;
var target_position = null;
// xmin, xmax, ymin, ymax
var viewport = null;
var rendering_function = null;
var g = 9.81;

var get_function_from_input = function(input_element) {
  var func;
  var varname = input_element.getAttribute('varname');
  try {
    func = eval('fucn = function(' + varname + ') { return ' + input_element.value + '}'); // jshint ignore:line
  } catch (e) {
    throw "bad function definition at " + input_element.getAttribute('name');
  }
  return func;
};

var canvas_setup = function() {
  // define canvas width / height
  canvas_width = canvas_properties.querySelector('[name=width]').value;
  canvas_height = canvas_properties.querySelector('[name=height]').value;

  return new Promise(function(resolve, reject) {
    canvas_element.width = canvas_width;
    canvas_element.height = canvas_height;

    return resolve();
  });
};

var blendColors = function (c0, c1, p) {
  // taken from: http://stackoverflow.com/a/13542669
      var f=parseInt(c0.slice(1),16),t=parseInt(c1.slice(1),16),R1=f>>16,G1=f>>8&0x00FF,B1=f&0x0000FF,R2=t>>16,G2=t>>8&0x00FF,B2=t&0x0000FF;
          return "#"+(0x1000000+(Math.round((R2-R1)*p)+R1)*0x10000+(Math.round((G2-G1)*p)+G1)*0x100+(Math.round((B2-B1)*p)+B1)).toString(16).slice(1);
};

var draw_background = function() {
  // draw background with air density
  var start_color = background_properties.querySelector('[name=start-color]').value;
  var end_color = background_properties.querySelector('[name=end-color]').value;
  var y_step = 5;
  // only positive densities
  var user = get_function_from_input(pressure_function_input_element);
  airdensity_function = function(y) {
    var userval = user(y);
    return userval > 0 ? userval : 0;
  };
  return new Promise(function(resolve, reject) {
    if(airdensity_function === null) {
      return reject('air density undefined');
    }
    var ctx = canvas_element.getContext('2d');
    var pressures = [];
    var ymin = viewport[2];
    var ymax = viewport[3];
    for(var i=0; i < Math.floor(canvas_height / y_step); i++) {
      var hi = i*y_step;
      var a = ymin + (ymax - ymin)*hi/canvas_height;
      var p = airdensity_function(ymin + (ymax - ymin)*hi/canvas_height);
      pressures.push(p);
    }

    var fmin = pressures.reduce(function(a, b) { return a > b ? a : b;});
    var fmax = pressures.reduce(function(a, b) { return a < b ? a : b;});

    for(var j=0; j < pressures.length; j++) {
      var percent = Math.floor((pressures[j]-fmin)/(fmax-fmin)*1000)/1000;
      ctx.fillStyle = blendColors(start_color, end_color, percent);
      ctx.fillRect(0, canvas_height - j*y_step, canvas_width, y_step);
    }

    return resolve();
  });
};

var draw_unit_labels = function() {
  return new Promise(function(resolve, reject) {
    var ctx = canvas_element.getContext('2d');
    ctx.textAlign = "left";
    ctx.fillStyle = "red";
    var text;
    for(var i=0; i < viewport[1]-viewport[0]; i+= Math.floor((viewport[1]-viewport[0])/Math.floor(canvas_width/100))) {
      text = viewport[0] + i;
      var xi = i/(viewport[1]-viewport[0])*canvas_width;
      ctx.save();
      ctx.translate(xi, canvas_height);
      ctx.rotate(-Math.PI/2);
      ctx.fillText(text, 10, 0);
      ctx.restore();
    }
    ctx.textAlign = "right";
    for(var j=0; j < viewport[3]-viewport[2]; j+= Math.floor((viewport[3]-viewport[2])/Math.floor(canvas_height/100))) {
      var yi = canvas_height*(1 - j/(viewport[3]-viewport[2]));
      console.log(j);
      text = viewport[2] + j;
      ctx.fillText(text, canvas_width, yi);
      ctx.restore();
    }

    return resolve();
  });
};

var draw_hill = function() {
  hill_function = get_function_from_input(hill_function_input_element);
  return new Promise(function(resolve, reject) {
    if(hill_function === null) {
      return reject('hill profile undefined');
    }
    var ctx = canvas_element.getContext('2d');
    var x_step = 10;
    var xmin = viewport[0];
    var xmax = viewport[1];
    var ymin = viewport[2];
    var ymax = viewport[3];
    ctx.beginPath();
    ctx.moveTo(0, canvas_height + (1-(hill_function(xmin)-ymin)/(ymax-ymin)));
    var yi = 0;
    for(var i=0; i < Math.floor(canvas_width / x_step); i++) {
      var hi = i*x_step;
      var xval = xmin + (xmax-xmin)*(hi / canvas_width);
      var yval = hill_function(xval);
      var xi = (xval - xmin)/(xmax - xmin)*canvas_width;
      yi = (yval - ymin)/(ymax - ymin)*canvas_height;
      ctx.lineTo(xi, canvas_height - yi);
    }
    ctx.lineTo(canvas_width, canvas_height-yi);
    ctx.lineTo(canvas_width, canvas_height);
    ctx.closePath();
    ctx.fillStyle = background_properties.querySelector("[name=hill_color]").value;
    ctx.fill();
    return resolve();
  });
};

var initialize_positions = function() {
  var target_x = (target_position-viewport[0])/(viewport[1]-viewport[0])*canvas_width;
  var target_y = (hill_function(target_position)-viewport[2])/(viewport[3]-viewport[2])*canvas_height;
  var initial_x = (initial_position-viewport[0])/(viewport[1]-viewport[0])*canvas_width;
  var initial_y = (hill_function(initial_position)-viewport[2])/(viewport[3]-viewport[2])*canvas_height;
  console.log(target_x, target_y);
  return new Promise(function(resolve, reject) {
    var ctx = canvas_element.getContext('2d');
    ctx.beginPath();
    ctx.arc(target_x, canvas_height - target_y, 5, 0, Math.PI*2, false);
    ctx.fillStyle = 'pink';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(initial_x, canvas_height - initial_y, 5, 0, Math.PI*2, false);
    ctx.fillStyle = 'orange';
    ctx.fill();
    return resolve();
  });
};
var fire = function* (initial_coordinates, angle, velocity, step_size, render) {
  var angle_rad = 1/2*Math.PI - angle*Math.PI / 180;
  var current_x_pos = initial_coordinates[0];
  var current_y_pos = initial_coordinates[1];

  var current_x_vel = Math.sin(angle_rad)*velocity;
  var current_y_vel = Math.cos(angle_rad)*velocity;
  var ret = [];
  var last_x = current_x_pos;
  var last_y = current_y_pos;

  while (current_y_pos >= hill_function(current_x_pos) && (current_y_pos < viewport[3] || true) && current_x_pos > viewport[0] && current_x_pos < viewport[1]) {
    if(windvelocity_function !== null) {
      windvelocity = windvelocity_function(current_y_pos);
    } else {
      windvelocity = 0;
    }
    current_x_pos += (current_x_vel+windvelocity)*step_size;
    current_y_pos += current_y_vel*step_size;

    d_v_x = -airdensity_function(current_y_pos)*Math.pow(Math.abs(current_x_vel), 2)*step_size;
    d_v_y = -(airdensity_function(current_y_pos)*Math.pow(Math.abs(current_y_vel), 2) + g)*step_size;

    current_x_vel += d_v_x;
    current_y_vel += d_v_y;

    ret = [current_x_pos, current_y_pos, current_x_vel, current_y_vel];
    if(rendering_function !== null && render === true) {
      rendering_function([last_x, last_y], [current_x_pos, current_y_pos], false);
    }

    last_x = current_x_pos;
    last_y = current_y_pos;

    yield ret;
  }
  if (rendering_function !== null && render === true) {
    rendering_function([last_x, last_y], [current_x_pos, current_y_pos], true);
  }
  record_run(angle, ret);
  yield ret;
};

var initialize_render_function = function(viewport_array) {
  var ctx = canvas.getContext('2d');
  var strokeColor = 'red';
  return function(start, stop, last) {
    ctx.beginPath();

    var startx = (start[0]-viewport_array[0])/(viewport_array[1]-viewport_array[0])*canvas_width;
    var starty = (1-(start[1]-viewport_array[2])/(viewport_array[3]-viewport_array[2]))*canvas_height;
    var endx = (stop[0]-viewport_array[0])/(viewport_array[1]-viewport_array[0])*canvas_width;
    var endy = (1-(stop[1]-viewport_array[2])/(viewport_array[3]-viewport_array[2]))*canvas_height;
    ctx.moveTo(startx, starty);
    ctx.lineTo(endx, endy);
    ctx.strokeStyle = strokeColor;
    ctx.stroke();
    if(last === true) {
      // render 'exposion'
      ctx.beginPath();
      ctx.fillStyle = 'red';
      ctx.arc(endx, endy, 5, 0, 2*Math.PI);
      ctx.fill();
    }
  };
};

var initialize_canvas = function(e) {
  // update globals
  // get x/y range
  e.target.textContent = "Reset";
  var x_lower_bound = Number(background_properties.querySelector("[name=x_lower_bound]").value);
  var x_upper_bound = Number(background_properties.querySelector("[name=x_upper_bound]").value);
  var y_lower_bound = Number(background_properties.querySelector("[name=y_lower_bound]").value);
  var y_upper_bound = Number(background_properties.querySelector("[name=y_upper_bound]").value);
  viewport = [x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound];

  rendering_function = initialize_render_function(viewport);
  windvelocity_function = get_function_from_input(wind_velocity_function_element);


  target_position = Number(init_properties.querySelector('[name=target_position]').value);
  initial_position = Number(init_properties.querySelector('[name=initial_position]').value);

  // get y range
  canvas_setup().then(draw_background).then(draw_hill).then(initialize_positions).then(draw_unit_labels).catch(function(reason) {
    alert('failed: ' + reason);
    return;
  });
};


initialize_button.addEventListener('click', initialize_canvas);

var record_run = function(angle, last) {
  var last_fires = document.getElementById('last_fires');

  var end_x = last[0];
  var end_y = last[1];
  var target_x = target_position;
  var target_y = hill_function(target_position);
  var distance = Math.sqrt(Math.pow(end_x - target_x, 2) + Math.pow(end_y - target_y, 2));
  elem = document.createElement('tr');
  var e1 = document.createElement('td');
  e1.textContent = angle;
  var e2 = document.createElement('td');
  e2.textContent = distance;
  elem.appendChild(e1);
  elem.appendChild(e2);
  last_fires.querySelector('tbody').appendChild(elem);
};

fire_listener = function(e) {
  var step_size = Number(init_properties.querySelector('[name=step_size]').value);
  return new Promise(function(resolve, reject) {
    var angle = init_properties.querySelector('[name=initial_angle]').value;
    var velocity = init_properties.querySelector('[name=muzzle_velocity]').value;

    var gen = fire(
        [initial_position, hill_function(initial_position)],
        angle,
        Number(velocity),
        step_size,
        true
        );

    var lastval = null;
    if(init_properties.querySelector('[name=animate]').checked) {
      var interval = setInterval(function() {
        var n = gen.next();
        if(n.done) {
          console.log(lastval);
          clearInterval(interval);
        } else {
          lastval = n.value;
        }
      }, 10);
    } else {
      var n = gen.next();
      while(n.done !== true) {
        n = gen.next();
        if(n.done === true) {
          console.log(lastval);
        } else {
          lastval = n.value;
        }
      }
    }


    return resolve();
  });
};

fire_button.addEventListener('click', function() {
  Promise.resolve().then(fire_listener).catch(function(reason) {
    alert('failed: ' + reason);
  });
});

var fire_over_range = function* (initial_coordinates, start_angle, end_angle, angle_step, step_size, velocity, render) {
  var gens = [];
  for(var anglei=start_angle; anglei < end_angle; anglei+=angle_step) {
    gens.push(fire(initial_coordinates, anglei, Number(velocity), step_size, render));
  }
  var trials = 0;
  while(gens.length > 0 && trials < 1000) {
    for(var j=0; j < gens.length; j++) {
      var n = gens[j].next();
      if(n.done) {
        gens[j] = null;
      }
    }
    var k = 0;
    // remove dead generators
    while(k < gens.length) {
      if(gens[k] === null) {
        gens.splice(k, 1);
      } else {
        k++;
      }
    }
    yield;
    trials++;
  }
};


fire_lots_listener = function(e) {
  fire_lots_button.disabled = true;
  var step_size = Number(init_properties.querySelector('[name=step_size]').value);
  return Promise.resolve().then(function() {
    var angle_step = Number(init_properties.querySelector('[name=angle_step]').value);
    var angle_start = Number(init_properties.querySelector('[name=angle_start]').value);
    var angle_stop = Number(init_properties.querySelector('[name=angle_stop]').value);
    console.log(angle_step, angle_start, angle_stop);
    var velocity = init_properties.querySelector('[name=muzzle_velocity]').value;
    var gen = fire_over_range([initial_position, hill_function(initial_position)], angle_start, angle_stop, angle_step, step_size, velocity, true);
    var n = gen.next();
    while(!n.done) {
      n = gen.next();
    }
  }).then(function() {
    fire_lots_button.disabled = false;
  });
};

fire_lots_button.addEventListener('click', function() {
  fire_lots_listener().catch(function(reason) {
    alert('failed: ' + reason);
  });
});

save_canvas_button = document.getElementById('save-canvas');

save_canvas_event = function(e) {
  var canvas = document.getElementById('canvas');
  var data = canvas.toDataURL("image/png");
  var w=window.open('about:blank','image from canvas');
  w.document.write("<img src='"+data+"' alt='from canvas'/>");
};

save_canvas_button.addEventListener('click', save_canvas_event);

plot_angles_event = function(e) {
  var table = document.getElementById('last_fires').querySelector('tbody');
  var x = [];
  var y = [];
  var rows = table.querySelectorAll('tr');
  for(var i=0; i < rows.length; i++) {
    var columns = rows[i].querySelectorAll('td');
    x.push(Number(columns[0].textContent));
    y.push(Number(columns[1].textContent));
  }
  if(x.length === 0) {
    return;
  }
  var ctx = angles_canvas.getContext('2d');
  xmax = x.reduce(function(a, b) {return a > b ? a : b;});
  xmin = x.reduce(function(a, b) {return a < b ? a : b;});
  ymax = y.reduce(function(a, b) {return a > b ? a : b;});
  ymin = y.reduce(function(a, b) {return a < b ? a : b;});

  ctx.fillStyle = 'red';
  var padding = 50;
  for(var j=0; j < x.length; j++) {
    var xi = padding + (x[j]-xmin)/(xmax-xmin)*(angles_canvas.width-2*padding);
    var yi = padding + ((1-(y[j]-ymin)/(ymax-ymin))*(angles_canvas.height-2*padding));
    ctx.beginPath();
    ctx.lineTo(xi, yi);
    ctx.arc(xi, yi, 2, 0, 2*Math.PI, false);
    ctx.fill();
  }
  ctx.fillStyle = 'black';
  ctx.textBaseline = 'middle';
  ctx.strokeStyle = 'lightblue';
  ctx.textAlign = 'right';
  var x_step = 20;
  for(var k=0; k < Math.floor((angles_canvas.width - padding*2) / x_step); k++) {
    ctx.save();
    ctx.translate(padding + k*x_step, angles_canvas.height-padding+5);
    ctx.rotate(-Math.PI/2);
    ctx.fillText(Math.round((k*x_step/(angles_canvas.width-padding*2)*(xmax-xmin)+xmin)), 0, 0);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(angles_canvas.height-2*padding+5, 0);
    ctx.stroke();
    ctx.restore();
  }
  for(var l=0; l < Math.floor((angles_canvas.height - padding*2) / x_step); l++) {
    ctx.fillText(
        Math.round((l*x_step/(angles_canvas.height-2*padding)*(ymax-ymin)+ymin)),
        angles_canvas.width,
        angles_canvas.height - (padding+l*x_step)
        );
    ctx.beginPath();
    ctx.moveTo(angles_canvas.width-padding, angles_canvas.height - (padding+l*x_step));
    ctx.lineTo(padding, angles_canvas.height - (padding+l*x_step));
    ctx.stroke();
  }

};

plot_angles_button.addEventListener('click', plot_angles_event);

save_angles_canvas_button = document.getElementById('save-angles-canvas');

save_angles_canvas_event = function(e) {
  var canvas = document.getElementById('range_canvas');
  var data = canvas.toDataURL("image/png");
  var w=window.open('about:blank','image from canvas');
  w.document.write("<img src='"+data+"' alt='from canvas'/>");
};

save_angles_canvas_button.addEventListener('click', save_angles_canvas_event);
