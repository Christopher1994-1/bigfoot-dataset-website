
function selected(county) {
    fetch(`/county_selection?county=${county}`)
      .then(response => response.text())
      .then(html => {
        document.open("text/html").write(html);
        document.close();
        history.pushState(null, null, `/?county=${county}`);
      })
      .catch(error => console.log(error));
  }


