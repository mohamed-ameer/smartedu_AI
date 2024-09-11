
let counter=0;

// Set the date we're counting down to
var countDownDate = new Date("Jan 5, 2023 15:37:25").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
  
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
  // console.log(distance); 
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("demo").innerHTML =   minutes + "m :" + seconds + "s ";
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
      document.getElementById("submiteman").disabled = true;
    
  }
     // if student leave page 
     document.onmouseleave= function (event){
      console.log(event);
      event.preventDefault();
      counter++;
      console.log(counter);
      if(counter<3 && distance > 0){
        // var modal = new bootstrap.Modal('#myModal');
          alert('Stop cheating during the quiz so that the quiz won`t be canceled for you');

      }
      if (counter===3 && distance > 0){
            alert("Your quiz has been canceled  ");
           
            document.getElementById("submiteman").click();
            // هقففل زرار الارسال
            // document.getElementById("submiteman").disabled = true;
            // document.forms[0].onsubmit = function (e){
            // e.preventDefault();
            // }
            // Just call the .click method of the button
          }
      }

}, 1000);
// for icon image in Assignment page to upload file
document.onmouseenter= function (event){
  document.getElementById("Upload").style.cursor = "pointer";
  document.getElementsByClassName("Mpointer").style.cursor = "pointer";
}