
function input_changed(){
	const open_jaw = document.getElementById("openjaw")
	const location2 = document.querySelector("#second_locations")
	if (open_jaw.checked){
		location2.style.display = "block"	
	}else{
		location2.style.display = "none"
	}

	const single = document.getElementById("single")
	const time2 = document.getElementById("date2")

	if(single.checked){
		time2.style.display = "none"	
	}else{
		time2.style.display = "block"
	}
}

function search_json() {
	const flight_class = document.querySelector('input[name="flightclass"]:checked').value;
	const adults = document.querySelector('#adults').value;
	const children = document.querySelector('#children').value
	const infants = document.querySelector('#infants').value
	const flight_type = document.querySelector('input[name ="flighttype"]:checked').value
	
	const from1 = document.querySelector("#fromplace").value
	const to1 = document.querySelector('#toplace').value
	const from2 = document.querySelector('#fromplace2').value
	const to2 = document.querySelector('#toplace2').value
	
	const date1 = new Date(document.querySelector("#datefrom").value)
	const date2 = new Date(document.querySelector("#dateto").value)
	const flexdate1 = document.querySelector("#flexdate1").checked
	const flexdate2 = document.querySelector("#flexdate2").checked


	var obj = {
		flight_class: flight_class,
		flight_type: flight_type,
		adults: adults,
		children: children,
		infants: infants,
	}
	if (flight_type == "open_jaw"){
		obj.from1 = from1
		obj.from2 = from2
		obj.to1 = to1
		obj.to2 = to2
	}else{
		obj.from = from1
		obj.to = to1
	}
	if (flight_type == "single"){
		obj.date = date1
		obj.flexdate = flexdate1
	}else{
		obj.date1 = date1
		obj.date2 = date2
		obj.flexdate1 = flexdate1
		obj.flexdate2 = flexdate2
	}
	return obj
}

function user_json(){
	const device_type = document.querySelector('input[name="devicetype"]:checked').value;
	const user_type = document.querySelector('input[name="user_type"]:checked').value;
	return {
		device_type: device_type,
		user_type: user_type,
	}
}

function input_submit() {
    const currentHost = window.location.hostname;
    const currentPort = window.location.port;
    const url = `http://${currentHost}:${currentPort}/searchflight/`;

    var xmlHttp = new XMLHttpRequest();

    xmlHttp.open("POST", url);
    xmlHttp.setRequestHeader("Content-type", "application/json; charset=utf-8");

    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            try {
                var response = JSON.parse(xmlHttp.responseText);
				alert(JSON.stringify(response));
            } catch (err) {
                console.error("Error parsing JSON response:", err);
            }
        }
    };

    const result = {
        search: search_json(),
        user: user_json(),
    }

    xmlHttp.send(JSON.stringify(result));
}

function get_results() {
    const requestdata = {
        search: search_json(),
        user: user_json(),
    };

    const currentHost = window.location.hostname;
    const currentPort = window.location.port;
    const url = `http://${currentHost}:${currentPort}/getresults/`;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", url);
    xmlHttp.setRequestHeader("Content-type", "application/json; charset=utf-8");

    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                try {
                    var response = JSON.parse(xmlHttp.responseText);
                    handleResults(response);
                } catch (err) {
                    console.error("Error parsing JSON response:", err);
                }
            } else {
                console.error("Error: ", xmlHttp.status);
            }
        }
    };

    xmlHttp.send(JSON.stringify(requestdata));
}

function handleResults(response) {
	var flightResults = response.results;
    var resultsContainer = document.getElementById("results_content");
    resultsContainer.innerHTML = "<hr>Results:<br>";
	for (var i = 0; i < flightResults.length; i++) {
		var result = flightResults[i];
		resultsContainer.innerHTML += "<strong>Price:</strong> " + result.price + "<br>";

		for (var j = 0; j < result.legs.length; j++) {
			var leg = result.legs[j];
			resultsContainer.innerHTML += "<strong>Leg " + (j + 1) + ":</strong><br>";
			resultsContainer.innerHTML += "Start Time: " + leg.starttime + "<br>";
			resultsContainer.innerHTML += "End Time: " + leg.endtime + "<br>";
			resultsContainer.innerHTML += "Airports: " + leg.airports.join(" -> ") + "<br><br>";
		}

		resultsContainer.innerHTML += "<hr>";
	}
}

function init(){
	input_changed()
	//const input_form = document.querySelector("input_form");
	//input_form.addEventListener("change", input_edit);
	//input_form.addEventListener("submit", input_submit);
}

