$(document).ready(function(){

           $('#play').click(function() {
           // validate and process form here
            /*  alert("button"); */


            var radio_button_value;
            radio_button_value = $('input:radio[name=gamesel]:checked').val();
            alert("TEST!"+radio_button_value);
            }

           $.ajax({
                          type: "POST",
                          url: "save.php",
                          data: {"gamesel":radio_button_value},
                          success: function() {
                               alert("form submitted: "+ radio_button_value);
                          }
                       });
            return false;
)});
