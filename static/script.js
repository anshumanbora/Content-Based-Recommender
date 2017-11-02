
$(document).ready(function() {


    document.getElementById('1').style.display = 'none';
    document.getElementById('2').style.display = 'none';
    document.getElementById('3').style.display = 'none';
    document.getElementById('4').style.display = 'none';
    document.getElementById('5').style.display = 'none';
    document.getElementById('6').style.display = 'none';
    document.getElementById('7').style.display = 'none';
    document.getElementById('8').style.display = 'none';
    document.getElementById('9').style.display = 'none';
    document.getElementById('10').style.display = 'none';






});

function getRecommendation(x){

        var xhr = new XMLHttpRequest();
        var url = "http://127.0.0.1:5000/recommend";
        xhr.open("POST", url, true);
        uriData = "index="+x;
        console.log(uriData);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {//Call a function when the state changes.
            if(xhr.readyState == 4 && xhr.status == 200) {
                //console.log(xhr.responseText);
                var results = JSON.parse(xhr.responseText);
                console.log(results[0]);

                for (var i=0; i<results.length; i++){
                    var number = i+1;
                    var newElement = '<div ><h4><br/><br/><br/>'+'Document# '+ number +', '+results[i].title+'</h4><br/>'+results[i].html+'<div><br/>';
                    // console.log(results[i].html);
                    $('#'+x).append(newElement);

                }
            }
        }
        xhr.send(uriData);
        $("#"+x).toggle();




}
