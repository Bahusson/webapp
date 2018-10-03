$(function() {
           $(".buttonS").click(function() {
           // validate and process form here
           var radio_button_value;

           if ($("input[name='ex1']:checked").length > 0){
               radio_button_value = $('input:radio[name=ex1]:checked').val();
           }
           else{
               alert("No button selected, try again!");
               return false;
           }
           $.ajax({
                          type: "POST",
                          url: "save.php",
                          data: {"ex1":radio_button_value},
                          success: function() {
                               alert("form submitted: "+ radio_button_value);
                          }
                       });
            return false;
         });
});
