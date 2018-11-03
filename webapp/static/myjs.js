$(document).ready(function(){

            //Funkcja wywołująca wynik gry losowej.
        $('#play').click(function() {
            var radio_button_value;
            radio_button_value = $('input:radio[name=gamesel]:checked').val();
            /*alert("TEST!"+radio_button_value);*/

            //AJAX przesyła dane dalej aż do randomize1.py
           req = $.ajax({
                    type: "POST",
                    url: "/pybrun/roll/",
                    data: {"gamesel":radio_button_value
                    /*csrfmiddlewaretoken:$('input[csrfmiddlewaretoken]').val(),*/
                  },

                    success:function(){
                    alert("form submitted: "+ radio);

                    }
           });
        });
});
