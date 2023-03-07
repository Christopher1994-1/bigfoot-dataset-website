document.getElementById('my-form').addEventListener('click', function(event) {
  // only handle clicks on submit buttons
  if (event.target.tagName.toLowerCase() === 'input' && event.target.type === 'submit') {

    // get the value of the corresponding "number" input field
    var numberInput = event.target.parentNode.querySelector('#number');
    var numberValue = numberInput.innerHTML.trim();

    fetch('/my-endpoint', {
      method: 'POST',
      body: JSON.stringify({ data: numberValue }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
  }
});