var s = null;
var on_pic = true, on_temp = false, on_hum = false, on_water = false;

function encode (input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    while (i < input.length) {
        chr1 = input[i++];
        chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
        chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }
        output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
            keyStr.charAt(enc3) + keyStr.charAt(enc4);
    }
    return output;
}

var img = document.createElement('img');
document.body.appendChild(img);

window.onload = function() 
{
    s = new WebSocket("ws://poorhackers.com:9000/");
    s.onopen = function(e) { console.log("opened");  }
    s.onclose = function(e) { console.log("closed"); }    
    s.binaryType = 'arraybuffer'

s.onmessage = function(e) { 
    var x=document.getElementById('data').rows
    var y1 = x[0].cells
    var y2 = x[1].cells
    var y3 = x[2].cells

    if (on_pic) {
	on_pic = false;on_temp = true;
	console.log("PIC: " + e.data);

	var arrayBuffer = e.data;

	img.src = 'data:image/jpeg;base64,' 
	    + encode(new Uint8Array(arrayBuffer));
    }
    else if (on_temp) {
	on_temp = false; on_hum = true;
	y1[1].innerHTML = e.data + " F";
	//console.log("TMP: " + e.data); 
    }
    else if (on_hum) {
	on_hum = false; on_water = true;
	y2[1].innerHTML= e.data + " %";
	//console.log("HUMID: " + e.data); 	
    }
    else if (on_water) {
	on_water = false;
	on_pic = true;

	if (e.data == "1") {
	    y3[1].innerHTML="Absent";
	}
	else if (e.data == "0") {
	    y3[1].innerHTML="Present";	    
	}
	else {
	    y3[1].innerHTML="SENSOR ERROR, REFRESH.";	    
	}

	//console.log("water: " + e.data); 
    }
}
}

function looper()
{
    s.send("x");
}

setInterval(looper, 5000);