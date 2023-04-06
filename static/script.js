// Checks if the key size is valid
function key_validation() {
    let help_key = document.querySelector("#help_key");
    let key_input = document.querySelector("#keySize");

    // Invalid key size
    if (key_input.value < 256) {
        help_key.innerHTML = "Key size must be at least 256 bits";
        help_key.classList.add("is-danger");
        key_input.classList.add("is-danger");
        help_key.classList.remove("is-success");
        key_input.classList.remove("is-success");
    }
    // Key size is valid
    else {
        help_key.innerHTML = "Key size is valid";
        help_key.classList.add("is-success");
        key_input.classList.add("is-success");
        help_key.classList.remove("is-danger");
        key_input.classList.remove("is-danger");
    }
}

// Checks if the message is valid
function message_validation() {
    let help_message = document.querySelector("#help_message");
    let message_input = document.querySelector("#msg");

    // Message is empty
    if (message_input.value.length == 0) {
        help_message.innerHTML = "Message field cannot be empty";
        help_message.classList.add("is-danger");
        message_input.classList.add("is-danger");
        help_message.classList.remove("is-success");
        message_input.classList.remove("is-success");
    }
    // Message is valid
    else {
        help_message.innerHTML = "Message is valid";
        help_message.classList.add("is-success");
        message_input.classList.add("is-success");
        help_message.classList.remove("is-danger");
        message_input.classList.remove("is-danger");
    }
}
