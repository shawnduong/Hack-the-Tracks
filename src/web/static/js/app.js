/* This is the send button (found by ID). */
const send = document.getElementById("send-grep");

/* Override default form behavior so it doesn't take us to a new page. */
form.addEventListener("submit", (event) =>
{
	event.preventDefault();
});

/* Get the sent command and run it. */
send.addEventListener("click", (event) =>
{
	/* Get the command the user sent. */
	let command = document.getElementById("command").value;

	/* Prepare to POST the data to the API endpoint. */
	let request = new XMLHttpRequest();
	request.open("POST", "/api", true);
	request.setRequestHeader("Content-Type", "application/json");

	/* Send the data. */
	let data = {"command": command};
	request.send(JSON.stringify(data));

	let tmp = document.createElement("p");

	/* Display the output on the page. */
	request.onload = function()
	{
		let response = JSON.parse(this.responseText);
		tmp.innerHTML = response["result"];
	}

	/* Find the output section and add the output to it. */
	document.getElementById("output-grep").innerHTML = "";
	document.getElementById("output-grep").appendChild(tmp);
});
