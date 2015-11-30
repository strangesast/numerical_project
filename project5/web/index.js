var canvas_properties = document.getElementById("canvas-properties");

var initialize = function(canvas, width, height) {
  canvas.width = width;
  canvas.height = height;
  var context = canvas.getContext('2d');
  return Promise.resolve(context);
};

var initialize_button = canvas_properties.querySelector('button');

var draw_background = function(ctx, width, height) {
  ctx.fillStyle="blue";
  ctx.fillRect(0, 0, width, height);
};

var draw_hill = function(ctx, func, range, width, height) {
  var y = [];
  var x = [];
  for(var i=range[0]; i < range[1]; i++) {
    x.push(i);
    y.push(func(i));
  }
  console.log(x);
  console.log(y);

};

initialize_button.addEventListener('click', function(e) {
  var width = canvas_properties.querySelector("[name=width]").value;
  var height = canvas_properties.querySelector("[name=height]").value;

  // get hill function... or just use this
  var hill_function = function(x) {
    //return 1000*Math.exp(Math.pow(x-4800, 2)/10e6);
    return 1000*Math.exp(Math.pow((x-4800), 2)/10000000);
  };
  var range = [0, 5000];

  initialize(document.getElementById("canvas"), width, height).then(function(ctx) {
    draw_background(ctx, width, height);
    draw_hill(ctx, hill_function, range, width, height);
  });
});
