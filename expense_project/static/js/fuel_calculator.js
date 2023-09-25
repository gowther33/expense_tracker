
var IDs = 1
origin_array = [];
destination_array = [];
distances = [];
var origin = null;
var destination = null;
var set_delete_row = null;
var fuel_rate;
var maintenance_factor;
var idling_factor;
fetch("/fuel-calculator/get-fuel")
.then((res) => res.json())
.then((data) => {
    fuel_rate = data.rate;
    maintenance_factor = data.maintenance;
    idling_factor = data.idling
    sessionStorage.setItem("fuel_rate", fuel_rate);
    console.log(`Fuel Rate: ${fuel_rate}`);
    console.log(`maintenance: ${maintenance_factor}`);
    console.log(`idling: ${idling_factor}`);
})
function addtest()
{	
    console.log(`IDs: ${IDs}`)
    document.getElementById("addbtn").disabled = true;
    document.getElementById("dwnbtn").disabled = true;
    document.getElementById("labbtn").disabled = true;
    document.getElementById("done").disabled = true;
    var table = document.getElementById("Tadd");
    var rows = table.rows.length;
    //document.getElementById("rows").innerHTML = rows;
    if (rows == 2)
        {
            document.getElementById("deleterow").type = 'number';
            document.getElementById("deleterow").setAttribute("min",1);
        }
    var row = table.insertRow(rows-1);
    document.getElementById("deleterow").setAttribute("max",rows-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = table.rows.length-2;
    if (table.rows.length<=3)
        {
            cell2.innerHTML =  "<input name = 'Origin' id = 'Origin' type = 'text' list = 'Centres' required style = 'width:100%' onchange = 'set_initial_origin(this)'>";
        }
    else
        {
            origin = destination_array[table.rows.length-4];
            setorigin();
        }
    cell3.innerHTML =  "<input name = 'Destination' id = 'Destination' type = 'text' list = 'Centres' required style = 'width:100%' onchange = 'set_initial_destination(this)'>";
}
function downroute()
{	
    document.getElementById("addbtn").disabled = true;
    document.getElementById("dwnbtn").disabled = true;
    document.getElementById("done").disabled = true;
    var table = document.getElementById("Tadd");
    var rows = table.rows.length;
    //document.getElementById("rows").innerHTML = rows;
    if (rows == 2)
        {
            document.getElementById("deleterow").type = 'number';
            document.getElementById("deleterow").setAttribute("min",1);
        }
    var row = table.insertRow(rows-1);
    document.getElementById("deleterow").setAttribute("max",rows-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = table.rows.length-2;
    cell2.innerHTML =  destination_array[table.rows.length-4];
    origin = destination_array[table.rows.length-4];
    cell3.innerHTML =  origin_array[table.rows.length-4];
    destination = origin_array[table.rows.length-4];
}
function tolab()
{	
    document.getElementById("addbtn").disabled = true;
    document.getElementById("dwnbtn").disabled = true;
    document.getElementById("done").disabled = true;
    var table = document.getElementById("Tadd");
    var rows = table.rows.length;
    //document.getElementById("rows").innerHTML = rows;
    if (rows == 2)
        {
            document.getElementById("deleterow").type = 'number';
            document.getElementById("deleterow").setAttribute("min",1);
        }
    var row = table.insertRow(rows-1);
    document.getElementById("deleterow").setAttribute("max",rows-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = table.rows.length-2;
    cell2.innerHTML =  destination_array[table.rows.length-4];
    origin = destination_array[table.rows.length-4];
    cell3.innerHTML = "Biolight Laboratory";//origin_array[table.rows.length-4];
    destination = "Biolight Laboratory";//origin_array[table.rows.length-4];
}
function set_initial_origin(x)
{
    origin = x.value;
    document.getElementById("set_origin").disabled = false;
}
function set_initial_destination(x)
{
    destination = x.value;
}
function setorigin()
{
    var t = document.getElementById("Tadd");
    var editrow = t.rows.length-2;
    origin_array[t.rows.length-3] = origin;
    t.rows[editrow].cells[1].innerHTML = `<input id = 'org${IDs}' name = 'origin'  type = 'text'  style = 'width:100%' readonly>`;
    document.getElementById(`org${IDs}`).setAttribute('value',origin)  
    document.getElementById("set_origin").disabled = true;
    document.getElementById("set_destination").disabled = false;
    //document.getElementById("rows").innerHTML = origin_array;
    console.log(`ids in origin: ${IDs}`)
}
function setdestination()
{
    var t = document.getElementById("Tadd");
    var editrow = t.rows.length-2;
    destination_array[t.rows.length-3] = destination;
    // t.rows[editrow].cells[2].innerHTML = destination;
    t.rows[editrow].cells[2].innerHTML = `<input id = 'dest${IDs}' name = 'destination'  type = 'text'  style = 'width:100%' readonly>`;
    document.getElementById(`dest${IDs}`).setAttribute('value',destination)
    document.getElementById("addbtn").disabled = false;
    document.getElementById("dwnbtn").disabled = false;
    document.getElementById("labbtn").disabled = false;
    document.getElementById("set_destination").disabled = true;
    console.log(`ids in destination: ${IDs}`)
    //document.getElementById("delete").disabled = false;
    //document.getElementById("rows1").innerHTML = destination_array;
    // Row added
    IDs++;
    update();
    Total();
}
function setDeleteRow(x)
{
    set_delete_row = x.value;
    //document.getElementById("rows").innerHTML = set_delete_row;
}
function delete_row()
{
    var table = document.getElementById("Tadd");
    var rows = table.rows.length;
    if (rows == 2)
    {
        document.getElementById("deleterow").setAttribute("min",1);
        alert("No rows to delete, please add rows first!");
    }
    else if (set_delete_row == 0)
    {
        slert("Please change row value to minimum 1");
    }
    else
    {
        document.getElementById("Tadd").deleteRow(set_delete_row);
        origin_array.splice(set_delete_row-1,1);
        destination_array.splice(set_delete_row-1, 1);
        distances.splice(set_delete_row-1, 1);
        //document.getElementById("rows").innerHTML = origin_array;
        //document.getElementById("rows1").innerHTML = destination_array;
        document.getElementById("delete").disabled = true;
        update();
        Total();
    }
    rows = table.rows.length;
    document.getElementById("deleterow").setAttribute("max",rows-2);
    document.getElementById("addbtn").disabled = false;
}
function update()
{					
    var table = document.getElementById("Tadd");
    var tableLength = table.rows.length;
    var current_origin;
    var current_destination;
    for (var i = 0; i<tableLength-2; i++)
        {
            current_origin = origin_array[i];
            current_destination = destination_array[i];
            /*if (current_origin == "Biolight Laboratory" && current_destination == "AnkleSaria")
                {
                    distances[i] = 3;
                }*/
            if ((current_origin == "AnkleSaria" && current_destination == "Biolight Laboratory") || (current_origin == "Biolight Laboratory" && current_destination == "AnkleSaria"))
                {
                    distances[i] = 3;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Kulsoom")
                {
                    distances[i] = 8.7;
                }
            else if (current_origin == "Dr. Kulsoom" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 10.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Tahir Shamsi")
                {
                    distances[i] = 8.7;
                }
            else if (current_origin == "Tahir Shamsi" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 8.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Taj Medical Complex")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Al-Hayyat Medical Centre")
                {
                    distances[i] = 4.0;
                }
            else if (current_origin == "Al-Hayyat Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.0;
                }
            else if (current_origin == "Taj Medical Complex" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 3.6;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Al-Shifa Clinic")
                {
                    distances[i] = 1.9;
                }
            else if (current_origin == "Al-Shifa Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.4;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 8.2;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 8.2;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 6.5;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 6.5;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 4;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 4;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "JPMC")
                {
                    distances[i] = 5;
                }
            else if (current_origin == "JPMC" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "The Laboratory")
                {
                    distances[i] = 3.5;
                }
            else if (current_origin == "The Laboratory" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 3.5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Medicentre Hospital")
                {
                    distances[i] = 2.3;
                }
            else if (current_origin == "Medicentre Hospital" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.3;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Hashmani Hospital")
                {
                    distances[i] = 3.2;
                }
            else if (current_origin == "Hashmani Hospital" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.5;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Medicentre Hospital")
                {
                    distances[i] = 3.9;
                }
            else if (current_origin == "Medicentre Hospital" && current_destination == "AnkleSaria")
                {
                    distances[i] = 3.9;
                }
            else if (current_origin == "Taj Medical Complex" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Taj Medical Complex")
                {
                    distances[i] = 1;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 3.4;
                }
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "AnkleSaria")
                {
                    distances[i] = 3.4;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "JPMC")
                {
                    distances[i] = 3.5;
                }
            else if (current_origin == "JPMC" && current_destination == "AnkleSaria")
                {
                    distances[i] = 3.5;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "The Laboratory")
                {
                    distances[i] = 1;
                }
            else if (current_origin == "The Laboratory" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1;
                }
            else if (current_origin == "Hashmani Hospital" && current_destination == "Taj Medical Complex")
                {
                    distances[i] = 0.6;
                }
            else if (current_origin == "Taj Medical Complex" && current_destination == "Hashmani Hospital")
                {
                    distances[i] = 0.6;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Dr. Kulsoom")
                {
                    distances[i] = 5.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Rida Medical Centre")
                {
                    distances[i] = 5.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 6.3;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Urdu Bazaar")
                {
                    distances[i] = 4.2;
                }
            else if (current_origin == "Urdu Bazaar" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.2;
                }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 6.3;
                }
            /*else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "JPMC")
                {
                    distances[i] = 8.6;
                }*/
            else if (current_origin == "JPMC" && current_destination == "Bismillah Hospital - Korangi")
                {
                    distances[i] = 8.6;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dar-ul-Shifa")
                {
                    distances[i] = 13;
                }
            else if (current_origin == "Dar-ul-Shifa" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 13;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Ali Medical Clinic")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "Khan Clinic")
                {
                    distances[i] = 0.5;
                }
            else if (current_origin == "Khan Clinic" && current_destination == "Ali Medical Clinic")
                {
                    distances[i] = 0.5;
                }
            else if (current_origin == "Khan Clinic" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 8.9;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Khan Clinic")
                {
                    distances[i] = 8.9;
                }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Ali Medical Clinic")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Rida Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 5.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Maryam Market")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Maryam Market" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Khan Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Khan Clinic")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Khan Clinic" && current_destination == "AnkleSaria")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Khan Clinic")
                {
                    distances[i] = 2.2;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Nawab Clinic")
                {
                    distances[i] = 2.6;
                }
            else if (current_origin == "Nawab Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.6;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Maryam Medical Centre")
                {
                    distances[i] = 2.6;
                }
            else if (current_origin == "Maryam Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.6;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Tariq Clinic")
                {
                    distances[i] = 4.0;
                }
            else if (current_origin == "Tariq Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.0;
                }	
            else if (current_origin == "Biolight Laboratory" && current_destination == "Husaini Collection Point - Nishter Park")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Husaini Collection Point - Nishter Park" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Jilani Medical Centre")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Jilani Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Jilani Medical Centre" && current_destination == "Nawab Clinic")
                {
                    distances[i] = 1.0;
                }
            else if (current_origin == "Nawab Clinic" && current_destination == "Jilani Medical Centre")
                {
                    distances[i] = 1.0;
                }
            else if (current_origin == "Jilani Medical Centre" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 1.0;
                }
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "Jilani Medical Centre")
                {
                    distances[i] = 1.0;
                }
            else if (current_origin == "Husaini Collection Point - Nishter Park" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 2.1;
                }
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "Husaini Collection Point - Nishter Park")
                {
                    distances[i] = 2.1;
                }
            else if (current_origin == "Husaini Collection Point - Nishter Park" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Husaini Collection Point - Nishter Park")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "JPMC" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 4.1;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "JPMC")
                {
                    distances[i] = 4.4;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 0.3;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 0.3;
                }
            else if (current_origin == "JPMC" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 4.4;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "JPMC")
                {
                    distances[i] = 4.7;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Bismillah Hospital - Korangi")
                {
                    distances[i] = 5.2;
                }
            else if (current_origin == "Bismillah Hospital - Korangi" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 5.2;
                }
            else if (current_origin == "The Laboratory" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 9.9;
                }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "The Laboratory")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Bismillah Hospital - Korangi")
                {
                    distances[i] = 5.0;
                }
            else if (current_origin == "Bismillah Hospital - Korangi" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 5.0;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Board Office")
                {
                    distances[i] = 7.7;
                }
            else if (current_origin == "Board Office" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 7.7;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "LUHMS - Gulshan")
                {
                    distances[i] = 7.5;
                }
            else if (current_origin == "LUHMS - Gulshan" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 7.5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "LUHMS - Fatima Bai")
                {
                    distances[i] = 1.2;
                }
            else if (current_origin == "LUHMS - Fatima Bai" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 1.5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Etemad Medical Centre")
                {
                    distances[i] = 1.4;
                }
            else if (current_origin == "Etemad Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 1.4;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "7th Day Adventist Hospital")
                {
                    distances[i] = 2.8;
                }
            else if (current_origin == "7th Day Adventist Hospital" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.8;
                }
            else if (current_origin == "7th Day Adventist Hospital" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1.5;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "7th Day Adventist Hospital")
                {
                    distances[i] = 1.5;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 7.0;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 7.0;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dua Clinic")
                {
                    distances[i] = 3.3;
                }
            else if (current_origin == "Dua Clinic" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.0;
                }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "Dua Clinic")
                {
                    distances[i] = 6.1;
                }
            else if (current_origin == "Dua Clinic" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 5.8;
                }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 6.2;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 5.8;
                }	
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "JPMC")
                {
                    distances[i] = 6.5;
                }
            else if (current_origin == "JPMC" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 7.5;
                }		
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "Nawab Clinic")
                {
                    distances[i] = 0.75;
                }
            else if (current_origin == "Nawab Clinic" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 0.75;
                }
            else if (current_origin == "Nawab Clinic" && current_destination == "AnkleSaria")
                {
                    distances[i] = 4.7;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Nawab Clinic")
                {
                    distances[i] = 4.7;
                }
            else if (current_origin == "Rida Medical Centre" && current_destination == "LUHMS")
                {
                    distances[i] = 4.1;
                }
            else if (current_origin == "LUHMS" && current_destination == "Rida Medical Centre")
                {
                    distances[i] = 3.3;
                }
            else if (current_origin == "Taj Medical Complex" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 7.0;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Taj Medical Complex")
                {
                    distances[i] = 7.0;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "AnkleSaria")
                {
                    distances[i] = 9.2;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 9.2;
                }
            else if (current_origin == "Dr. Ismat House (Pakola Masjid)" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 2.0;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Ismat House (Pakola Masjid)")
                {
                    distances[i] = 2.0;
                }
            else if (current_origin == "Dr. Ismat House (Pakola Masjid)" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1.8;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Dr. Ismat House (Pakola Masjid)")
                {
                    distances[i] = 2.7;
                }
            else if (current_origin == "Sir Syed Hospital" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 11.0;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Sir Syed Hospital")
                {
                    distances[i] = 11.0;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Ismat House (Pakola Masjid)")
                {
                    distances[i] = 11.0;
                }
            else if (current_origin == "Sir Syed Hospital" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 1.5;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Sir Syed Hospital")
                {
                    distances[i] = 1.5;
                }
            else if (current_origin == "Kharadar General Hospital" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 8.1;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Kharadar General Hospital")
                {
                    distances[i] = 7.4;
                }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Dr. Farrukh")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Dr. Farrukh" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Kharadar General Hospital" && current_destination == "JPMC")
                {
                    distances[i] = 6.8;
                }
            else if (current_origin == "JPMC" && current_destination == "Kharadar General Hospital")
                {
                    distances[i] = 7.5;
                }
            else if (current_origin == "Sir Syed Hospital" && current_destination == "JPMC")
                {
                    distances[i] = 5.1;
                }
            else if (current_origin == "JPMC" && current_destination == "Sir Syed Hospital")
                {
                    distances[i] = 5.3;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Ali Medical Clinic")
                {
                    distances[i] = 2.9;
                }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "AnkleSaria")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "AnkleSaria" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "AnkleSaria")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 5.0;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "Ali Medical Clinic")
                {
                    distances[i] = 5.0;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "Mehran Medical Centre")
                {
                    distances[i] = 9.5;
                }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 7.7;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 3.5;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Dr. Ejaz Clinic")
            {
                distances[i] = 3.5;
            }
            else if (current_origin == "Get Well Clinic" && current_destination == "Sir Syed Hospital")
            {
                distances[i] = 6.4;
            }
            else if (current_origin == "Sir Syed Hospital" && current_destination == "Get Well Clinic")
            {
                distances[i] = 5.2;
            }
            else if (current_origin == "Life Care Hospital" && current_destination == "Dr. Ejaz Clinic")
            {
                distances[i] = 0.3;
            }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Life Care Hospital")
            {
                distances[i] = 0.3;
            }
            else if (current_origin == "Life Care Hospital" && current_destination == "Mehran Medical Centre")
            {
                distances[i] = 0.6;
            }
            else if (current_origin == "Mehran Medical Centre" && current_destination == "Life Care Hospital")
            {
                distances[i] = 0.6;
            }
            else if (current_origin == "Life Care Hospital" && current_destination == "Biolight Laboratory")
            {
                distances[i] = 7.8;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Life Care Hospital")
            {
                distances[i] = 7.8;
            }
            else if (current_origin == "Gilani Clinic (Dr. DK)" && current_destination == "Biolight Laboratory")
            {
                distances[i] = 2.3;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Gilani Clinic (Dr. DK)")
            {
                distances[i] = 2.3;
            }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 1.6;
                }
            else if (current_origin == "Bismillah Hospital - Baloch Colony" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 6.2;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Bismillah Hospital - Baloch Colony")
                {
                    distances[i] = 6.2;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "Dr. Ejaz Clinic")
                {
                    distances[i] = 9.5;
                }
            else if (current_origin == "Dr. Ejaz Clinic" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 7.7;
                }
            else if (current_origin == "Dr. Wazir Clinic" && current_destination == "JPMC")
                {
                    distances[i] = 4.5;
                }
            else if (current_origin == "JPMC" && current_destination == "Dr. Wazir Clinic")
                {
                    distances[i] = 3.6;
                }	
            else if (current_origin == "Falahi Medical Centre" && current_destination == "Biolight Laboratory")
            {
                distances[i] = 3.0;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Falahi Medical Centre")
            {
                distances[i] = 2.9;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Habib Public School")
            {
                distances[i] = 6.8;
            }		
            else if (current_origin == "Habib Public School" && current_destination == "Biolight Laboratory")
            {
                distances[i] = 6.8;
            }
            else if (current_origin == "Ali Medical Clinic" && current_destination == "Maryam Market")
            {
                distances[i] = 2.7;
            }
            else if (current_origin == "Maryam Market" && current_destination == "Ali Medical Clinic")
            {
                distances[i] = 4.0;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Godam Chowrangi - Brooks Chowrangi")
            {
                distances[i] = 9.8;
            }
            else if (current_origin == "Godam Chowrangi - Brooks Chowrangi" && current_destination == "Biolight Laboratory")
            {
                distances[i] = 9.8;
            }
            else if (current_origin == "Get Well Clinic" && current_destination == "Godam Chowrangi - Brooks Chowrangi")
            {
                distances[i] = 4.6;
            }
            else if (current_origin =="Godam Chowrangi - Brooks Chowrangi" && current_destination == "Get Well Clinic")
            {
                distances[i] = 6.5;
            }
            else if (current_origin == "Nawab Clinic" && current_destination == "Tariq Clinic")
                {
                    distances[i] = 2.3;
                }
            else if (current_origin == "Tariq Clinic" && current_destination == "Nawab Clinic")
                {
                    distances[i] = 2.3;
                }
            else if (current_origin == "Husaini Collection Point - Nishter Park" && current_destination == "The Laboratory")
            {
                distances[i] = 2.3;
            }
            else if (current_origin == "The Laboratory" && current_destination == "Husaini Collection Point - Nishter Park")
            {
                distances[i] = 2.3;
            }
            else if (current_origin == "Biolight Laboratory" && current_destination == "Naseem Medical Centre")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Naseem Medical Centre" && current_destination == "Biolight Laboratory")
                {
                    distances[i] = 8.5;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Taj Medical Complex")
                {
                    distances[i] = 6.8;
                }
            else if (current_origin == "Taj Medical Complex" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 7.3;
                }
            else if (current_origin == "Al-Hafiz Clinic" && current_destination == "Board Office")
                {
                    distances[i] = 5.7;
                }
            else if (current_origin == "Board Office" && current_destination == "Al-Hafiz Clinic")
                {
                    distances[i] = 5.7;
                }
            else if (current_origin == "Get Well Clinic" && current_destination == "Naseem Medical Centre")
                {
                    distances[i] = 5.3;
                }
            else if (current_origin == "Naseem Medical Centre" && current_destination == "Get Well Clinic")
                {
                    distances[i] = 4.0;
                }							
            else
                {
                    distances[i] = 0;
                }
            table.rows[i+1].cells[0].innerHTML = i+1;
            let dis = distances[i]
            table.rows[i+1].cells[3].innerHTML = `<input type = 'number' name = 'distance' value = ${dis}  style = 'width:100%' readonly>`;

            // table.rows[i+1].cells[3].innerHTML = distances[i]
            //table.rows[i+1].cells[2].innerHTML = destination_array[i];
            //table.rows[i+1].cells[1].innerHTML = origin_array[i];
        }
    document.getElementById("done").disabled = false;
}
function Total()
{
    var table = document.getElementById("Tadd");
    // Iterate through each row in the table body
    const tbody = table.querySelector("tbody");
    const rows = tbody.getElementsByTagName("tr");

    var tableLength = table.rows.length;

    console.log(`table length: ${tableLength}`)
    var Total = 0;
    for (let i = 1; i<tableLength-1; i++)
        {

            const inputD = rows[i].getElementsByTagName("td")[3].querySelector("input[type='number']");

            // Ensure the input field exists and has a valid numerical value
            if (inputD && !isNaN(inputD.valueAsNumber)) {
              // Add the numerical value to the total
              Total += inputD.valueAsNumber;
            }

            // Added
            // let row_dist = document.getElementById(`dist${i}`).value
            // console.log(`distance: ${row_dist}`)
            // Total += row_dist
            //
            // Total += parseFloat(document.getElementById("Tadd").rows[i].cells[3].innerHTML)
        }
    total_distance = parseFloat(Total.toFixed(2) +" km");
    // table.rows[tableLength-1].cells[1].innerHTML = (Total).toFixed(2)+" km";
    console.log("Total distance")
    table.rows[tableLength-1].cells[1].innerHTML = `<input name = 'Total_Distance' id = 'Total_Distance' value = ${total_distance} type = 'text' style = 'width:100%' readonly>`
    sessionStorage.setItem("Psum", Total);
    document.getElementById("done").disabled = false;
}
function updatefuel()
{
    var Total_distance = parseFloat(sessionStorage.getItem("Psum")).toFixed(2);
    //var Total_distance = parseFloat(sessionStorage.getItem("Psum"));
    sessionStorage.setItem("Total_distance", Total_distance);

    var fuel = Total_distance*(fuel_rate/45)*idling_factor;
    // var fuel = Total_distance*(fuel_rate/45)*1;

    //var fuel = Total_distance*(fuel_rate/45);
    sessionStorage.setItem("calfuel", (fuel).toFixed(2));
    var incentive = 0;
    var distance_1 = 0;
    var distance_2 = 0;
    var distance_3 = 0;
    
    incentive = Total_distance*maintenance_factor;
    sessionStorage.setItem("incent", (incentive).toFixed(2));
    var Total_amount = fuel + incentive;
    sessionStorage.setItem("TAP", Math.ceil(Total_amount));
    
    fuel = fuel.toFixed(2)
    incentive = Math.ceil(incentive)
    Total_amount = Total_amount.toFixed(2)

    // document.getElementById("fuelrate").innerHTML = "Rs."+fuel_rate+"/-";
    // document.getElementById("calfuel").innerHTML = "Rs."+(fuel).toFixed(2)+"/-";
    // document.getElementById("incent").innerHTML = "Rs."+Math.ceil(incentive)+"/-";
    // document.getElementById("TAP").innerHTML = "Rs."+Math.ceil(Total_amount)+"/-";

    document.getElementById("fuelrate").innerHTML = `<input type = 'number' name = 'fuelrate' value = ${fuel_rate} style = 'width:100%'  readonly>`;
    document.getElementById("calfuel").innerHTML = `<input type = 'number' name = 'calfuel' value = ${fuel} style = 'width:100%'  readonly>`;
    document.getElementById("incent").innerHTML = `<input type = 'number' name = 'incentive' value = ${incentive} style = 'width:100%'  readonly>`;
    document.getElementById("TAP").innerHTML = `<input type = 'number' name = 'TAP' value = ${Total_amount} style = 'width:100%'  readonly>`;
}
function enableGrcpt()
{


    document.getElementById("addbtn").disabled = true;
    document.getElementById("dwnbtn").disabled = true;
    document.getElementById("labbtn").disabled = true;
    document.getElementById("Grcpt").disabled = false;
    document.getElementById("delete").disabled = true;
    document.getElementById("deleterow").type = 'hidden';

}