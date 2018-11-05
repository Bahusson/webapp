$(document).ready(function(){

            //Funkcja wywołująca wynik gry losowej.
        $('#play').click(function(e) {
          e.preventDefault()
            //AJAX przesyła dane dalej aż do randomize1.py
           $.ajax({
                    url: "/lotto/roll/",
                    type: "POST",
                    dataType: "json",
                    data: {
                      gamesel:$('input:radio[name=gamesel]:checked').val(),
                    //  csrfmiddlewaretoken: "{{ csrf_token }}",
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                          },
                    success:function(data){
                    $('#textarea2').val(data['number']);
                    //alert("form submitted: " + data['number']);
                    console.log(data)
                                      }
                  });
        });
});
