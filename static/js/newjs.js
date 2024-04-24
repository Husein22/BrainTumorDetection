$(function() {    var body = document.body;
    var regexVelikoSlovo = /[A-Z]/;
    var regexZnak = /[\W_]/;  
    var regexBroj = /\d/;
    $('#insertUser').hide();
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#poruka').hide()
$('#sifra').val("")
$('#ime').val("")

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr( 'src', e.target.result );
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        $('#poruka').hide()

        
        
        readURL(this);
    });


$("#btn-dodaj-termin").on("click",function(e){
e.preventDefault();

docIme=$("#doktor").val()
pacIme=$("#pacijent").val()
datum=$("#datum").val()


if(docIme=="" || pacIme=="" || datum==""){
    $('#porukaTermin').show().addClass('p-3 mb-2 bg-danger text-white');

    $('#porukaTermin').text(' Korisnik nije uspjesno dodan u bazu podataka!');

    alert("Niti jedno ne smije biti prazno!");
    throw new Error("Niti jedno polje ne smije biti prazno!");
}


$.ajax({
    type:"POST",
    url:"unosTermina",
    data:{
        pacijent:pacIme,
        doktor:docIme,
        datum:datum,
    },
    success:function (data) {
        $('#porukaTermin').show().addClass('p-3 mb-2 bg-success text-white');
        $('#porukaTermin').text('Uspjesno ste dodali termin u bazu podataka! ');
        console.log("Uspjesno ste dodali termin u bazu podataka!")
        
    },error: function (error) {

        console.error('Greška prilikom dodavanja korisnika:', error);
    }
})

});

    $('#btn-dodaj-korisnika').on('click', function(e) {
        e.preventDefault();

        var imee = $('#imee').val();
        var sifraa = $('#sifraa').val();
        var slika = $('#fileNameInput').val();
        var rezultat = $('#rezultat').val();
        var doktor = $('#doktorInput').val();
    console.log(rezultat)    
if(imee=="" || sifraa=="" || slika=="" || rezultat=="" || doktor==""){

    $('#poruka').show().show().addClass('p-3 mb-2 bg-danger text-white');
    $('#poruka').text(' Korisnik nije uspjesno dodan u bazu podataka!');

    alert("Niti jedno ne smije biti prazno!");
    throw new Error("Niti jedno polje ne smije biti prazno!");


}
if (!regexVelikoSlovo.test(sifraa) || !regexZnak.test(sifraa) || !regexBroj.test(sifraa)) {
    alert("Šifra mora sadržavati bar jedno veliko slovo, jedan znak (specijalni karakter) i jedan broj.");

    throw new Error("Šifra mora sadržavati bar jedno veliko slovo, jedan znak (specijalni karakter) i jedan broj.");
}
        $.ajax({
            type: 'POST',
            url: '/index', 
            data: {
                imee: imee,
                sifraa: sifraa,
                slika: slika,
                rezultatA: rezultat,
                doktor:doktor
            },
            success: function (data) {
                $('#poruka').show().addClass('p-3 mb-2 bg-success text-white')
                $('#poruka').text('Uspjesno ste dodali korisnika u bazu podataka! ');
                $('#insertUser').hide();
                body.style.backgroundImage = "url('https://wallpaperbat.com/img/219606-free-medical-wallpaper-background.jpg')";


                $('#imageUpload').val(null);


                $('#imagePreview').attr('src', 'https://media.istockphoto.com/id/530190582/photo/white-blank-frame.jpg?s=612x612&w=0&k=20&c=pTsqxeoRVqNBuF5xeeeJ7r3wjKiLTmxvOQzjHH3mIZs=');
                $('#result').hide();

                console.log('Uspjesno ste dodali korisnika u bazu podataka!');
            },
            error: function (error) {
                $('#poruka').text(' Korisnik nije uspjesno dodan u bazu podataka,sifra mora sadrzavati jedno vveliko slovo,znak i broj');

                console.error('Greška prilikom dodavanja korisnika:', error);
            }
        });
    });
    
    


    $(".addtermin-btn").on('click', function() {
        var rowId = $(this).data('rowiddd');
        console.log(rowId)
        addRecord(rowId);
    });
    function addRecord(id) {

            $.ajax({
                type: 'PATCH',
                url: `/addrecord/${id}`,
                success: function(response) {
                    alert("CESTITAMO!Uspjesno ste odobrili termin!");
                    window.location.href =" http://127.0.0.1:5000/i/pregledTermina"
                },
                error: function(error) {
                    console.error('Greška prilikom brisanja zapisa:', error);
                }
            });
        
    }


    $(".delete-btn").on('click', function() {
        var rowId = $(this).data('rowidd');
        console.log(rowId)
        deleteRecord(rowId);
    });
    function deleteRecord(id) {
        if (confirm('Da li ste sigurni da želite obrisati ovaj zapis?')) {
            $.ajax({
                type: 'DELETE',
                url: `/delete/${id}`,
                success: function(response) {
                    console.log('Zapis obrisan!');
                    alert("CESTITAMO!Uspjesno ste izbrisali pregled!");

                    window.location.href =" http://127.0.0.1:5000/i/pregledTermina"
                },
                error: function(error) {
                    console.error('Greška prilikom brisanja zapisa:', error);
                }
            });
        }
    }


    $(".otvori-btn").on('click', function() {
        var rowId = $(this).data('rowid');
    var slikaPac = $(this).data('slikaac'); 
    var sifraPac = $(this).data('sifraac');
    var imePac = $(this).data('imeac');
    var rezultatPac = $(this).data('rezultatac');
    var doktorPac = $(this).data('doktorac');
        openModalWithRowId(rowId, slikaPac, rezultatPac, sifraPac, imePac, doktorPac);
    });
    
    


function openModalWithRowId(rowId,slikaPac,rezultatPac,sifraPac,imePac,doktorPac) {
    $("#idModal").val(rowId);
    $("#imeModal").val(imePac);
    $("#sifraModal").val(sifraPac);
    $("#slikaModal").val(slikaPac);
    $("#rezultatModal").val(rezultatPac);
    $("#doktorModal").val(doktorPac);


}


$(".apdejt").on('click', function() {
    console.log("apdejtovan")
    var rowId = $("#idModal").val();  
    $.ajax({
        type: 'PATCH',
        url: `/update/${rowId}`, 
        data: {
            ime: $("#imeModal").val(),
            sifra: $("#sifraModal").val(),
            slika: $("#slikaModal").val(),
            rezultatt: $("#rezultatModal").val(),
            doktor: $("#doktorModal").val(),
        },
        success: function (data) {
            console.log('Uspješno AZURIRANO!');
            $("#reg-modal").modal('hide'); 
            window.location.href =" http://127.0.0.1:5000/index/pregledPacijenata"
            alert("CESTITAMO!Uspjesno ste ažurirali korisnika!");
            
        }
    });
})




    
    $('#btn-predict').on('click', function(e) {
        var form_data = new FormData($('#upload-file')[0]);

        $(this).hide();
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {

                body.style.backgroundImage = "url('https://wallpaperbat.com/img/197912-wallpaper-light-doctors-medical-study-medical-examination.jpg')";
                $('#imee').val("");
                 $('#sifraa').val("");
                 $('#rezultat').val("");
                 
                $('#insertUser').show();
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#fileNameInput').val(data.file_name);
                $('#rezultat').val(data.result);
                $('#result').text(' Rezultat:  ' + data.result);
                console.log('Success!');
            }, error: function (error) {

                console.error('Greška prilikom kk korisnika:', error);
            }
        });
    });

});
