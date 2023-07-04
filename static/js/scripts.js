function copyToClipboard() {
    /* Get the input field */
    var inputField = document.getElementById("urlinput");
  
    /* Select the text in the input field */
    inputField.select();
    inputField.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text to the clipboard */
    document.execCommand("copy");
  
    /* Alert the user that the text has been copied */
    alert("Copied to clipboard: " + inputField.value);
  }