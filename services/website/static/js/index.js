
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
	const offset1 = document.querySelector("#dateoffset1").value
	const offset2 = document.querySelector("#dateoffset2").value
	const offset3 = document.querySelector("#dateoffset3").value
	const offset4 = document.querySelector("#dateoffset4").value
	var datefrombegin =  new Date()

	//integrade offset idk why they dont work
	datefrombegin.setDate(date1.getDate())
	var datefromend = new Date()
	datefromend.setDate(date1.getDate())
	var datetobegin = new Date()
	datetobegin.setDate(date2.getDate())
	var datetoend = new Date()
	datetoend.setDate(date2.getDate())

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
		obj.dateBegin = datefrombegin
		obj.dateEnd = datefromend
	}else{
		obj.dateFromBegin = datefrombegin
		obj.dateFromEnd = datefromend
		obj.dateToBegin = datetobegin
		obj.dateToEnd = datetoend
	}
	
	return obj
}

function input_submit(){


	const url = 'http://127.0.0.1:5000/searchflight'
	var xmlHttp = new XMLHttpRequest();
    	xmlHttp.open( "POST", url );
	xmlHttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
	xmlHttp.send(JSON.stringify(search_json()));	
	//var response = JSON.parse(xmlHttp.responseText);
	//alert(JSON.stringify(response))
}

function init(){
	input_changed()
	//const input_form = document.querySelector("input_form");
	//input_form.addEventListener("change", input_edit);
	//input_form.addEventListener("submit", input_submit);
}

