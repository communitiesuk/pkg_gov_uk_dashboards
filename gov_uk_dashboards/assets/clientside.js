
// assets/clientside.js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
  utils: {
    setTitle: function (title) {
      if (typeof title === "string" && title.trim().length > 0) {
        document.title = title;
      }
      // Return something to satisfy Dash's need for an output value
      return title;
    }
  }
});
