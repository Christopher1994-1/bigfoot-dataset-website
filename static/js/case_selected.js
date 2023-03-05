


function data() {
    // Get the input value
    const input = document.getElementById("check").value;
  
    // Send the input to the backend without waiting for a response
    fetch("/individual_case", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    });
  
    // Log a message to the console
    console.log("Data sent to the backend");
  }
  
  


  