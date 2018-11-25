$(document).ready(function(){
        $("#numinput").val("0");
        $('input[type="checkbox"]').val("0");
        $('input[type="checkbox"]').click(function () {
          $(this).prop("checked") ? $(this).val("1") : $(this).val("0")
        });

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
                    data: {
/*Numer gry*/         gamesel:$('input:radio[name=gamesel]:checked').val(),
/*Data Od:*/          datefrom:$("#date1").val(),
/*Data Do:*/          dateto:$("#date2").val(),
/*Cała baza*/         dateall:$("#checkboxG1").val(),
/*Skrajne numery*/    numhilow:$("#checkboxG2").val(),
/*Pomiń losowania*/   norolls:$("#checkboxG3").val(),
/*Skrajne numery*/    mostoften:$("#numinput").val(),
/*Średnie wyników*/   avgscores:$("#checkboxG4").val(),
/*Generuj wykres*/    graphgen:$("#checkboxG5").val(), /*Ten można by alternatywnie zrobic jako button z oddzielną funkcją*/
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                          },
                    success:function(data){
                //    var jdata = data['hilow','often',"avgsc","rolls"];
                  //  var finaldata = jdata.join("\n\n");
                    $('#textarea1').val(data['hilow'] + "\n\n" + data['often'] + "\n\n" + data['avgsc'] + "\n\n" + data['rolls']);
                    console.log(data)
                                      }
                  });
        });
});
