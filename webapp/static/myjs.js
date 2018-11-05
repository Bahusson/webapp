$(document).ready(function(){

            //Funkcja #play odwołuje się do randomize1.py, wywołuje wynik gry losowej z przycisku "zagraj",
            // i zwraca dane do textarea2.
        $('#play').click(function(e) {
          e.preventDefault()
           $.ajax({
                    url: "/lotto/roll/",
                    type: "POST",
                    dataType: "json",
                    data: {
                      gamesel:$('input:radio[name=gamesel]:checked').val(),
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                          },
                    success:function(data){
                    $('#textarea2').val(data['number']);
                                      }
                  });
        });
            //Funkcja #generate odwołuje się do randomize.py, obsługuje większą częśc
            //programu po kliknięciu w "generuj" - przesyła dane do "textarea".
        $('#generate').click(function(e) {
          e.preventDefault()
           $.ajax({
                    url: "/lotto/generate/",
                    type: "POST",
                    dataType: "json",
                    data: {
/*Numer gry*/         gamesel:$('input:radio[name=gamesel]:checked').val(),
/*Data Od:*/          datefrom:$('input:date[name=date1]').val(),
/*Data Do:*/          dateto:$('input:date[name=date2]').val(),
/*Cała baza*/         dateall:$('input:checkbox[name=checkboxG1]').val(),
/*Skrajne numery*/    numhilow:$('input:checkbox[name=checkboxG2]').val(),
/*Pomiń losowania*/   norolls:$('input:checkbox[name=checkboxG3]').val(),
/*Skrajne numery*/    mostoften:$('input:numinput[name=numinput]').val(),
/*Średnie wyników*/   avgscores:$('input:checkbox[name=checkboxG4]').val(),
/*Generuj wykres*/    graph:$('input:checkbox[name=checkboxG5]').val(), /*Ten można by alternatywnie zrobic jako button z oddzielną funkcją*/
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                          },
                    success:function(data){
                    $('#textarea').val(data['number']);
                    //alert("form submitted: " + data['number']);
                    console.log(data)
                                      }
                  });
        });
});
