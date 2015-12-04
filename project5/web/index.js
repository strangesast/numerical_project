var canvas_properties = document.getElementById("canvas-properties");
var target_properties = document.getElementById("target-properties");
var hill_properties = document.getElementById("hill-properties");
var init_properties = document.getElementById('init-properties');
var fire_button = document.getElementById('fire');
var fire_lots_button = document.getElementById('fire-lots');

var g = 9.81; // m / s^2
var initial_velocity = 350; // m / s
var explosion_radius = 3;

// get canvas context & reset width + height
var initialize = function(canvas, width, height) {
  canvas.width = width;
  canvas.height = height;
  var context = canvas.getContext('2d');
  return Promise.resolve(context);
};

// min / max of large arrays
var max = function(iterable) {
  return iterable.reduce(function(a, b) {
    return a > b ? a : b; 
  });
};

var min = function(iterable) {
  return iterable.reduce(function(a, b) {
    return a < b ? a : b; 
  });
};

var initialize_button = canvas_properties.querySelector('button');

var determine_domain = function(func, range) {
  var y = [];
  for(var i=range[0]; i < range[1]; i++) {
    y.push(func(i));
  }
  var minval = min(y);
  var maxval = max(y);
  return [minval, maxval];
};

var pressure_function = function(y) {
  var a = -4.75/10e8;
  var b = 2.0/10e4;
  return a*y + b;
};

// background shading with pressure lightening
var draw_background = function(ctx, func, range, width, height, hrat) {
  var pressures = [];
  var pressure_interval = 20;
  for(var i=0; i < Math.floor(height / pressure_interval); i++) {
    pressures.push(pressure_function(i*pressure_interval / hrat));
  }
  var maxval = max(pressures);
  var minval = min(pressures);
  for(var j=0; j < pressures.length; j++) {
    var percent = 0.25 + 0.75*(1 - (pressures[j]-minval)/(maxval-minval));
    ctx.fillStyle = 'rgba(173, 216, 230, ' + percent.toString() + ')';
    ctx.fillRect(0, j*pressure_interval, width, pressure_interval);
  }
};


var draw_background = function(ctx, func, range, width, height, hrat) {
  var pressures = [];
  var pressure_interval = 20;
  for(var i=0; i < Math.floor(height / pressure_interval); i++) {
    var hi = i*pressure_interval;
    var ah = hi / hrat; // height in m 
    console.log(rho(ah));
  }
};

var draw_hill = function(ctx, func, range, width, height, hrat) {
  ctx.beginPath();
  ctx.moveTo(0, height-func(range[0])*hrat);
  for(var xi=range[0]; xi < range[1]; xi++) {
    var yi = func(xi)*hrat;
    ctx.lineTo((xi - range[0])/(range[1]-range[0])*width, height - yi);
  }
  ctx.lineTo(width, height);
  ctx.lineTo(0, height);
  ctx.closePath();
  ctx.fillStyle = "black";
  ctx.fill();
};

// vertical labels
var draw_heights = function(ctx, width, height, hrat) {
  ctx.textAlign = 'right';
  for(var i=0; i < Math.floor(height / 100); i++) {
    ctx.fillText(Math.floor(i*100/hrat*100)/100 + 'm', width - 10, height - i*100);
  }
};

// horizontal labels
var draw_widths = function(ctx, width, height, range) {
  ctx.textAlign = 'left';
  for(var i=0; i < Math.floor(width / 100); i++) {
    ctx.save();
    xi = i*100;
    yi = height - 10;
    ctx.translate(xi, yi);
    ctx.rotate(-Math.PI/2);
    ctx.fillText(Math.floor(i*100 / width * (range[1] - range[0]) + range[0]) + 'm', 0, 0);
    ctx.restore();
  }
  ctx.restore();
};

var get_ceiling = function() {
  var ceiling = hill_properties.querySelector('[name=ceiling]').value;
  console.log(ceiling);
  if(isNaN(ceiling) || ceiling == "") {
    alert("invalid ceiling");
    return 1000;
  } else {
    return Number(ceiling);
  }
}

var get_range = function() {
  var range_upper = hill_properties.querySelector('[name=upper_bound]').value;
  var range_lower = hill_properties.querySelector('[name=lower_bound]').value;
  if(isNaN(range_upper) || isNaN(range_lower)) {
    alert("invalid range");
    return [-100, 10100];
  } else {
    return [range_lower, range_upper]
  }
}

var determine_height_rat = function(func, range, height, ceiling) {
  var both = determine_domain(func, range);
  var minval = both[0];
  var maxval = both[1];
  return height/(maxval + ceiling);
};

var draw_start = function(ctx, func, range, width, height, start_pos, hrat) {
  var hill_height = height / 3;
  var xi = width*(start_pos - range[0]) / (range[1]-range[0]);
  var yi = height - func(start_pos)*hrat;

  ctx.fillStyle = 'red';
  ctx.beginPath();
  ctx.arc(xi, yi, 5, 0, Math.PI*2);
  ctx.closePath();
  ctx.fill();
};

var draw_target = function(ctx, func, range, width, height, target_pos, hrat) {
  var xi = width*(target_pos - range[0]) / (range[1]-range[0]);
  var yi = height - func(target_pos)*hrat;

  ctx.fillStyle = 'blue';
  ctx.beginPath();
  ctx.arc(xi, yi, 5, 0, Math.PI*2);
  ctx.closePath();
  ctx.fill();
};

