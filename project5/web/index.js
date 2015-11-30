var canvas_properties = document.getElementById("canvas-properties");
var target_properties = document.getElementById("target-properties");

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
  })
}

var min = function(iterable) {
  return iterable.reduce(function(a, b) {
    return a < b ? a : b; 
  })
}

var initialize_button = canvas_properties.querySelector('button');

var determine_domain = function(func, range) {
  var y = [];
  for(var i=range[0]; i < range[1]; i++) {
    y.push(func(i));
  }
  var minval = min(y);
  var maxval = max(y);
  return [minval, maxval];
}

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
  for(var i=0; i < pressures.length; i++) {
    var percent = 0.25 + 0.75*(1 - (pressures[i]-minval)/(maxval-minval));
    ctx.fillStyle = 'rgba(173, 216, 230, ' + percent.toString() + ')';
    ctx.fillRect(0, i*pressure_interval, width, pressure_interval)
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
  ctx.textAlign = 'right'
  for(var i=0; i < Math.floor(height / 100); i++) {
    ctx.fillText(Math.floor(i*100/hrat*100)/100 + 'm', width - 10, height - i*100);
  }
}

// horizontal labels
var draw_widths = function(ctx, width, height, range) {
  ctx.textAlign = 'left'
  for(var i=0; i < Math.floor(width / 100); i++) {
    ctx.save();
    xi = i*100;
    yi = height - 10;
    ctx.translate(xi, yi);
    ctx.rotate(-Math.PI/2);
    ctx.fillText(Math.floor(i*100 / width * (range[1] - range[0]) + range[0]) + 'm', 0, 0)
    ctx.restore()
  }
}

var determine_height_rat = function(func, range, height, ceiling) {
  var both = determine_domain(func, range);
  var minval = both[0];
  var maxval = both[1];
  return height/(maxval + ceiling);
}

var draw_start = function(ctx, func, range, width, height, start_pos, hrat) {
  var hill_height = height / 3;
  var xi = width*(start_pos - range[0]) / (range[1]-range[0]);
  var yi = height - func(start_pos)*hrat;

  ctx.fillStyle = 'red';
  ctx.beginPath();
  ctx.arc(xi, yi, 5, 0, Math.PI*2);
  ctx.closePath();
  ctx.fill();
}

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
    return 1000*Math.exp(Math.pow(x-4800, 2)/10e6);
  };
  var range = [-100, 5200];

  initialize(document.getElementById("canvas"), width, height).then(function(ctx) {
    var hrat = determine_height_rat(hill_function, range, height, 10000);
    draw_background(ctx, hill_function, range, width, height, hrat);
    draw_hill(ctx, hill_function, range, width, height, hrat);
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
  });
});

save_canvas = document.getElementById('save-canvas');

save_canvas_event = function(e) {
  var canvas = document.getElementById('canvas');
  var data = canvas.toDataURL("image/png");
  var w=window.open('about:blank','image from canvas');
  w.document.write("<img src='"+data+"' alt='from canvas'/>");
}

save_canvas.addEventListener('click', save_canvas_event);
