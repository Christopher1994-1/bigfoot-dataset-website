function data() {
  const store_value = [];

  // Get the input value
  const input = document.getElementById("id_number").innerHTML;

  if (store_value.length === 0) {
    // Store the input value in the array if it doesn't have any other value
    store_value.push(input);

    // Send the input to the backend without waiting for a response
    fetch("/get_id_number", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    });
  }
}