initialize_button.addEventListener('click', function(e) {
  e.target.textContent = 'Reset';
  var width = canvas_properties.querySelector("[name=width]").value;
  var height = canvas_properties.querySelector("[name=height]").value;
  // get hill function... or just use this
  var hill_function = function(x) {
    return 1000*Math.exp(-Math.pow(4800-x, 2)/1000000);
  };

  //var range = [-100, 10200]; // NOTE: should be defined by 'hill properties'
  var range = get_range(); 

  initialize(
    document.getElementById("canvas"),
    width,
    height
  ).then(post_initialization(width, height, hill_function, range));
});

// air pressure
var rho = function(y) {
  var a = -4.75/Math.pow(10, 8);
  var b = 2.0/Math.pow(10, 4);
  var ret = a*y + b;
  if(ret < 0) {
    return 0;
  } else {
    return ret;
  }
};

var fire_over_range = function* (ctx, position, angle_interval, velocity, hill_function, pressure_function, width, height, hrat, range) {
  var gens = [];
  console.log('gens');
  // add generator for each angle
  for(var i=1; i < Math.floor(180 / angle_interval); i++) {
    var angle = angle_interval*i;
    gens.push(fire(ctx, [0, hill_function(0)], angle, velocity, hill_function, pressure_function, width, height, hrat, range));
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

var fire = function* (ctx, position, angle, velocity, hill_function, pressure_function, width, height, hrat, range) {
  var angle_rad = angle*Math.PI / 180;

  var x_c = position[0];
  var y_c = position[1];


  var x_v_c = Math.sin(angle_rad)*velocity;
  var y_v_c = Math.cos(angle_rad)*velocity;

  var ret = [];

  ctx.strokeStyle = 'red';

  var xi = ((x_c-range[0])/(range[1]-range[0]))*width;
  var yi = y_c*hrat;


  var last_xi = xi;
  var last_yi = yi;
  while (y_c >= hill_function(x_c) && y_c < hill_function(range[0]) + 10000 && x_c > range[0] && x_c < range[1]) {
    ctx.beginPath();
    ctx.moveTo(last_xi, height - last_yi);

    x_c += x_v_c/10;
    y_c += y_v_c/10;

    d_v_x = -rho(y_c)*Math.pow(Math.abs(x_v_c), 2)/10;
    d_v_y = -(rho(y_c)*Math.pow(Math.abs(y_v_c), 2) + g)/10;

    x_v_c += d_v_x;
    y_v_c += d_v_y;

    ret = [x_c, y_c, x_v_c, y_v_c];

    xi = ((x_c-range[0])/(range[1]-range[0]))*width;
    yi = y_c*hrat;

    ctx.lineTo(xi, height - yi);
    ctx.stroke();

    last_xi = xi;
    last_yi = yi;
    yield ret;
  }
  ctx.beginPath();
  ctx.fillStyle = 'red';
  ctx.arc(last_xi, height-last_yi, explosion_radius, 0, 2*Math.PI);
  ctx.fill();
  yield ret;
};


var post_initialization = function(width, height, hill_function, range) {
  return function(ctx) {
    var ceiling = get_ceiling();
    var hrat = determine_height_rat(hill_function, range, height, ceiling);
    draw_background(ctx, hill_function, range, width, height, hrat);
    draw_hill(ctx, hill_function, range, width, height, hrat);
    // NOTE: need to update this: needs to be modifiable
    draw_start(ctx, hill_function, range, width, height, 0, hrat);
    draw_heights(ctx, width, height, hrat);
    draw_widths(ctx, width, height, range);
    
    // add event listeners for properties
    var target_update_listener = function(the_context) {
      return function(e) {
        var target_position = e.target.parentElement.querySelector('[name=target_position]').value;
        draw_target(the_context, hill_function, range, width, height, target_position, hrat);
      };
    }(ctx);
  
    target_properties.addEventListener('click', target_update_listener);
  
  
    var fire_button_listener = function(e) {
      var angle = target_properties.querySelector('[name=initial_angle]').value;
      var gen = fire(ctx, [0, hill_function(0)], angle, initial_velocity, hill_function, pressure_function, width, height, hrat, range);
  
      var interval = setInterval(function() {
        var n = gen.next();
        if(n.done) {
          clearInterval(interval);
          console.log("done");
        } else {
          //console.log(n.value);
        }
      }, 10);
    };
  
    fire_button.addEventListener('click', fire_button_listener);
  
    var fire_lots_listener = function(e) {
      var angle_interval = e.target.parentElement.querySelector('[name=angle_interval]').value;
      if(angle_interval === "" || isNaN(angle_interval)){
        alert("invalid angle interval");
        return;
      } else {
        angle_interval = Number(angle_interval);
      }
  
      var gen = fire_over_range(ctx, [0, hill_function(0)], angle_interval, initial_velocity, hill_function, pressure_function, width, height, hrat, range);
      var interval = setInterval(function() {
  
        var n = gen.next();
        if(n.done) {
          clearInterval(interval);
          console.log("done");
        } else {
          //console.log(n.value);
        }
      }, 10);
  
    };
  
    fire_lots_button.addEventListener('click', fire_lots_listener);
  };
};

save_canvas_button = document.getElementById('save-canvas');

save_canvas_event = function(e) {
  var canvas = document.getElementById('canvas');
  var data = canvas.toDataURL("image/png");
  var w=window.open('about:blank','image from canvas');
  w.document.write("<img src='"+data+"' alt='from canvas'/>");
};

save_canvas_button.addEventListener('click', save_canvas_event);
